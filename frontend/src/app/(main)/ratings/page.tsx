'use client';

import { useState, useEffect } from 'react';
import { Star, Loader } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/Card';
import { MasonryGrid } from '@/components/ui/MasonryGrid';
import { Dropdown } from '@/components/ui/Dropdown';
import { ratingService, Rating } from '@/services/rating.service';
import { toast } from 'sonner';

export default function MyRatingsPage() {
  const [ratings, setRatings] = useState<Rating[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [sortBy, setSortBy] = useState<'recent' | 'rating_high' | 'rating_low'>('recent');

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

  // Sort ratings
  const sortedRatings = [...ratings].sort((a, b) => {
    if (sortBy === 'rating_high') return b.overall_rating - a.overall_rating;
    if (sortBy === 'rating_low') return a.overall_rating - b.overall_rating;
    return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
  });

  const ratedMovies = sortedRatings.map(r => {
    if (!r.movie) return undefined;

    // We augment the movie with the user's rating for display purposes if needed
    // But for now MasonryGrid just takes standard Movie objects.
    // We could use the matchScore prop to show rating? 
    // matchScore is usually 0-100. overall_rating is 0-5.
    // Let's multiply by 20 to map 5 -> 100.
    return {
      ...r.movie,
      match_score: r.overall_rating * 20
    };
  }).filter((m): m is NonNullable<typeof m> => m !== undefined);

  if (isLoading && page === 1) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader className="h-8 w-8 animate-spin text-klein-blue" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-void">
      <section className="bg-void/80 border-b border-white/5 backdrop-blur-md sticky top-[64px] z-30 shadow-lg">
        <div className="container-padding py-6">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4 mb-6">
            <div>
              <h1 className="text-3xl md:text-4xl font-bold mb-2 font-headline leading-none">My Ratings</h1>
              <p className="text-text-secondary font-mono text-sm">
                {ratings.length} movies evaluated
              </p>
            </div>

            <div className="w-48">
              <Dropdown
                label="Sort By"
                options={[
                  { value: 'recent', label: 'Most Recent' },
                  { value: 'rating_high', label: 'Highest Rated' },
                  { value: 'rating_low', label: 'Lowest Rated' },
                ]}
                value={sortBy}
                onChange={(val) => setSortBy(val as any)}
              />
            </div>
          </div>
        </div>
      </section>

      <section className="section-spacing">
        <div className="container-padding">
          {ratedMovies.length > 0 ? (
            // Use MasonryGrid. We pass match_score (mapped from rating) to show it on the card.
            // MasonryGrid handles objects with match_score.
            <MasonryGrid items={ratedMovies} />
          ) : (
            <Card variant="glass">
              <CardContent className="p-12 text-center">
                <Star className="h-16 w-16 text-white/40 mx-auto mb-4" />
                <h3 className="text-xl font-semibold mb-2">No ratings yet</h3>
                <p className="text-text-secondary">
                  Start rating movies to see them here
                </p>
              </CardContent>
            </Card>
          )}
        </div>
      </section>
    </div>
  );
}
