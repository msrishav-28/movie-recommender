'use client';

import { useState } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { Play, Plus, Info, Check, Star, Clock } from 'lucide-react';
import { motion } from 'framer-motion';
import type { Movie } from '@/types';
import { getTmdbImageUrl, extractYear, formatRuntime } from '@/lib/utils';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { cn } from '@/lib/utils';

export interface MovieCardProps {
  movie: Movie;
  size?: 'small' | 'medium' | 'large';
  tilt3D?: boolean;
  showQuickActions?: boolean;
  matchScore?: number;
  onWatchlistToggle?: (movieId: number) => void;
  isInWatchlist?: boolean;
  priority?: boolean;
  index?: number;
}

export function MovieCard({
  movie,
  size = 'medium',
  tilt3D = true,
  showQuickActions = true,
  matchScore,
  onWatchlistToggle,
  isInWatchlist = false,
  priority = false,
  index = 0,
}: MovieCardProps) {
  const [isHovered, setIsHovered] = useState(false);
  const [tiltStyle, setTiltStyle] = useState({});

  const sizes = {
    small: { width: 160, height: 240, fontSize: 'text-xs' },
    medium: { width: 220, height: 330, fontSize: 'text-sm' },
    large: { width: 280, height: 420, fontSize: 'text-base' },
  };

  const cardSize = sizes[size];

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!tilt3D) return;

    const card = e.currentTarget;
    const rect = card.getBoundingClientRect();
    const x = (e.clientY - rect.top - rect.height / 2) / (rect.height / 2);
    const y = (e.clientX - rect.left - rect.width / 2) / (rect.width / 2);

    setTiltStyle({
      transform: `perspective(1000px) rotateX(${x * -7}deg) rotateY(${y * 7}deg)`,
      transition: 'transform 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
    });
  };

  const handleMouseLeave = () => {
    setIsHovered(false);
    setTiltStyle({
      transform: 'perspective(1000px) rotateX(0deg) rotateY(0deg)',
      transition: 'transform 0.5s cubic-bezier(0.4, 0, 0.2, 1)',
    });
  };

  const handleWatchlistClick = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    onWatchlistToggle?.(movie.id);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{
        duration: 0.4,
        delay: index * 0.05,
        ease: 'easeOut',
      }}
      style={{ width: cardSize.width }}
      className="group relative"
    >
      <Link href={`/movie/${movie.id}`}>
        <div
          className="relative overflow-hidden rounded-lg gpu-accelerated preserve-3d"
          style={{
            ...tiltStyle,
            height: cardSize.height,
          }}
          onMouseMove={handleMouseMove}
          onMouseEnter={() => setIsHovered(true)}
          onMouseLeave={handleMouseLeave}
        >
          {/* Poster Image */}
          <div className="relative h-full w-full">
            <Image
              src={getTmdbImageUrl(movie.poster_path, 'w500')}
              alt={movie.title}
              fill
              className="object-cover"
              sizes={`${cardSize.width}px`}
              priority={priority}
            />

            {/* Match Score Badge (for aesthetic search results) */}
            {matchScore !== undefined && (
              <div className="absolute right-2 top-2 z-10">
                <Badge variant="success" size="sm" className="glass-heavy backdrop-blur-md font-bold">
                  {Math.round(matchScore)}% Match
                </Badge>
              </div>
            )}

            {/* Hover Overlay */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: isHovered ? 1 : 0 }}
              transition={{ duration: 0.3 }}
              className="absolute inset-0 bg-gradient-to-t from-background/90 via-background/40 to-background/20 z-10"
            >
              {showQuickActions && (
                <div className="absolute inset-0 flex items-center justify-center gap-3 z-20">
                  <Button
                    variant="glass"
                    size="sm"
                    icon={<Play className="h-4 w-4" />}
                    className="hover:scale-110 transition-transform"
                    onClick={(e) => {
                      e.preventDefault();
                      e.stopPropagation();
                      // Play trailer
                    }}
                  />
                  <Button
                    variant="glass"
                    size="sm"
                    icon={isInWatchlist ? <Check className="h-4 w-4" /> : <Plus className="h-4 w-4" />}
                    className={cn(
                      'hover:scale-110 transition-transform',
                      isInWatchlist && 'bg-brand-primary-light text-brand-primary'
                    )}
                    onClick={handleWatchlistClick}
                  />
                  <Button
                    variant="glass"
                    size="sm"
                    icon={<Info className="h-4 w-4" />}
                    className="hover:scale-110 transition-transform"
                  />
                </div>
              )}

              {/* Info Panel at Bottom */}
              <div className="absolute bottom-0 left-0 right-0 p-3 space-y-2">
                {/* Genres */}
                {movie.genres && movie.genres.length > 0 && (
                  <div className="flex gap-1.5">
                    {movie.genres.slice(0, 2).map((genre) => (
                      <Badge key={genre.id} variant="default" size="sm" className="glass-light">
                        {genre.name}
                      </Badge>
                    ))}
                  </div>
                )}

                {/* Runtime & Rating */}
                <div className="flex items-center gap-3 text-xs text-text-tertiary">
                  {movie.runtime && (
                    <span className="flex items-center gap-1">
                      <Clock className="h-3 w-3" />
                      {formatRuntime(movie.runtime)}
                    </span>
                  )}
                  {movie.vote_average && movie.vote_average > 0 && (
                    <span className="flex items-center gap-1 text-brand-tertiary">
                      <Star className="h-3 w-3 fill-current" />
                      {movie.vote_average.toFixed(1)}
                    </span>
                  )}
                </div>
              </div>
            </motion.div>
          </div>

          {/* Card Footer */}
          <div className="absolute bottom-0 left-0 right-0 bg-surface border-t border-border p-3 z-0">
            <h3 className={cn('font-semibold text-text-primary truncate-2', cardSize.fontSize)}>
              {movie.title}
            </h3>
            <div className="flex items-center justify-between mt-1">
              <span className="text-xs text-text-tertiary">
                {movie.release_date ? extractYear(movie.release_date) : 'N/A'}
              </span>
              {movie.vote_average && movie.vote_average > 0 && !isHovered && (
                <span className="flex items-center gap-1 text-xs text-brand-tertiary">
                  <Star className="h-3 w-3 fill-current" />
                  {movie.vote_average.toFixed(1)}
                </span>
              )}
            </div>
          </div>
        </div>
      </Link>
    </motion.div>
  );
}

// Skeleton loader for MovieCard
export function MovieCardSkeleton({ size = 'medium' }: { size?: 'small' | 'medium' | 'large' }) {
  const sizes = {
    small: { width: 160, height: 240 },
    medium: { width: 220, height: 330 },
    large: { width: 280, height: 420 },
  };

  const cardSize = sizes[size];

  return (
    <div style={{ width: cardSize.width }}>
      <div
        className="skeleton-shimmer rounded-lg"
        style={{ height: cardSize.height }}
      />
      <div className="mt-2 space-y-2">
        <div className="skeleton-shimmer h-4 w-3/4 rounded" />
        <div className="skeleton-shimmer h-3 w-1/2 rounded" />
      </div>
    </div>
  );
}
