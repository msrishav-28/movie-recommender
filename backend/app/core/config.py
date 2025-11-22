"""
Core configuration module for CineAesthete backend.
Handles all environment variables and application settings.
"""

from typing import List, Optional
from pydantic import Field, validator, AnyHttpUrl
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings from environment variables."""
    
    # Application
    APP_NAME: str = "CineAesthete"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "production"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_PREFIX: str = "/api/v1"
    CORS_ORIGINS: List[str] = ["https://cineaesthete.com"]
    ALLOWED_HOSTS: List[str] = ["cineaesthete.com", "*.cineaesthete.com"]
    
    # Database - PostgreSQL
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 40
    DATABASE_POOL_TIMEOUT: int = 30
    DATABASE_ECHO: bool = False
    
    # Redis
    REDIS_URL: str
    REDIS_DB_SESSIONS: int = 0
    REDIS_DB_CACHE: int = 1
    REDIS_DB_RATE_LIMIT: int = 2
    REDIS_DB_REALTIME: int = 3
    REDIS_DB_CELERY: int = 4
    REDIS_MAX_CONNECTIONS: int = 50
    REDIS_SOCKET_TIMEOUT: int = 5
    REDIS_SOCKET_CONNECT_TIMEOUT: int = 5
    
    # Security & Authentication
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    PASSWORD_MIN_LENGTH: int = 8
    MAX_LOGIN_ATTEMPTS: int = 5
    LOGIN_ATTEMPT_WINDOW_MINUTES: int = 15
    
    # OAuth
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    GITHUB_CLIENT_ID: Optional[str] = None
    GITHUB_CLIENT_SECRET: Optional[str] = None
    OAUTH_REDIRECT_URI: Optional[str] = None
    
    # Email
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM: str = "noreply@cineaesthete.com"
    SMTP_TLS: bool = True
    
    # External APIs
    TMDB_API_KEY: str
    TMDB_BASE_URL: str = "https://api.themoviedb.org/3"
    TMDB_RATE_LIMIT: int = 40
    JUSTWATCH_API_KEY: Optional[str] = None
    OMDB_API_KEY: Optional[str] = None
    
    # Vector Databases
    PINECONE_API_KEY: str
    PINECONE_ENVIRONMENT: str = "us-east-1-aws"
    PINECONE_INDEX_AESTHETIC: str = "movie-aesthetic-search"
    PINECONE_INDEX_CONTENT: str = "movie-content-embeddings"
    PINECONE_INDEX_USER: str = "user-embeddings"
    PINECONE_DIMENSION: int = 512
    PINECONE_METRIC: str = "cosine"
    
    # Elasticsearch
    ELASTICSEARCH_URL: str
    ELASTICSEARCH_USER: str = "elastic"
    ELASTICSEARCH_PASSWORD: str
    ELASTICSEARCH_INDEX_MOVIES: str = "movies"
    ELASTICSEARCH_INDEX_REVIEWS: str = "reviews"
    
    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9092"
    KAFKA_TOPIC_USER_INTERACTIONS: str = "user-interactions"
    KAFKA_TOPIC_RECOMMENDATIONS: str = "recommendations"
    KAFKA_TOPIC_SENTIMENT: str = "sentiment-analysis"
    KAFKA_CONSUMER_GROUP: str = "cineaesthete-consumers"
    
    # Celery
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    CELERY_TASK_SERIALIZER: str = "json"
    CELERY_RESULT_SERIALIZER: str = "json"
    CELERY_ACCEPT_CONTENT: List[str] = ["json"]
    CELERY_TIMEZONE: str = "UTC"
    CELERY_ENABLE_UTC: bool = True
    CELERY_TASK_TRACK_STARTED: bool = True
    CELERY_TASK_TIME_LIMIT: int = 300
    CELERY_TASK_SOFT_TIME_LIMIT: int = 240
    
    # ML Models
    MODEL_COLLABORATIVE_PATH: str = "models/collaborative_filtering"
    MODEL_CONTENT_PATH: str = "models/content_based"
    MODEL_GNN_PATH: str = "models/graph_neural_network"
    MODEL_SENTIMENT_PATH: str = "models/sentiment_analysis"
    MODEL_CLIP_PATH: str = "openai/clip-vit-large-patch14"
    MODEL_BERT_PATH: str = "distilbert-base-uncased"
    MODEL_EMOTION_PATH: str = "j-hartmann/emotion-english-distilroberta-base"
    
    # LLM
    OLLAMA_HOST: str = "http://ollama:11434"
    OLLAMA_MODEL: str = "mistral:7b-instruct"
    OLLAMA_TIMEOUT: int = 60
    OLLAMA_NUM_CTX: int = 4096
    OLLAMA_TEMPERATURE: float = 0.7
    
    # Recommendation Engine
    REC_CANDIDATE_POOL_SIZE: int = 200
    REC_FINAL_RESULTS: int = 20
    REC_COLLABORATIVE_WEIGHT: float = 0.35
    REC_CONTENT_WEIGHT: float = 0.25
    REC_GNN_WEIGHT: float = 0.20
    REC_SENTIMENT_WEIGHT: float = 0.10
    REC_POPULARITY_WEIGHT: float = 0.05
    REC_CONTEXT_WEIGHT: float = 0.05
    REC_DIVERSITY_LAMBDA: float = 0.7
    REC_CACHE_TTL: int = 3600
    GNN_EMBEDDING_DIM: int = 128
    LLM_EXPLANATIONS_ENABLED: bool = True
    
    # Aesthetic Search
    AESTHETIC_FRAMES_PER_MOVIE: int = 15
    AESTHETIC_FPS: float = 0.333
    AESTHETIC_SEARCH_TOP_K: int = 50
    AESTHETIC_MIN_SCORE: float = 0.3
    AESTHETIC_COLOR_TOLERANCE: float = 0.1
    
    # Sentiment Analysis
    SENTIMENT_BATCH_SIZE: int = 32
    SENTIMENT_MAX_LENGTH: int = 512
    SENTIMENT_THRESHOLD_POSITIVE: float = 0.2
    SENTIMENT_THRESHOLD_NEGATIVE: float = -0.2
    SENTIMENT_UPDATE_INTERVAL_HOURS: int = 24
    
    # Caching Strategy
    CACHE_DEFAULT_TTL: int = 3600
    CACHE_USER_PROFILE_TTL: int = 1800
    CACHE_MOVIE_DETAILS_TTL: int = 86400
    CACHE_RECOMMENDATIONS_TTL: int = 3600
    CACHE_SEARCH_RESULTS_TTL: int = 1800
    CACHE_TRENDING_TTL: int = 300
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    RATE_LIMIT_BURST: int = 10
    
    # Monitoring
    PROMETHEUS_PORT: int = 9090
    GRAFANA_PORT: int = 3000
    SENTRY_DSN: Optional[str] = None
    SENTRY_TRACES_SAMPLE_RATE: float = 0.1
    SENTRY_ENVIRONMENT: str = "production"
    
    # Logging
    LOG_FORMAT: str = "json"
    LOG_FILE: str = "logs/cineaesthete.log"
    LOG_ROTATION: str = "daily"
    LOG_RETENTION_DAYS: int = 30
    
    # S3/Object Storage
    S3_BUCKET: str = "cineaesthete-media"
    S3_REGION: str = "us-east-1"
    S3_ACCESS_KEY: Optional[str] = None
    S3_SECRET_KEY: Optional[str] = None
    S3_ENDPOINT_URL: str = "https://s3.amazonaws.com"
    CDN_URL: str = "https://cdn.cineaesthete.com"
    
    # A/B Testing
    AB_TESTING_ENABLED: bool = True
    AB_TEST_SAMPLE_RATE: float = 0.1
    
    # Feature Flags
    FEATURE_GNN_ENABLED: bool = True
    FEATURE_LLM_ENABLED: bool = True
    FEATURE_SOCIAL_ENABLED: bool = True
    FEATURE_REALTIME_ENABLED: bool = True
    
    # Performance
    WORKER_COUNT: int = 4
    MAX_CONCURRENT_REQUESTS: int = 1000
    REQUEST_TIMEOUT: int = 30
    KEEPALIVE_TIMEOUT: int = 5
    
    # Data Processing
    DATA_INGESTION_BATCH_SIZE: int = 1000
    DATA_UPDATE_INTERVAL_HOURS: int = 24
    TRAILER_DOWNLOAD_WORKERS: int = 5
    FRAME_EXTRACTION_WORKERS: int = 10
    
    # Model Training
    TRAINING_BATCH_SIZE: int = 256
    TRAINING_EPOCHS: int = 50
    TRAINING_LEARNING_RATE: float = 0.001
    TRAINING_VALIDATION_SPLIT: float = 0.2
    TRAINING_EARLY_STOPPING_PATIENCE: int = 5
    
    # Development
    RELOAD: bool = False
    WORKERS: int = 4
    
    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    @validator("ALLOWED_HOSTS", pre=True)
    def assemble_allowed_hosts(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    @validator("CELERY_ACCEPT_CONTENT", pre=True)
    def assemble_celery_content(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached application settings.
    This is cached to avoid reading .env file multiple times.
    """
    return Settings()


# Export settings instance
settings = get_settings()
