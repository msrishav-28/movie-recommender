'use client';

import { useEffect } from 'react';
import { Star, Film } from 'lucide-react';
import { MasonryGrid } from '@/components/ui/MasonryGrid';
import { useInfiniteTopRatedMovies } from '@/hooks/useMovies';
import { useInView } from 'react-intersection-observer';
import { motion } from 'framer-motion';

export default function TopRatedPage() {
  const { ref, inView } = useInView();
  const {
    data,
    isLoading,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage
  } = useInfiniteTopRatedMovies(24);

  useEffect(() => {
    if (inView && hasNextPage && !isFetchingNextPage) {
      fetchNextPage();
    }
  }, [inView, hasNextPage, isFetchingNextPage, fetchNextPage]);

  // Flatten pages into a single array of movies
  const movies = data?.pages.flatMap((page) => page.items) || [];

  return (
    <div className="min-h-screen bg-void">
      {/* Sticky Header */}
      <motion.div
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        className="sticky top-[64px] z-30 z-header bg-void/80 backdrop-blur-md border-b border-white/5 shadow-lg"
      >
        <div className="container-padding py-6">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-brand-tertiary/10 border border-brand-tertiary/20">
                <Star className="h-6 w-6 text-brand-tertiary fill-current" />
              </div>
              <div>
                <h1 className="text-2xl font-bold font-headline leading-none mb-1">Top Rated</h1>
                <p className="text-sm text-text-secondary font-mono">
                  Critically acclaimed masterpieces
                </p>
              </div>
            </div>

            <div className="flex items-center gap-2 text-xs font-mono text-white/40">
              <Film className="w-3 h-3" />
              <span>{movies.length} TITLES</span>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Content */}
      <section className="section-spacing pt-8">
        <div className="container-padding">
          <MasonryGrid
            items={movies}
            isLoading={isLoading}
          />

          {/* Infinite Scroll Trigger */}
          <div ref={ref} className="w-full h-20 flex items-center justify-center mt-8">
            {isFetchingNextPage && (
              <div className="flex flex-col items-center gap-2">
                <div className="w-6 h-6 border-2 border-brand-tertiary border-t-transparent rounded-full animate-spin" />
                <span className="text-xs text-brand-tertiary/80 font-mono animate-pulse">LOADING MORE...</span>
              </div>
            )}
          </div>
        </div>
      </section>
    </div>
  );
}
