"""
FastAPI main application
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.models.schemas import PRReviewRequest, ReviewResponse, HealthResponse
from app.services.github_service import GitHubService
from app.services.review_orchestrator import ReviewOrchestrator
import uvicorn

app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
github_service = GitHubService()
review_orchestrator = ReviewOrchestrator()


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint"""
    return HealthResponse()


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint"""
    return HealthResponse()


@app.post("/review", response_model=ReviewResponse)
async def review_pr(request: PRReviewRequest):
    """
    Review a GitHub Pull Request
    
    Accepts either:
    - PR URL (pr_url)
    - Owner, repo, and PR number
    - Manual diff text
    """
    try:
        diff_text = None
        pr_url = None
        
        # Get diff from different sources
        if request.diff_text:
            # Manual diff input
            diff_text = request.diff_text
        elif request.pr_url or (request.owner and request.repo and request.pr_number):
            # Fetch from GitHub
            try:
                pr_data = github_service.fetch_pr_for_review(
                    pr_url=request.pr_url,
                    owner=request.owner,
                    repo=request.repo,
                    pr_number=request.pr_number
                )
                diff_text = pr_data['diff_text']
                pr_url = pr_data.get('pr_url')
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Failed to fetch PR: {str(e)}")
        else:
            raise HTTPException(
                status_code=400,
                detail="Must provide either diff_text, pr_url, or owner/repo/pr_number"
            )
        
        if not diff_text:
            raise HTTPException(status_code=400, detail="No diff content available")
        
        # Perform review
        review_response = review_orchestrator.review_pr(
            diff_text=diff_text,
            pr_url=pr_url,
            enable_agents=request.enable_agents
        )
        
        return review_response
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post("/review/async", response_model=ReviewResponse)
async def review_pr_async(request: PRReviewRequest):
    """
    Review a GitHub Pull Request (async version)
    
    Same as /review but uses async processing for better performance
    """
    try:
        diff_text = None
        pr_url = None
        
        # Get diff from different sources
        if request.diff_text:
            diff_text = request.diff_text
        elif request.pr_url or (request.owner and request.repo and request.pr_number):
            try:
                pr_data = github_service.fetch_pr_for_review(
                    pr_url=request.pr_url,
                    owner=request.owner,
                    repo=request.repo,
                    pr_number=request.pr_number
                )
                diff_text = pr_data['diff_text']
                pr_url = pr_data.get('pr_url')
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Failed to fetch PR: {str(e)}")
        else:
            raise HTTPException(
                status_code=400,
                detail="Must provide either diff_text, pr_url, or owner/repo/pr_number"
            )
        
        if not diff_text:
            raise HTTPException(status_code=400, detail="No diff content available")
        
        # Perform async review
        review_response = await review_orchestrator.review_pr_async(
            diff_text=diff_text,
            pr_url=pr_url,
            enable_agents=request.enable_agents
        )
        
        return review_response
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

