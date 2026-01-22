'use client';

import { useState } from 'react';
import { MovieCard } from '@/components/movie/MovieCard';
import type { Movie, AestheticSearchResult } from '@/types';
import { cn } from '@/lib/utils';

type GridItem = Movie | AestheticSearchResult;

interface MasonryGridProps {
    items: GridItem[];
    className?: string;
    onWatchlistToggle?: (movieId: number) => void;
    watchlistMovieIds?: Set<number>;
    isLoading?: boolean;
}

export function MasonryGrid({ items, className, onWatchlistToggle, watchlistMovieIds, isLoading = false }: MasonryGridProps) {
    const [hoveredIndex, setHoveredIndex] = useState<number | null>(null);

    return (
        <div className={cn(
            "grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 md:gap-8",
            className
        )}>
            {isLoading && items.length === 0 ? (
                Array.from({ length: 10 }).map((_, i) => (
                    <div key={i} className="aspect-[2/3] bg-white/5 rounded-lg animate-pulse" />
                ))
            ) : (
                items.map((item, index) => {
                    // Handle both Movie objects and AestheticSearchResult objects
                    const movie = 'movie' in item ? item.movie : item;
                    const score = 'match_score' in item ? item.match_score : undefined;

                    // Use movie.id as key, assume unique
                    return (
                        <div
                            key={movie.id}
                            className="relative transition-all duration-500"
                            onMouseEnter={() => setHoveredIndex(index)}
                            onMouseLeave={() => setHoveredIndex(null)}
                        >
                            <MovieCard
                                movie={movie}
                                size="large" // Force large monolith size
                                dimmed={hoveredIndex !== null && hoveredIndex !== index}
                                index={index}
                                matchScore={score}
                                onWatchlistToggle={onWatchlistToggle}
                                isInWatchlist={watchlistMovieIds?.has(movie.id)}
                            />
                        </div>
                    );
                })
            )}
        </div>
    );
}
