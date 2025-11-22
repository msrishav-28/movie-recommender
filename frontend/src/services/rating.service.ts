/**
 * Rating and Review Service
 * Handles all rating and review operations
 */

import { apiClient } from './api.client';

// Types
export interface CreateRatingRequest {
  movie_id: number;
  overall_rating: number;
  plot_rating?: number;
  acting_rating?: number;
  cinematography_rating?: number;
  soundtrack_rating?: number;
}

export interface Rating {
  id: number;
  movie_id: number;
  overall_rating: number;
  plot_rating?: number;
  acting_rating?: number;
  cinematography_rating?: number;
  soundtrack_rating?: number;
  created_at: string;
}

export interface CreateReviewRequest {
  movie_id: number;
  rating_id: number;
  title?: string;
  content: string;
  is_spoiler: boolean;
}

export interface Review {
  id: number;
  movie_id: number;
  user_id: string;
  title?: string;
  content: string;
  sentiment_score?: number;
  sentiment_label?: string;
  is_spoiler: boolean;
  likes_count: number;
  created_at: string;
  user?: {
    username: string;
    avatar_url?: string;
  };
}

export const ratingService = {
  /**
   * Rate a movie (create or update rating)
   */
  async rateMovie(data: CreateRatingRequest): Promise<Rating> {
    const response = await apiClient.post('/ratings/rate', data);
    return response.data;
  },

  /**
   * Get current user's ratings
   */
  async getMyRatings(page: number = 1, pageSize: number = 20): Promise<Rating[]> {
    const response = await apiClient.get('/ratings/my-ratings', {
      params: { page, page_size: pageSize },
    });
    return response.data;
  },

  /**
   * Create a review for a movie
   */
  async createReview(data: CreateReviewRequest): Promise<Review> {
    const response = await apiClient.post('/ratings/review', data);
    return response.data;
  },

  /**
   * Get reviews for a movie
   */
  async getMovieReviews(
    movieId: number,
    page: number = 1,
    pageSize: number = 20
  ): Promise<Review[]> {
    const response = await apiClient.get(`/ratings/movie/${movieId}/reviews`, {
      params: { page, page_size: pageSize },
    });
    return response.data;
  },

  /**
   * Like a review
   */
  async likeReview(reviewId: number): Promise<void> {
    await apiClient.post(`/ratings/review/${reviewId}/like`);
  },

  /**
   * Delete a rating
   */
  async deleteRating(ratingId: number): Promise<void> {
    await apiClient.delete(`/ratings/${ratingId}`);
  },
};
