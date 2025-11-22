/**
 * Ratings and Reviews Hook
 * React Query hooks for managing ratings and reviews
 */

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { ratingService, Rating, Review, CreateRatingRequest, CreateReviewRequest } from '@/services/rating.service';
import { toast } from 'sonner';

/**
 * Hook to get user's ratings
 */
export function useMyRatings(page: number = 1, pageSize: number = 20) {
  return useQuery({
    queryKey: ['ratings', 'my', page, pageSize],
    queryFn: () => ratingService.getMyRatings(page, pageSize),
  });
}

/**
 * Hook to get movie reviews
 */
export function useMovieReviews(movieId: number, page: number = 1, pageSize: number = 20) {
  return useQuery({
    queryKey: ['reviews', 'movie', movieId, page, pageSize],
    queryFn: () => ratingService.getMovieReviews(movieId, page, pageSize),
    enabled: !!movieId,
  });
}

/**
 * Hook to rate a movie
 */
export function useRateMovie() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateRatingRequest) => ratingService.rateMovie(data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['ratings', 'my'] });
      queryClient.invalidateQueries({ queryKey: ['movies', variables.movie_id] });
      toast.success('Rating submitted successfully!');
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to submit rating');
    },
  });
}

/**
 * Hook to create a review
 */
export function useCreateReview() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateReviewRequest) => ratingService.createReview(data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['reviews', 'movie', variables.movie_id] });
      toast.success('Review posted successfully!');
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to post review');
    },
  });
}

/**
 * Hook to like a review
 */
export function useLikeReview() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (reviewId: number) => ratingService.likeReview(reviewId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['reviews'] });
    },
    onError: (error: any) => {
      toast.error('Failed to like review');
    },
  });
}

/**
 * Hook to delete a rating
 */
export function useDeleteRating() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (ratingId: number) => ratingService.deleteRating(ratingId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['ratings', 'my'] });
      toast.success('Rating deleted');
    },
    onError: (error: any) => {
      toast.error('Failed to delete rating');
    },
  });
}
