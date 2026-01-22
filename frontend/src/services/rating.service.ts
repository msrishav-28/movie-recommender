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
  movie?: import('@/types').Movie;
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
    return await apiClient.post<Rating>('/ratings/rate', data);
  },

  /**
   * Get current user's ratings
   */
  async getMyRatings(page: number = 1, pageSize: number = 20): Promise<Rating[]> {
    return await apiClient.get<Rating[]>('/ratings/my-ratings', {
      params: { page, page_size: pageSize },
    });
  },

  /**
   * Create a review for a movie
   */
  async createReview(data: CreateReviewRequest): Promise<Review> {
    return await apiClient.post<Review>('/ratings/review', data);
  },

  /**
   * Get reviews for a movie
   */
  async getMovieReviews(
    movieId: number,
    page: number = 1,
    pageSize: number = 20
  ): Promise<Review[]> {
    return await apiClient.get<Review[]>(`/ratings/movie/${movieId}/reviews`, {
      params: { page, page_size: pageSize },
    });
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
