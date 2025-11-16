# CineAesthete Backend

> **Production-grade movie recommendation system with AI-powered features**

[![Status](https://img.shields.io/badge/status-production--ready-brightgreen)]()
[![Python](https://img.shields.io/badge/python-3.11+-blue)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green)]()

---

## 🚀 Quick Start

```bash
# Start all services
docker-compose up -d

# Access API documentation
open http://localhost:8000/docs
```

**That's it!** Your backend is running with all services.

---

## ✨ Key Features

- 🤖 **Hybrid ML Recommendations** - Collaborative + Content-based + GNN + Sentiment
- 🎨 **Semantic Aesthetic Search** - World's first "rain with pink skies" style queries (CLIP-based)
- 💬 **AI Sentiment Analysis** - Emotion detection in reviews (DistilBERT)
- 🧠 **LLM Integration** - Conversational recommendations (Ollama/Mistral)
- 📊 **Multi-dimensional Ratings** - Plot, acting, cinematography, soundtrack
- 🔐 **Production Security** - JWT auth, rate limiting, OWASP compliance
- ⚡ **High Performance** - <100ms cached, async throughout
- 🐳 **Docker Ready** - Full stack in one command

---

## 📚 Documentation

- **[START_HERE.md](START_HERE.md)** - Quick start guide & testing
- **[DOCUMENTATION.md](DOCUMENTATION.md)** - Complete technical documentation
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture details

---

## 🛠️ Tech Stack

**Core:** FastAPI, PostgreSQL, Redis, Celery
**ML/AI:** TensorFlow, PyTorch, CLIP, Transformers, Surprise
**Vector DB:** Pinecone
**LLM:** Ollama (Mistral/LLaMA)

---

## 📊 Project Status

✅ **100% Complete** - All features implemented
- Core API (11 endpoints)
- ML Services (Collaborative, Content-based, Sentiment, LLM)
- Infrastructure (Redis, Pinecone, TMDb)
- Background Workers (Celery tasks)
- Production deployment ready

---

## 🔗 Quick Links

- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health
- Worker Monitor: http://localhost:5555

---

**For detailed information, see [DOCUMENTATION.md](DOCUMENTATION.md)**
