import { useState } from 'react';
import type { Movie } from '@/types';
import { MovieCard, MovieCardSkeleton } from './MovieCard';

interface MovieGridProps {
  movies: Movie[];
  isLoading?: boolean;
  size?: 'small' | 'medium' | 'large';
  showQuickActions?: boolean;
  onWatchlistToggle?: (movieId: number) => void;
  watchlistMovieIds?: Set<number>;
}

export function MovieGrid({
  movies,
  isLoading = false,
  size = 'medium',
  showQuickActions = true,
  onWatchlistToggle,
  watchlistMovieIds = new Set(),
}: MovieGridProps) {
  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null);

  if (isLoading) {
    return (
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-6">
        {Array.from({ length: 24 }).map((_, i) => (
          <MovieCardSkeleton key={i} size={size} />
        ))}
      </div>
    );
  }

  if (!movies || movies.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-20">
        <p className="text-lg text-text-secondary">No movies found</p>
        <p className="text-sm text-white/40 mt-2">Try adjusting your search or filters</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-6" onMouseLeave={() => setHoveredIndex(null)}>
      {movies.map((movie, index) => (
        <MovieCard
          key={movie.id}
          movie={movie}
          size={size}
          showQuickActions={showQuickActions}
          onWatchlistToggle={onWatchlistToggle}
          isInWatchlist={watchlistMovieIds.has(movie.id)}
          index={index}
          // Lights Out Logic
          dimmed={hoveredIndex !== null && hoveredIndex !== index}
          onHover={(isHovered) => setHoveredIndex(isHovered ? index : null)}
        />
      ))}
    </div>
  );
}
