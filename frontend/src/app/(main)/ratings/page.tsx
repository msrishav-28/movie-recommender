'use client';

import { useState, useEffect } from 'react';
import { Star, Loader, Trash2 } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { ratingService, Rating } from '@/services/rating.service';
import { formatDate } from '@/lib/utils';
import { toast } from 'sonner';

export default function MyRatingsPage() {
  const [ratings, setRatings] = useState<Rating[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [page, setPage] = useState(1);

  useEffect(() => {
    loadRatings();
  }, [page]);

  const loadRatings = async () => {
    try {
      setIsLoading(true);
      const data = await ratingService.getMyRatings(page, 20);
      setRatings(data);
    } catch (error) {
      toast.error('Failed to load ratings');
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteRating = async (ratingId: number) => {
    if (!confirm('Are you sure you want to delete this rating?')) return;

    try {
      await ratingService.deleteRating(ratingId);
      toast.success('Rating deleted');
      loadRatings();
    } catch (error) {
      toast.error('Failed to delete rating');
      console.error(error);
    }
  };

  if (isLoading && page === 1) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader className="h-8 w-8 animate-spin text-brand-primary" />
      </div>
    );
  }

  return (
    <div className="min-h-screen section-spacing">
      <div className="container-padding">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">My Ratings</h1>
          <p className="text-text-secondary">
            All movies you've rated ({ratings.length})
          </p>
        </div>

        {/* Ratings Grid */}
        {ratings.length === 0 ? (
          <Card variant="glass">
            <CardContent className="p-12 text-center">
              <Star className="h-16 w-16 text-text-tertiary mx-auto mb-4" />
              <h3 className="text-xl font-semibold mb-2">No ratings yet</h3>
              <p className="text-text-secondary">
                Start rating movies to see them here
              </p>
            </CardContent>
          </Card>
        ) : (
          <div className="grid grid-cols-1 gap-4">
            {ratings.map((rating) => (
              <Card key={rating.id} variant="glass">
                <CardContent className="p-6">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-3">
                        <div className="flex items-center gap-2">
                          <Star className="h-6 w-6 fill-brand-tertiary text-brand-tertiary" />
                          <span className="text-2xl font-bold">
                            {rating.overall_rating.toFixed(1)}
                          </span>
                        </div>
                        <span className="text-text-tertiary">/</span>
                        <span className="text-text-tertiary">5.0</span>
                      </div>

                      <p className="text-sm text-text-tertiary">
                        Rated {formatDate(rating.created_at, 'short')}
                      </p>

                      {/* Detailed Ratings */}
                      {(rating.plot_rating ||
                        rating.acting_rating ||
                        rating.cinematography_rating ||
                        rating.soundtrack_rating) && (
                        <div className="flex flex-wrap gap-2 mt-4">
                          {rating.plot_rating && (
                            <Badge variant="default">
                              Plot: {rating.plot_rating.toFixed(1)}
                            </Badge>
                          )}
                          {rating.acting_rating && (
                            <Badge variant="default">
                              Acting: {rating.acting_rating.toFixed(1)}
                            </Badge>
                          )}
                          {rating.cinematography_rating && (
                            <Badge variant="default">
                              Cinematography: {rating.cinematography_rating.toFixed(1)}
                            </Badge>
                          )}
                          {rating.soundtrack_rating && (
                            <Badge variant="default">
                              Soundtrack: {rating.soundtrack_rating.toFixed(1)}
                            </Badge>
                          )}
                        </div>
                      )}
                    </div>

                    <Button
                      variant="ghost"
                      size="sm"
                      icon={<Trash2 className="h-4 w-4" />}
                      onClick={() => handleDeleteRating(rating.id)}
                    >
                      Delete
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
