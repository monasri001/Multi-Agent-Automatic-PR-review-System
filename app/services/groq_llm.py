"""
Groq LLM wrapper for LangChain compatibility
"""
from typing import List, Optional, Any
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.callbacks import CallbackManagerForLLMRun
import requests
from app.config import settings


class GroqChatLLM(BaseChatModel):
    """Groq API wrapper compatible with LangChain"""
    
    model: str = "llama-3.1-70b-versatile"
    groq_api_key: str = ""
    temperature: float = 0.3
    max_tokens: int = 2000
    
    def __init__(self, model: str = None, groq_api_key: str = None, 
                 temperature: float = None, max_tokens: int = None, **kwargs):
        super().__init__(**kwargs)
        self.groq_api_key = groq_api_key or settings.GROQ_API_KEY
        self.model = model or settings.LLM_MODEL
        self.temperature = temperature if temperature is not None else settings.LLM_TEMPERATURE
        self.max_tokens = max_tokens or settings.MAX_TOKENS
    
    @property
    def _llm_type(self) -> str:
        return "groq"
    
    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Generate a response from Groq API"""
        
        # Convert LangChain messages to Groq format
        groq_messages = []
        for message in messages:
            if isinstance(message, SystemMessage):
                groq_messages.append({"role": "system", "content": message.content})
            elif isinstance(message, HumanMessage):
                groq_messages.append({"role": "user", "content": message.content})
            elif isinstance(message, AIMessage):
                groq_messages.append({"role": "assistant", "content": message.content})
        
        # Call Groq API
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": groq_messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
        
        if stop:
            data["stop"] = stop
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            # Create LangChain compatible response
            message = AIMessage(content=content)
            generation = ChatGeneration(message=message)
            
            return ChatResult(generations=[generation])
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Groq API error: {str(e)}")
    
    def _stream(self, *args, **kwargs):
        """Streaming not implemented yet"""
        raise NotImplementedError("Streaming not yet implemented for Groq")

