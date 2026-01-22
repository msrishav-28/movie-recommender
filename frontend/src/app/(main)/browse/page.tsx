'use client';

import { useState } from 'react';
import { Search, SlidersHorizontal } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { MasonryGrid } from '@/components/ui/MasonryGrid';
import { Dropdown } from '@/components/ui/Dropdown';
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
    <div className="min-h-screen bg-void">
      {/* Header Section */}
      <section className="bg-void/80 border-b border-white/5 backdrop-blur-md sticky top-[64px] z-30 shadow-lg">
        <div className="container-padding py-6">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4 mb-6">
            <div>
              <h1 className="text-3xl md:text-4xl font-bold mb-2 font-headline leading-none">Browse Movies</h1>
              <p className="text-text-secondary font-mono text-sm">
                Discover {data?.pages[0]?.total.toLocaleString() || 'thousands of'} movies
              </p>
            </div>

            <div className="flex items-center gap-3 w-full md:w-auto">
              <form onSubmit={handleSearch} className="flex-1 md:w-80">
                <Input
                  type="search"
                  placeholder="Search titles..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  prefix={<Search className="h-4 w-4" />}
                  showClearButton
                  onClear={() => {
                    setSearchQuery('');
                    setFilters({ ...filters, query: '' });
                  }}
                  className="bg-white/5 border-white/10"
                />
              </form>
              <Button
                variant={showFilters ? 'primary' : 'outline'}
                icon={<SlidersHorizontal className="h-4 w-4" />}
                onClick={() => setShowFilters(!showFilters)}
                size="md"
              >
                Filters
              </Button>
            </div>
          </div>

          {/* Filter Sidebar (Collapsible) */}
          {showFilters && (
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 animate-fade-in pt-4 border-t border-white/5">
              <Dropdown
                label="Genre"
                placeholder="All Genres"
                options={[
                  { value: '', label: 'All Genres' },
                  { value: '28', label: 'Action' },
                  { value: '35', label: 'Comedy' },
                  { value: '18', label: 'Drama' },
                  { value: '27', label: 'Horror' },
                  { value: '878', label: 'Sci-Fi' },
                ]}
                value={filters.genres?.[0] || ''}
                onChange={(val) => setFilters({ ...filters, genres: val ? [val] : undefined })}
              />

              <Dropdown
                label="Year"
                placeholder="All Years"
                options={[
                  { value: '', label: 'All Years' },
                  { value: '2024', label: '2024' },
                  { value: '2023', label: '2023' },
                  { value: '2022', label: '2022' },
                  { value: '2021', label: '2021' },
                  { value: '2020', label: '2020' },
                ]}
                value={filters.min_year?.toString()}
                onChange={(val) => setFilters({
                  ...filters,
                  min_year: val ? parseInt(val) : undefined,
                  max_year: val ? parseInt(val) : undefined
                })}
              />

              <Dropdown
                label="Min Rating"
                placeholder="Any"
                options={[
                  { value: '', label: 'Any' },
                  { value: '7', label: '7+' },
                  { value: '8', label: '8+' },
                  { value: '9', label: '9+' },
                ]}
                value={filters.min_rating?.toString()}
                onChange={(val) => setFilters({ ...filters, min_rating: val ? parseInt(val) : undefined })}
              />

              <Dropdown
                label="Sort By"
                options={[
                  { value: 'popularity', label: 'Popularity' },
                  { value: 'rating', label: 'Rating' },
                  { value: 'release_date', label: 'Release Date' },
                  { value: 'title', label: 'Title' },
                ]}
                value={filters.sort_by || 'popularity'}
                onChange={(val) => setFilters({ ...filters, sort_by: val as any })}
              />
            </div>
          )}
        </div>
      </section>

      {/* Movies Grid */}
      <section className="section-spacing">
        <div className="container-padding">
          <MasonryGrid items={movies} />
          {isLoading && movies.length === 0 && (
            <div className="text-center py-20 text-text-secondary">Loading movies...</div>
          )}

          {/* Load More Trigger */}
          {hasNextPage && (
            <div ref={ref} className="flex justify-center py-12">
              {isFetchingNextPage && (
                <div className="animate-spin h-8 w-8 border-4 border-klein-blue border-t-transparent rounded-full" />
              )}
            </div>
          )}
        </div>
      </section>
    </div>
  );
}
