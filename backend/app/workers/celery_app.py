"""
Celery application for background task processing.
"""

from celery import Celery
from celery.schedules import crontab
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

# Create Celery app
celery_app = Celery(
    "cineaesthete",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        'app.workers.tasks.data_ingestion',
        'app.workers.tasks.sentiment_analysis',
        'app.workers.tasks.model_training',
        'app.workers.tasks.frame_extraction',
        'app.workers.tasks.recommendation_update'
    ]
)

# Configure Celery
celery_app.conf.update(
    task_serializer=settings.CELERY_TASK_SERIALIZER,
    result_serializer=settings.CELERY_RESULT_SERIALIZER,
    accept_content=settings.CELERY_ACCEPT_CONTENT,
    timezone=settings.CELERY_TIMEZONE,
    enable_utc=settings.CELERY_ENABLE_UTC,
    task_track_started=settings.CELERY_TASK_TRACK_STARTED,
    task_time_limit=settings.CELERY_TASK_TIME_LIMIT,
    task_soft_time_limit=settings.CELERY_TASK_SOFT_TIME_LIMIT,
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

# Periodic task schedule
celery_app.conf.beat_schedule = {
    # Update movie data from TMDb every 24 hours
    'update-movie-data': {
        'task': 'app.workers.tasks.data_ingestion.update_movie_data',
        'schedule': crontab(hour=2, minute=0),  # 2 AM daily
    },
    # Analyze new reviews every hour
    'analyze-reviews': {
        'task': 'app.workers.tasks.sentiment_analysis.analyze_pending_reviews',
        'schedule': crontab(minute=0),  # Every hour
    },
    # Retrain recommendation models weekly
    'retrain-models': {
        'task': 'app.workers.tasks.model_training.retrain_all_models',
        'schedule': crontab(hour=3, minute=0, day_of_week=0),  # Sunday 3 AM
    },
    # Update user recommendations daily
    'update-recommendations': {
        'task': 'app.workers.tasks.recommendation_update.update_all_user_recommendations',
        'schedule': crontab(hour=4, minute=0),  # 4 AM daily
    },
}

logger.info("Celery app configured")
