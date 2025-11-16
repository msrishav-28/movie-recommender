# CineAesthete Backend - Complete Production Architecture

## 📁 Complete File Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                          # FastAPI application entry point
│   │
│   ├── core/                            # Core configuration and utilities
│   │   ├── __init__.py
│   │   ├── config.py                    # ✅ Settings and environment variables
│   │   ├── security.py                  # Password hashing, JWT tokens
│   │   ├── logging.py                   # Structured logging configuration
│   │   ├── exceptions.py                # Custom exception handlers
│   │   └── middleware.py                # Custom middleware (CORS, timing, etc.)
│   │
│   ├── db/                              # Database layer
│   │   ├── __init__.py
│   │   ├── database.py                  # ✅ Database connection and sessions
│   │   ├── models/                      # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   ├── user.py                  # User, UserProfile, UserPreferences
│   │   │   ├── movie.py                 # Movie, Genre, Cast, Crew
│   │   │   ├── rating.py                # Ratings, Reviews
│   │   │   ├── watchlist.py             # Watchlists, Lists
│   │   │   ├── social.py                # Follows, Likes, Comments
│   │   │   ├── streaming.py             # StreamingServices, Availability
│   │   │   ├── aesthetic.py             # MovieFrames, VisualTags
│   │   │   ├── interaction.py           # UserInteractions, ABTests
│   │   │   └── sentiment.py             # SentimentData, EmotionScores
│   │   ├── repositories/                # Data access layer (Repository pattern)
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── movie.py
│   │   │   ├── rating.py
│   │   │   └── recommendation.py
│   │   └── migrations/                  # Alembic migrations
│   │       └── versions/
│   │
│   ├── api/                             # API endpoints
│   │   ├── __init__.py
│   │   ├── deps.py                      # Common dependencies
│   │   ├── v1/                          # API version 1
│   │   │   ├── __init__.py
│   │   │   ├── router.py                # Main router
│   │   │   └── endpoints/
│   │   │       ├── __init__.py
│   │   │       ├── auth.py              # Authentication endpoints
│   │   │       ├── users.py             # User management
│   │   │       ├── movies.py            # Movie CRUD
│   │   │       ├── recommendations.py   # Recommendation endpoints
│   │   │       ├── aesthetic_search.py  # Semantic search
│   │   │       ├── ratings.py           # Ratings and reviews
│   │   │       ├── watchlist.py         # Watchlist management
│   │   │       ├── social.py            # Social features
│   │   │       ├── streaming.py         # Streaming availability
│   │   │       └── admin.py             # Admin endpoints
│   │   └── websocket/                   # WebSocket endpoints
│   │       ├── __init__.py
│   │       ├── connection.py
│   │       └── handlers.py
│   │
│   ├── schemas/                         # Pydantic schemas (request/response)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── movie.py
│   │   ├── rating.py
│   │   ├── recommendation.py
│   │   ├── aesthetic.py
│   │   └── common.py
│   │
│   ├── services/                        # Business logic layer
│   │   ├── __init__.py
│   │   ├── auth_service.py              # Authentication logic
│   │   ├── user_service.py              # User management logic
│   │   ├── movie_service.py             # Movie operations
│   │   ├── rating_service.py            # Rating operations
│   │   ├── watchlist_service.py         # Watchlist logic
│   │   ├── social_service.py            # Social features
│   │   └── streaming_service.py         # Streaming availability
│   │
│   ├── ml/                              # Machine Learning services
│   │   ├── __init__.py
│   │   ├── recommendation/              # Recommendation engine
│   │   │   ├── __init__.py
│   │   │   ├── hybrid_engine.py         # Main hybrid recommendation
│   │   │   ├── collaborative.py         # Collaborative filtering
│   │   │   ├── content_based.py         # Content-based filtering
│   │   │   ├── gnn_recommender.py       # Graph Neural Network
│   │   │   ├── diversity.py             # Diversity and MMR
│   │   │   └── explainer.py             # Explanation generation
│   │   ├── semantic_search/             # Aesthetic search
│   │   │   ├── __init__.py
│   │   │   ├── clip_engine.py           # CLIP-based search
│   │   │   ├── frame_extractor.py       # Video frame extraction
│   │   │   ├── color_analyzer.py        # Color palette extraction
│   │   │   ├── visual_detector.py       # Visual element detection
│   │   │   └── query_parser.py          # Natural language query parsing
│   │   ├── sentiment/                   # Sentiment analysis
│   │   │   ├── __init__.py
│   │   │   ├── analyzer.py              # Sentiment analysis engine
│   │   │   ├── emotion_detector.py      # Emotion detection
│   │   │   ├── aspect_analyzer.py       # Aspect-based sentiment
│   │   │   └── aggregator.py            # Movie sentiment aggregation
│   │   ├── llm/                         # LLM services
│   │   │   ├── __init__.py
│   │   │   ├── ollama_client.py         # Ollama integration
│   │   │   ├── conversational.py        # Conversational recommendations
│   │   │   ├── summarizer.py            # Text summarization
│   │   │   └── explainer.py             # LLM-based explanations
│   │   ├── models/                      # Model management
│   │   │   ├── __init__.py
│   │   │   ├── loader.py                # Model loading/caching
│   │   │   ├── training.py              # Model training pipelines
│   │   │   └── evaluation.py            # Model evaluation metrics
│   │   └── utils/                       # ML utilities
│   │       ├── __init__.py
│   │       ├── feature_engineering.py
│   │       ├── preprocessing.py
│   │       └── embeddings.py
│   │
│   ├── integrations/                    # External API integrations
│   │   ├── __init__.py
│   │   ├── tmdb.py                      # TMDb API client
│   │   ├── justwatch.py                 # JustWatch API
│   │   ├── imdb_scraper.py              # IMDb scraping
│   │   └── youtube.py                   # YouTube trailer download
│   │
│   ├── cache/                           # Caching layer
│   │   ├── __init__.py
│   │   ├── redis_client.py              # Redis client wrapper
│   │   ├── cache_manager.py             # Cache management
│   │   └── strategies.py                # Caching strategies
│   │
│   ├── search/                          # Search engines
│   │   ├── __init__.py
│   │   ├── elasticsearch_client.py      # Elasticsearch client
│   │   └── movie_search.py              # Movie search functionality
│   │
│   ├── vector_db/                       # Vector database clients
│   │   ├── __init__.py
│   │   ├── pinecone_client.py           # Pinecone client
│   │   └── index_manager.py             # Index management
│   │
│   ├── messaging/                       # Message queue
│   │   ├── __init__.py
│   │   ├── kafka_client.py              # Kafka producer/consumer
│   │   ├── producers.py                 # Message producers
│   │   └── consumers.py                 # Message consumers
│   │
│   ├── workers/                         # Background workers
│   │   ├── __init__.py
│   │   ├── celery_app.py                # Celery application
│   │   ├── tasks/                       # Celery tasks
│   │   │   ├── __init__.py
│   │   │   ├── data_ingestion.py        # Data ingestion tasks
│   │   │   ├── model_training.py        # Model training tasks
│   │   │   ├── sentiment_analysis.py    # Sentiment analysis tasks
│   │   │   ├── frame_extraction.py      # Frame extraction tasks
│   │   │   └── recommendation_update.py # Recommendation updates
│   │   └── schedules.py                 # Scheduled tasks
│   │
│   ├── monitoring/                      # Monitoring and observability
│   │   ├── __init__.py
│   │   ├── metrics.py                   # Prometheus metrics
│   │   ├── health.py                    # Health checks
│   │   └── profiler.py                  # Performance profiling
│   │
│   └── utils/                           # Utility functions
│       ├── __init__.py
│       ├── validators.py                # Custom validators
│       ├── helpers.py                   # Helper functions
│       ├── formatters.py                # Data formatters
│       └── constants.py                 # Application constants
│
├── tests/                               # Test suite
│   ├── __init__.py
│   ├── conftest.py                      # Pytest configuration
│   ├── unit/                            # Unit tests
│   ├── integration/                     # Integration tests
│   └── e2e/                             # End-to-end tests
│
├── scripts/                             # Utility scripts
│   ├── init_db.py                       # Database initialization
│   ├── seed_data.py                     # Seed sample data
│   ├── download_trailers.py             # Batch trailer download
│   ├── extract_frames.py                # Batch frame extraction
│   ├── train_models.py                  # ML model training
│   └── migrate_data.py                  # Data migration
│
├── models/                              # Trained ML models
│   ├── collaborative_filtering/
│   ├── content_based/
│   ├── graph_neural_network/
│   └── sentiment_analysis/
│
├── logs/                                # Application logs
│
├── docker/                              # Docker configurations
│   ├── Dockerfile
│   ├── Dockerfile.worker
│   ├── docker-compose.yml
│   └── docker-compose.prod.yml
│
├── kubernetes/                          # Kubernetes manifests
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   └── configmap.yaml
│
├── alembic/                             # Database migrations
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│
├── .env.example                         # ✅ Environment variables template
├── requirements.txt                     # ✅ Python dependencies
├── pyproject.toml                       # Project configuration
├── pytest.ini                           # Pytest configuration
├── .dockerignore
├── .gitignore
└── README.md                            # ✅ Documentation
```

## 🏗️ Architecture Components

### 1. **API Layer** (FastAPI)
- RESTful API with FastAPI
- WebSocket for real-time features
- OpenAPI/Swagger documentation
- Request validation with Pydantic
- Rate limiting and authentication

### 2. **Business Logic Layer**
- Service classes for business logic
- Repository pattern for data access
- Transaction management
- Error handling

### 3. **ML/AI Layer**
- Hybrid recommendation engine
- CLIP-based semantic search
- Sentiment analysis with BERT
- LLM integration (Ollama/Mistral)
- Graph Neural Networks

### 4. **Data Layer**
- PostgreSQL (primary database)
- Redis (caching, sessions, rate limiting)
- Pinecone (vector database)
- Elasticsearch (full-text search)

### 5. **Integration Layer**
- TMDb API client
- JustWatch API client
- IMDb scraper
- YouTube downloader

### 6. **Background Processing**
- Celery workers
- Kafka message queue
- Scheduled tasks
- Data pipelines

### 7. **Infrastructure Layer**
- Docker containers
- Kubernetes orchestration
- Prometheus monitoring
- Grafana dashboards
- Sentry error tracking

## 🔄 Data Flow

1. **User Request** → API Gateway → FastAPI Endpoint
2. **Authentication** → JWT validation → User context
3. **Business Logic** → Service Layer → Repository Layer
4. **Data Access** → Database/Cache → Response
5. **Background Tasks** → Celery → Kafka → Workers

## 📊 Recommendation Pipeline

1. **Candidate Generation** (200 candidates)
   - Collaborative filtering (40%)
   - Content-based (30%)
   - GNN (20%)
   - Trending (10%)

2. **Re-ranking** (score each candidate)
   - Collaborative score (35%)
   - Content similarity (25%)
   - GNN score (20%)
   - Sentiment boost (10%)
   - Popularity (5%)
   - Context (5%)

3. **Diversification** (MMR algorithm)
   - Prevent filter bubbles
   - Ensure genre diversity

4. **Explanation Generation** (LLM)
   - Natural language explanations
   - Feature importance

## 🎨 Aesthetic Search Pipeline

1. **Frame Extraction** (FFmpeg)
   - Extract 15 frames per trailer
   - Store in S3/CDN

2. **Embedding Generation** (CLIP)
   - Convert frames to embeddings
   - Store in Pinecone

3. **Query Processing**
   - Convert text query to embedding
   - Parse filters (color, weather, etc.)

4. **Similarity Search**
   - Find matching frames
   - Aggregate by movie
   - Rank and return

## 🔐 Security Features

- JWT authentication with refresh tokens
- Password hashing (bcrypt)
- Rate limiting per user/IP
- SQL injection prevention
- XSS protection
- CSRF tokens
- HTTPS only
- CORS configuration
- Input validation
- OAuth 2.0 support

## 📈 Monitoring & Observability

- Prometheus metrics
- Grafana dashboards
- Sentry error tracking
- Structured logging (JSON)
- Request tracing
- Performance profiling
- Health check endpoints
- Database query monitoring

## 🚀 Deployment

- Docker containerization
- Kubernetes orchestration
- Horizontal auto-scaling
- Load balancing
- Blue-green deployment
- CI/CD with GitHub Actions
- Infrastructure as Code (Terraform)

---

## Next Steps

All backend services will be implemented with:
✅ Complete functionality
✅ Production-grade code quality
✅ Comprehensive error handling
✅ Full test coverage
✅ Detailed documentation
✅ Performance optimization
✅ Security best practices
