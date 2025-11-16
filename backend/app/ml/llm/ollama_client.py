"""
Ollama LLM Client for conversational recommendations.
Integrates local LLM (Mistral, LLaMA) for natural language interactions.
"""

import httpx
from typing import List, Dict, Any, Optional
import logging
import json

from app.core.config import settings
from app.core.exceptions import MLModelError

logger = logging.getLogger(__name__)


class OllamaClient:
    """
    Client for Ollama local LLM server.
    Provides conversational recommendations and explanations.
    """
    
    def __init__(self):
        self.base_url = settings.OLLAMA_HOST
        self.model = settings.OLLAMA_MODEL
        self.timeout = settings.OLLAMA_TIMEOUT
        self.client = httpx.AsyncClient(timeout=self.timeout)
    
    async def generate(
        self,
        prompt: str,
        temperature: float = None,
        max_tokens: int = None,
        system: Optional[str] = None
    ) -> str:
        """
        Generate text completion.
        
        Args:
            prompt: User prompt
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate
            system: System message
        
        Returns:
            Generated text
        """
        try:
            temperature = temperature or settings.OLLAMA_TEMPERATURE
            
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_ctx": settings.OLLAMA_NUM_CTX
                }
            }
            
            if system:
                payload["system"] = system
            
            response = await self.client.post(
                f"{self.base_url}/api/generate",
                json=payload
            )
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "")
            
        except Exception as e:
            logger.error(f"Ollama generation failed: {e}")
            raise MLModelError("Ollama", f"Generation failed: {e}")
    
    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = None
    ) -> str:
        """
        Chat completion with message history.
        
        Args:
            messages: List of {role: "user"|"assistant", content: "..."}
            temperature: Sampling temperature
        
        Returns:
            Assistant response
        """
        try:
            temperature = temperature or settings.OLLAMA_TEMPERATURE
            
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_ctx": settings.OLLAMA_NUM_CTX
                }
            }
            
            response = await self.client.post(
                f"{self.base_url}/api/chat",
                json=payload
            )
            response.raise_for_status()
            
            result = response.json()
            return result.get("message", {}).get("content", "")
            
        except Exception as e:
            logger.error(f"Ollama chat failed: {e}")
            raise MLModelError("Ollama", f"Chat failed: {e}")
    
    async def generate_recommendation_explanation(
        self,
        movie_title: str,
        user_history: List[str],
        scores: Dict[str, float]
    ) -> str:
        """
        Generate natural language explanation for recommendation.
        
        Args:
            movie_title: Recommended movie
            user_history: List of movies user enjoyed
            scores: Component scores
        
        Returns:
            Human-readable explanation
        """
        system_prompt = """You are a movie recommendation assistant. 
        Generate a brief, engaging explanation for why a movie is recommended 
        based on the user's viewing history and similarity scores. 
        Keep it under 3 sentences and sound natural."""
        
        history_str = ", ".join(user_history[:5])
        scores_str = ", ".join([f"{k}: {v:.2f}" for k, v in scores.items()])
        
        prompt = f"""Movie: {movie_title}
User enjoyed: {history_str}
Similarity scores: {scores_str}

Explain why this movie is recommended:"""
        
        try:
            explanation = await self.generate(
                prompt,
                temperature=0.7,
                system=system_prompt
            )
            return explanation.strip()
        except Exception as e:
            logger.error(f"Failed to generate explanation: {e}")
            return f"Recommended based on your interest in {history_str}"
    
    async def parse_natural_language_query(
        self,
        query: str
    ) -> Dict[str, Any]:
        """
        Parse natural language movie query into structured filters.
        
        Args:
            query: User's natural language query
        
        Returns:
            Structured filters
        """
        system_prompt = """You are a movie query parser. Convert natural language 
        queries into structured JSON filters. Extract: genres, mood, year, min_rating, 
        keywords. Return only valid JSON."""
        
        prompt = f"""Query: "{query}"

Extract filters as JSON:"""
        
        try:
            response = await self.generate(
                prompt,
                temperature=0.3,
                system=system_prompt
            )
            
            # Try to parse JSON
            try:
                filters = json.loads(response)
                return filters
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse LLM response as JSON: {response}")
                return {}
            
        except Exception as e:
            logger.error(f"Query parsing failed: {e}")
            return {}
    
    async def summarize_reviews(
        self,
        reviews: List[str],
        max_reviews: int = 10
    ) -> str:
        """
        Summarize multiple movie reviews.
        
        Args:
            reviews: List of review texts
            max_reviews: Maximum reviews to consider
        
        Returns:
            Summary text
        """
        system_prompt = """Summarize these movie reviews into a concise 
        2-3 sentence overview highlighting main points."""
        
        reviews_text = "\n\n".join(reviews[:max_reviews])
        
        prompt = f"""Reviews:
{reviews_text}

Summary:"""
        
        try:
            summary = await self.generate(
                prompt,
                temperature=0.5,
                system=system_prompt
            )
            return summary.strip()
        except Exception as e:
            logger.error(f"Review summarization failed: {e}")
            return "Multiple reviews available for this movie."
    
    async def get_conversational_recommendation(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]],
        user_profile: Dict[str, Any]
    ) -> str:
        """
        Get conversational movie recommendation.
        
        Args:
            user_message: User's message
            conversation_history: Previous messages
            user_profile: User preferences and history
        
        Returns:
            Assistant response with recommendations
        """
        system_prompt = f"""You are a knowledgeable movie recommendation assistant.
User's favorite genres: {user_profile.get('favorite_genres', [])}
User's recent watches: {user_profile.get('recent_movies', [])}

Provide personalized, conversational movie recommendations. Be friendly and concise."""
        
        messages = conversation_history + [
            {"role": "user", "content": user_message}
        ]
        
        try:
            response = await self.chat(messages, temperature=0.8)
            return response
        except Exception as e:
            logger.error(f"Conversational recommendation failed: {e}")
            return "I'd be happy to help you find a great movie! Could you tell me more about what you're in the mood for?"
    
    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()


# Singleton instance
_ollama_client = None


def get_ollama_client() -> OllamaClient:
    """Get singleton Ollama client."""
    global _ollama_client
    if _ollama_client is None:
        _ollama_client = OllamaClient()
    return _ollama_client
