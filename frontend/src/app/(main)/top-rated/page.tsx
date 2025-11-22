'use client';

import { Star } from 'lucide-react';
import { MovieGrid } from '@/components/movie/MovieGrid';
import { useTopRatedMovies } from '@/hooks/useMovies';
import { useState } from 'react';
import { Button } from '@/components/ui/Button';

export default function TopRatedPage() {
  const [page, setPage] = useState(1);
  const { data, isLoading } = useTopRatedMovies(page, 24);

  return (
    <div className="min-h-screen">
      <section className="bg-gradient-mesh py-12">
        <div className="container-padding">
          <div className="flex items-center gap-3 mb-4">
            <Star className="h-10 w-10 text-brand-tertiary fill-current" />
            <h1 className="text-5xl font-bold">Top Rated Movies</h1>
          </div>
          <p className="text-xl text-text-secondary">
            Highest rated movies of all time
          </p>
        </div>
      </section>

      <section className="section-spacing">
        <div className="container-padding">
          <MovieGrid movies={data?.items || []} isLoading={isLoading} />

          {data && page < data.total_pages && (
            <div className="flex justify-center mt-12">
              <Button variant="outline" size="lg" onClick={() => setPage(page + 1)}>
                Load More
              </Button>
            </div>
          )}
        </div>
      </section>
    </div>
  );
}
