import { apiClient } from './api.client';
import type { Recommendation, Movie, PaginatedResponse } from '@/types';

/**
 * Recommendation Service
 */
export const recommendationService = {
  /**
   * Get personalized recommendations
   */
  async getRecommendations(
    limit: number = 24,
    diversityWeight: number = 0.3
  ): Promise<Recommendation[]> {
    return apiClient.get<Recommendation[]>(
      `/recommendations?limit=${limit}&diversity_weight=${diversityWeight}`
    );
  },

  /**
   * Get similar movies
   */
  async getSimilarMovies(movieId: number, limit: number = 12): Promise<Movie[]> {
    return apiClient.get<Movie[]>(`/recommendations/similar/${movieId}?limit=${limit}`);
  },

  /**
   * Get recommendations based on aesthetic/vibe
   */
  async getAestheticRecommendations(
    query: string,
    limit: number = 24
  ): Promise<Recommendation[]> {
    return apiClient.post<Recommendation[]>('/recommendations/aesthetic', {
      query,
      limit,
    });
  },

  /**
   * Get recommendations for cold start users
   */
  async getColdStartRecommendations(preferences: any): Promise<Recommendation[]> {
    return apiClient.post<Recommendation[]>('/recommendations/cold-start', preferences);
  },

  /**
   * Provide feedback on recommendation
   */
  async provideFeedback(
    movieId: number,
    feedback: 'positive' | 'negative',
    reason?: string
  ): Promise<void> {
    await apiClient.post('/recommendations/feedback', {
      movie_id: movieId,
      feedback,
      reason,
    });
  },

  /**
   * Get explanation for why a movie was recommended
   */
  async getExplanation(movieId: number): Promise<{ explanation: string; reasons: string[] }> {
    return apiClient.get(`/recommendations/explain/${movieId}`);
  },
};
