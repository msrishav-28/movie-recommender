'use client';

import { useState, useRef } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { MovieCard } from './MovieCard';
import { Button } from '@/components/ui/Button';
import type { Movie } from '@/types';

interface MovieCarouselProps {
  movies: Movie[];
  title?: string;
  size?: 'small' | 'medium' | 'large';
}

export function MovieCarousel({ movies, title, size = 'medium' }: MovieCarouselProps) {
  const scrollRef = useRef<HTMLDivElement>(null);
  const [canScrollLeft, setCanScrollLeft] = useState(false);
  const [canScrollRight, setCanScrollRight] = useState(true);

  const checkScroll = () => {
    if (scrollRef.current) {
      const { scrollLeft, scrollWidth, clientWidth } = scrollRef.current;
      setCanScrollLeft(scrollLeft > 0);
      setCanScrollRight(scrollLeft < scrollWidth - clientWidth - 10);
    }
  };

  const scroll = (direction: 'left' | 'right') => {
    if (scrollRef.current) {
      const scrollAmount = scrollRef.current.clientWidth * 0.8;
      scrollRef.current.scrollBy({
        left: direction === 'left' ? -scrollAmount : scrollAmount,
        behavior: 'smooth',
      });
      setTimeout(checkScroll, 300);
    }
  };

  return (
    <div className="relative group">
      {title && <h3 className="text-2xl font-bold mb-4">{title}</h3>}

      <div
        ref={scrollRef}
        onScroll={checkScroll}
        className="flex gap-6 overflow-x-auto scrollbar-hide scroll-smooth pb-4"
      >
        {movies.map((movie, index) => (
          <MovieCard key={movie.id} movie={movie} size={size} index={index} />
        ))}
      </div>

      {canScrollLeft && (
        <Button
          variant="glass"
          size="sm"
          icon={<ChevronLeft />}
          className="absolute left-2 top-1/2 -translate-y-1/2 opacity-0 group-hover:opacity-100 transition-opacity z-10"
          onClick={() => scroll('left')}
        />
      )}

      {canScrollRight && (
        <Button
          variant="glass"
          size="sm"
          icon={<ChevronRight />}
          className="absolute right-2 top-1/2 -translate-y-1/2 opacity-0 group-hover:opacity-100 transition-opacity z-10"
          onClick={() => scroll('right')}
        />
      )}
    </div>
  );
}
