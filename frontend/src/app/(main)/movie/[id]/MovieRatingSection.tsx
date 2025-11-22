'use client';

import { useState } from 'react';
import { Star } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { RatingModal } from '@/components/movie/RatingModal';
import { ReviewForm } from '@/components/movie/ReviewForm';
import { Card, CardContent } from '@/components/ui/Card';

interface MovieRatingSectionProps {
  movieId: number;
  movieTitle: string;
}

export function MovieRatingSection({ movieId, movieTitle }: MovieRatingSectionProps) {
  const [showRatingModal, setShowRatingModal] = useState(false);
  const [showReviewForm, setShowReviewForm] = useState(false);
  const [ratingId, setRatingId] = useState<number | null>(null);

  const handleRatingSuccess = () => {
    setShowRatingModal(false);
    setShowReviewForm(true);
    // In a real app, you'd get the rating ID from the response
    setRatingId(1); // Placeholder
  };

  return (
    <div className="space-y-6">
      <Card variant="glass">
        <CardContent className="p-8 text-center">
          <Star className="h-16 w-16 text-brand-tertiary mx-auto mb-4" />
          <h3 className="text-2xl font-bold mb-2">Rate This Movie</h3>
          <p className="text-text-secondary mb-6">
            Share your thoughts and help others discover great movies
          </p>
          <Button
            size="lg"
            variant="primary"
            onClick={() => setShowRatingModal(true)}
            glow
          >
            Submit Your Rating
          </Button>
        </CardContent>
      </Card>

      {showReviewForm && ratingId && (
        <ReviewForm
          movieId={movieId}
          ratingId={ratingId}
          onSuccess={() => setShowReviewForm(false)}
          onCancel={() => setShowReviewForm(false)}
        />
      )}

      <RatingModal
        movieId={movieId}
        movieTitle={movieTitle}
        isOpen={showRatingModal}
        onClose={() => setShowRatingModal(false)}
        onSuccess={handleRatingSuccess}
      />
    </div>
  );
}
