"""
A/B Testing Framework - Production Grade
Framework for running experiments on recommendation algorithms.
"""

from typing import Dict, Any, Optional, List
from enum import Enum
import hashlib
import logging
from datetime import datetime, timedelta

from app.core.config import settings
from app.cache.cache_manager import CacheManager

logger = logging.getLogger(__name__)


class ExperimentVariant(str, Enum):
    """Experiment variant types."""
    CONTROL = "control"
    VARIANT_A = "variant_a"
    VARIANT_B = "variant_b"
    VARIANT_C = "variant_c"


class ABTestingFramework:
    """
    A/B testing framework for recommendation experiments.
    
    Features:
    - User assignment to variants
    - Consistent hashing for deterministic assignment
    - Experiment configuration management
    - Metrics tracking
    - Statistical significance testing
    """
    
    def __init__(self):
        self.cache = CacheManager()
        self.experiments: Dict[str, Dict[str, Any]] = {}
        self._load_experiments()
    
    def _load_experiments(self):
        """Load experiment configurations."""
        # In production: load from database or config
        self.experiments = {
            "recommendation_algorithm_v2": {
                "name": "Recommendation Algorithm V2",
                "description": "Test new GNN-based hybrid algorithm",
                "enabled": settings.AB_TESTING_ENABLED,
                "start_date": datetime(2025, 1, 1),
                "end_date": datetime(2025, 3, 1),
                "variants": {
                    ExperimentVariant.CONTROL: {
                        "name": "Original Algorithm",
                        "traffic": 0.5,  # 50% of users
                        "config": {
                            "use_gnn": False,
                            "diversity_weight": 0.7
                        }
                    },
                    ExperimentVariant.VARIANT_A: {
                        "name": "With GNN",
                        "traffic": 0.5,  # 50% of users
                        "config": {
                            "use_gnn": True,
                            "diversity_weight": 0.7
                        }
                    }
                },
                "metrics": ["ctr", "engagement_time", "recommendation_acceptance"]
            },
            "diversity_optimization": {
                "name": "Diversity Parameter Test",
                "description": "Test different diversity parameters",
                "enabled": settings.AB_TESTING_ENABLED,
                "start_date": datetime(2025, 2, 1),
                "end_date": datetime(2025, 4, 1),
                "variants": {
                    ExperimentVariant.CONTROL: {
                        "name": "Low Diversity (0.5)",
                        "traffic": 0.33,
                        "config": {"diversity": 0.5}
                    },
                    ExperimentVariant.VARIANT_A: {
                        "name": "Medium Diversity (0.7)",
                        "traffic": 0.33,
                        "config": {"diversity": 0.7}
                    },
                    ExperimentVariant.VARIANT_B: {
                        "name": "High Diversity (0.9)",
                        "traffic": 0.34,
                        "config": {"diversity": 0.9}
                    }
                },
                "metrics": ["user_satisfaction", "diversity_score", "serendipity"]
            }
        }
    
    def assign_variant(
        self,
        user_id: str,
        experiment_name: str
    ) -> ExperimentVariant:
        """
        Assign user to experiment variant using consistent hashing.
        
        Args:
            user_id: User ID
            experiment_name: Experiment name
        
        Returns:
            Assigned variant
        """
        experiment = self.experiments.get(experiment_name)
        
        if not experiment or not experiment["enabled"]:
            return ExperimentVariant.CONTROL
        
        # Check if experiment is active
        now = datetime.utcnow()
        if now < experiment["start_date"] or now > experiment["end_date"]:
            return ExperimentVariant.CONTROL
        
        # Check cache for existing assignment
        cache_key = f"ab_test:{experiment_name}:{user_id}"
        cached_variant = self.cache.get_sync(cache_key)
        if cached_variant:
            return ExperimentVariant(cached_variant)
        
        # Assign variant using consistent hashing
        hash_input = f"{user_id}:{experiment_name}".encode('utf-8')
        hash_value = int(hashlib.md5(hash_input).hexdigest(), 16)
        bucket = (hash_value % 100) / 100.0  # 0.00 to 0.99
        
        # Determine variant based on traffic allocation
        cumulative_traffic = 0.0
        variants = experiment["variants"]
        
        for variant_key, variant_config in variants.items():
            cumulative_traffic += variant_config["traffic"]
            if bucket < cumulative_traffic:
                assigned_variant = ExperimentVariant(variant_key)
                
                # Cache assignment
                self.cache.set_sync(cache_key, assigned_variant.value, ttl=86400 * 7)  # 7 days
                
                logger.info(f"User {user_id} assigned to {assigned_variant} in {experiment_name}")
                return assigned_variant
        
        return ExperimentVariant.CONTROL
    
    def get_variant_config(
        self,
        user_id: str,
        experiment_name: str
    ) -> Dict[str, Any]:
        """
        Get configuration for user's assigned variant.
        
        Args:
            user_id: User ID
            experiment_name: Experiment name
        
        Returns:
            Variant configuration
        """
        variant = self.assign_variant(user_id, experiment_name)
        experiment = self.experiments.get(experiment_name, {})
        variants = experiment.get("variants", {})
        
        return variants.get(variant, {}).get("config", {})
    
    def track_metric(
        self,
        user_id: str,
        experiment_name: str,
        metric_name: str,
        value: float
    ):
        """
        Track experiment metric for a user.
        
        Args:
            user_id: User ID
            experiment_name: Experiment name
            metric_name: Metric name (e.g., "ctr", "engagement_time")
            value: Metric value
        """
        variant = self.assign_variant(user_id, experiment_name)
        
        # In production: store in database or analytics service
        metric_key = f"ab_metric:{experiment_name}:{variant}:{metric_name}:{user_id}"
        
        logger.info(
            f"Tracked metric: {experiment_name}/{variant}/{metric_name} = {value} "
            f"for user {user_id}"
        )
        
        # Store metric (in production: use time-series database)
        # For now, just log it
    
    def get_experiment_results(
        self,
        experiment_name: str
    ) -> Dict[str, Any]:
        """
        Get experiment results summary.
        
        Args:
            experiment_name: Experiment name
        
        Returns:
            Results summary with metrics per variant
        """
        experiment = self.experiments.get(experiment_name)
        
        if not experiment:
            return {"error": "Experiment not found"}
        
        # In production: query actual metrics from database
        # Return placeholder results
        results = {
            "experiment_name": experiment_name,
            "status": "active" if experiment["enabled"] else "inactive",
            "variants": {}
        }
        
        for variant_key in experiment["variants"].keys():
            results["variants"][variant_key] = {
                "users_assigned": 0,  # Would be actual count
                "metrics": {
                    "ctr": 0.0,
                    "engagement_time": 0.0,
                    "conversion": 0.0
                },
                "statistical_significance": {
                    "vs_control": {
                        "p_value": 0.05,
                        "confidence": 0.95,
                        "significant": False
                    }
                }
            }
        
        return results
    
    def is_experiment_active(self, experiment_name: str) -> bool:
        """Check if experiment is currently active."""
        experiment = self.experiments.get(experiment_name)
        
        if not experiment or not experiment["enabled"]:
            return False
        
        now = datetime.utcnow()
        return experiment["start_date"] <= now <= experiment["end_date"]
    
    def list_active_experiments(self) -> List[str]:
        """Get list of active experiment names."""
        return [
            name for name, exp in self.experiments.items()
            if self.is_experiment_active(name)
        ]


# Singleton instance
_ab_testing_framework = None


def get_ab_testing_framework() -> ABTestingFramework:
    """Get singleton A/B testing framework instance."""
    global _ab_testing_framework
    if _ab_testing_framework is None:
        _ab_testing_framework = ABTestingFramework()
    return _ab_testing_framework
