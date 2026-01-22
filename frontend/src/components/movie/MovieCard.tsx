'use client';

import { useState } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { Play, Plus, Info, Star } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import type { Movie } from '@/types';
import { getTmdbImageUrl, extractYear } from '@/lib/utils';
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
  dimmed?: boolean; // New prop for Lights Out effect
  onHover?: (isHovered: boolean) => void;
}

export function MovieCard({
  movie,
  size = 'medium',
  tilt3D = true, // Maintained for legacy compatibility but disabled visually if needed
  showQuickActions = true,
  matchScore,
  onWatchlistToggle,
  isInWatchlist = false,
  priority = false,
  index = 0,
  dimmed = false,
  onHover,
}: MovieCardProps) {
  const [isHovered, setIsHovered] = useState(false);

  const sizes = {
    small: { width: 160, height: 240 },
    medium: { width: 220, height: 330 },
    large: { width: 280, height: 420 },
  };

  const cardSize = sizes[size];

  const handleMouseEnter = () => {
    setIsHovered(true);
    onHover?.(true);
  };

  const handleMouseLeave = () => {
    setIsHovered(false);
    onHover?.(false);
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{
        opacity: dimmed ? 0.3 : 1,
        scale: isHovered ? 1.05 : (dimmed ? 0.98 : 1),
        filter: dimmed ? 'grayscale(100%)' : 'grayscale(0%)',
      }}
      transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
      className={cn("group relative block", dimmed && "pointer-events-none")}
      style={{ width: '100%', aspectRatio: '2/3' }} // Responsive aspect ratio
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      <Link href={`/movie/${movie.id}`} className="block w-full h-full">
        <div className="relative w-full h-full overflow-hidden rounded-none sm:rounded-lg bg-void-deep border border-white/5">

          {/* Image Layer */}
          <div className="absolute inset-0 w-full h-full transform transition-transform duration-700 ease-out group-hover:scale-110">
            <Image
              src={getTmdbImageUrl(movie.poster_path, 'w500')}
              alt={movie.title}
              fill
              className="object-cover"
              sizes="(max-width: 768px) 50vw, 33vw"
              priority={priority}
            />
          </div>

          {/* Match Score Badge (Electric Teal) */}
          {matchScore !== undefined && (
            <div className="absolute right-2 top-2 z-20">
              <div className="px-2 py-1 bg-black/50 backdrop-blur-md border border-electric-teal/50 rounded flex items-center gap-1 shadow-[0_0_15px_rgba(0,217,255,0.3)]">
                <div className="w-1.5 h-1.5 rounded-full bg-electric-teal animate-pulse" />
                <span className="text-xs font-mono font-bold text-electric-teal">{Math.round(matchScore)}%</span>
              </div>
            </div>
          )}

          {/* Gradient Overlay (Always present but subtle, intensifies on hover) */}
          <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/20 to-transparent opacity-60 group-hover:opacity-90 transition-opacity duration-500" />

          {/* Content Layer (Reveals on Hover) */}
          <div className="absolute inset-0 flex flex-col justify-end p-4 z-20">

            {/* Title & Meta - Slides Up */}
            <div className="transform translate-y-4 group-hover:translate-y-0 transition-transform duration-500 ease-out">
              <h3 className="font-headline font-bold text-xl leading-tight text-white mb-1 drop-shadow-md">
                {movie.title}
              </h3>

              <div className="flex items-center gap-3 text-xs font-mono text-text-tech opacity-0 group-hover:opacity-100 transition-opacity duration-500 delay-75">
                <span>{movie.release_date ? extractYear(movie.release_date) : 'UNKNOWN'}</span>
                <span className="text-white/20">|</span>
                <div className="flex items-center gap-1">
                  <Star className="w-3 h-3 text-cinema-gold fill-current" />
                  <span className="text-cinema-gold">{movie.vote_average?.toFixed(1) || '0.0'}</span>
                </div>
              </div>
            </div>

            {/* Quick Actions (Optional, appear on hover) */}
            {showQuickActions && (
              <div className="mt-4 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity duration-500 delay-100 transform translate-y-4 group-hover:translate-y-0">
                <Button size="sm" className="bg-white text-black hover:bg-white/90 border-none font-bold">
                  <Play className="w-4 h-4 mr-1 fill-current" /> WATCH
                </Button>
                <Button
                  size="sm"
                  variant="glass"
                  className="border-white/20 hover:border-white text-white"
                  onClick={(e) => {
                    e.preventDefault();
                    onWatchlistToggle?.(movie.id);
                  }}
                >
                  <Plus className={cn("w-4 h-4", isInWatchlist && "rotate-45")} />
                </Button>
              </div>
            )}
          </div>

        </div>
      </Link>
    </motion.div>
  );
}

// Skeleton loader
export function MovieCardSkeleton({ size }: { size?: 'small' | 'medium' | 'large' }) {
  return (
    <div className="block w-full aspect-[2/3] rounded-lg bg-white/5 animate-pulse relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent animate-[shimmer_2s_infinite]" />
    </div>
  );
}

