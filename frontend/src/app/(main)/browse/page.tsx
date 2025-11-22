'use client';

import { useState } from 'react';
import { Search, SlidersHorizontal } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { MovieGrid } from '@/components/movie/MovieGrid';
import { useInfiniteMovies } from '@/hooks/useMovies';
import { useInView } from 'react-intersection-observer';
import { useEffect } from 'react';
import type { SearchFilters } from '@/types';

export default function BrowsePage() {
  const [filters, setFilters] = useState<SearchFilters>({});
  const [searchQuery, setSearchQuery] = useState('');
  const [showFilters, setShowFilters] = useState(false);

  const { data, fetchNextPage, hasNextPage, isFetchingNextPage, isLoading } =
    useInfiniteMovies(filters, 24);

  const { ref, inView } = useInView();

  // Load more when scrolling to bottom
  useEffect(() => {
    if (inView && hasNextPage && !isFetchingNextPage) {
      fetchNextPage();
    }
  }, [inView, hasNextPage, isFetchingNextPage, fetchNextPage]);

  const movies = data?.pages.flatMap((page) => page.items) ?? [];

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setFilters({ ...filters, query: searchQuery });
  };

  return (
    <div className="min-h-screen">
      {/* Header Section */}
      <section className="bg-surface/50 border-b border-border">
        <div className="container-padding py-8">
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 mb-6">
            <div>
              <h1 className="text-4xl font-bold mb-2">Browse Movies</h1>
              <p className="text-text-secondary">
                Discover {data?.pages[0]?.total.toLocaleString() || '...'} movies
              </p>
            </div>

            <Button
              variant="outline"
              icon={<SlidersHorizontal className="h-5 w-5" />}
              onClick={() => setShowFilters(!showFilters)}
            >
              {showFilters ? 'Hide' : 'Show'} Filters
            </Button>
          </div>

          {/* Search Bar */}
          <form onSubmit={handleSearch} className="max-w-2xl">
            <Input
              type="search"
              placeholder="Search for movies..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              prefix={<Search className="h-5 w-5" />}
              showClearButton
              onClear={() => {
                setSearchQuery('');
                setFilters({ ...filters, query: '' });
              }}
            />
          </form>
        </div>
      </section>

      {/* Filter Sidebar (Collapsible) */}
      {showFilters && (
        <section className="bg-surface border-b border-border">
          <div className="container-padding py-6">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              {/* Genre Filter */}
              <div>
                <label className="text-sm font-medium mb-2 block">Genre</label>
                <select className="w-full rounded-md border border-border bg-background px-3 py-2 text-sm">
                  <option value="">All Genres</option>
                  <option value="28">Action</option>
                  <option value="35">Comedy</option>
                  <option value="18">Drama</option>
                  <option value="27">Horror</option>
                  <option value="878">Sci-Fi</option>
                </select>
              </div>

              {/* Year Filter */}
              <div>
                <label className="text-sm font-medium mb-2 block">Year</label>
                <select className="w-full rounded-md border border-border bg-background px-3 py-2 text-sm">
                  <option value="">All Years</option>
                  <option value="2024">2024</option>
                  <option value="2023">2023</option>
                  <option value="2022">2022</option>
                  <option value="2021">2021</option>
                  <option value="2020">2020</option>
                </select>
              </div>

              {/* Rating Filter */}
              <div>
                <label className="text-sm font-medium mb-2 block">Min Rating</label>
                <select className="w-full rounded-md border border-border bg-background px-3 py-2 text-sm">
                  <option value="">Any</option>
                  <option value="7">7+</option>
                  <option value="8">8+</option>
                  <option value="9">9+</option>
                </select>
              </div>

              {/* Sort By */}
              <div>
                <label className="text-sm font-medium mb-2 block">Sort By</label>
                <select className="w-full rounded-md border border-border bg-background px-3 py-2 text-sm">
                  <option value="popularity">Popularity</option>
                  <option value="rating">Rating</option>
                  <option value="release_date">Release Date</option>
                  <option value="title">Title</option>
                </select>
              </div>
            </div>
          </div>
        </section>
      )}

      {/* Movies Grid */}
      <section className="section-spacing">
        <div className="container-padding">
          <MovieGrid movies={movies} isLoading={isLoading} size="medium" />

          {/* Load More Trigger */}
          {hasNextPage && (
            <div ref={ref} className="flex justify-center py-8">
              {isFetchingNextPage ? (
                <div className="animate-spin h-8 w-8 border-4 border-brand-primary border-t-transparent rounded-full" />
              ) : (
                <Button onClick={() => fetchNextPage()} variant="outline">
                  Load More
                </Button>
              )}
            </div>
          )}
        </div>
      </section>
    </div>
  );
}
