'use client';

import { useState, useEffect } from 'react';
import { MessageSquare, Loader } from 'lucide-react';
import { ReviewCard } from './ReviewCard';
import { Button } from '@/components/ui/Button';
import { ratingService, Review } from '@/services/rating.service';

interface ReviewListProps {
  movieId: number;
}

export function ReviewList({ movieId }: ReviewListProps) {
  const [reviews, setReviews] = useState<Review[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);

  useEffect(() => {
    loadReviews();
  }, [movieId, page]);

  const loadReviews = async () => {
    try {
      setIsLoading(true);
      const data = await ratingService.getMovieReviews(movieId, page, 10);
      
      if (page === 1) {
        setReviews(data);
      } else {
        setReviews((prev) => [...prev, ...data]);
      }
      
      setHasMore(data.length === 10);
    } catch (error) {
      console.error('Failed to load reviews:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLikeReview = async (reviewId: number) => {
    try {
      await ratingService.likeReview(reviewId);
      // Refresh reviews
      loadReviews();
    } catch (error) {
      console.error('Failed to like review:', error);
    }
  };

  if (isLoading && page === 1) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader className="h-8 w-8 animate-spin text-brand-primary" />
      </div>
    );
  }

  if (reviews.length === 0) {
    return (
      <div className="text-center py-12">
        <MessageSquare className="h-12 w-12 text-text-tertiary mx-auto mb-4" />
        <p className="text-text-secondary">No reviews yet. Be the first to review!</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {reviews.map((review) => (
        <ReviewCard
          key={review.id}
          review={review}
          onLike={() => handleLikeReview(review.id)}
        />
      ))}

      {hasMore && (
        <div className="flex justify-center pt-4">
          <Button
            variant="outline"
            onClick={() => setPage((p) => p + 1)}
            loading={isLoading}
          >
            Load More Reviews
          </Button>
        </div>
      )}
    </div>
  );
}
