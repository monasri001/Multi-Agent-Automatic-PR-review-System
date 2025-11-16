"""
Quick test script to verify setup
"""
import sys

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        from app.config import settings
        print("✓ Config imported")
        
        from app.agents.logic_agent import LogicAgent
        print("✓ LogicAgent imported")
        
        from app.agents.readability_agent import ReadabilityAgent
        print("✓ ReadabilityAgent imported")
        
        from app.agents.performance_agent import PerformanceAgent
        print("✓ PerformanceAgent imported")
        
        from app.agents.security_agent import SecurityAgent
        print("✓ SecurityAgent imported")
        
        from app.services.github_service import GitHubService
        print("✓ GitHubService imported")
        
        from app.services.diff_parser import DiffParser
        print("✓ DiffParser imported")
        
        from app.services.review_orchestrator import ReviewOrchestrator
        print("✓ ReviewOrchestrator imported")
        
        from app.main import app
        print("✓ FastAPI app imported")
        
        print("\n✅ All imports successful!")
        return True
        
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def test_config():
    """Test configuration"""
    print("\nTesting configuration...")
    
    try:
        from app.config import settings
        
        if not settings.GROQ_API_KEY:
            print("⚠️  Warning: GROQ_API_KEY not set in .env file")
            print("   Get your free API key from: https://console.groq.com/")
        else:
            print("✓ GROQ_API_KEY configured")
        
        print(f"✓ LLM Model: {settings.LLM_MODEL}")
        print(f"✓ Max Tokens: {settings.MAX_TOKENS}")
        
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("PR Review Agent - Setup Test")
    print("=" * 50)
    
    imports_ok = test_imports()
    config_ok = test_config()
    
    print("\n" + "=" * 50)
    if imports_ok and config_ok:
        print("✅ Setup looks good! You can now run the server.")
        print("\nTo start the server:")
        print("  python run_server.py")
        print("\nOr:")
        print("  uvicorn app.main:app --reload")
        sys.exit(0)
    else:
        print("❌ Setup issues detected. Please fix the errors above.")
        sys.exit(1)

