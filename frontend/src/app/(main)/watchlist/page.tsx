'use client';

import { useState } from 'react';
import { Heart, Check, Trash2, Grid, List } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { Dropdown } from '@/components/ui/Dropdown';
import { MovieGrid } from '@/components/movie/MovieGrid';
import { Card, CardContent } from '@/components/ui/Card';
import { useWatchlist } from '@/hooks/useWatchlist';
import { Badge } from '@/components/ui/Badge';
import Image from 'next/image';
import Link from 'next/link';
import { getTmdbImageUrl, extractYear, formatRuntime } from '@/lib/utils';

export default function WatchlistPage() {
  const { watchlist, isLoading, removeFromWatchlist, updateWatchlistStatus } = useWatchlist();
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [filterMode, setFilterMode] = useState<'all' | 'watched' | 'unwatched'>('all');
  const [sortBy, setSortBy] = useState<'added' | 'title' | 'rating'>('added');

  const filteredWatchlist = watchlist
    ?.filter((item) => {
      if (filterMode === 'watched') return item.watched;
      if (filterMode === 'unwatched') return !item.watched;
      return true;
    })
    .sort((a, b) => {
      if (sortBy === 'title') return a.movie.title.localeCompare(b.movie.title);
      if (sortBy === 'rating') return (b.movie.vote_average || 0) - (a.movie.vote_average || 0);
      return new Date(b.added_at).getTime() - new Date(a.added_at).getTime();
    });

  if (isLoading) {
    return (
      <div className="min-h-screen">
        <div className="container-padding py-20">
          <div className="animate-pulse space-y-4">
            <div className="h-8 w-64 bg-glass-medium rounded" />
            <div className="h-4 w-96 bg-glass-medium rounded" />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      {/* Header */}
      <section className="bg-surface/50 border-b border-border">
        <div className="container-padding py-8">
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 mb-6">
            <div>
              <h1 className="text-4xl font-bold mb-2">My Watchlist</h1>
              <p className="text-text-secondary">
                {filteredWatchlist?.length || 0} movies saved
              </p>
            </div>

            <div className="flex items-center gap-2">
              <Button
                variant={viewMode === 'grid' ? 'primary' : 'ghost'}
                size="sm"
                icon={<Grid className="h-4 w-4" />}
                onClick={() => setViewMode('grid')}
              />
              <Button
                variant={viewMode === 'list' ? 'primary' : 'ghost'}
                size="sm"
                icon={<List className="h-4 w-4" />}
                onClick={() => setViewMode('list')}
              />
            </div>
          </div>

          {/* Filters */}
          <div className="flex flex-wrap gap-3">
            <Dropdown
              label="Filter"
              options={[
                { value: 'all', label: 'All Movies' },
                { value: 'unwatched', label: 'Not Watched' },
                { value: 'watched', label: 'Watched' },
              ]}
              value={filterMode}
              onChange={(value) => setFilterMode(value as any)}
            />

            <Dropdown
              label="Sort By"
              options={[
                { value: 'added', label: 'Date Added' },
                { value: 'title', label: 'Title' },
                { value: 'rating', label: 'Rating' },
              ]}
              value={sortBy}
              onChange={(value) => setSortBy(value as any)}
            />
          </div>
        </div>
      </section>

      {/* Content */}
      <section className="section-spacing">
        <div className="container-padding">
          {filteredWatchlist && filteredWatchlist.length > 0 ? (
            viewMode === 'grid' ? (
              <MovieGrid
                movies={filteredWatchlist.map((item) => item.movie)}
                size="medium"
                onWatchlistToggle={removeFromWatchlist}
                watchlistMovieIds={new Set(watchlist?.map((i) => i.movie_id))}
              />
            ) : (
              <div className="space-y-4">
                {filteredWatchlist.map((item) => (
                  <Card key={item.id} variant="glass" hover>
                    <CardContent className="p-4">
                      <div className="flex gap-4">
                        <Link href={`/movie/${item.movie_id}`} className="shrink-0">
                          <div className="relative w-24 h-36 rounded-md overflow-hidden">
                            <Image
                              src={getTmdbImageUrl(item.movie.poster_path, 'w200')}
                              alt={item.movie.title}
                              fill
                              className="object-cover"
                            />
                          </div>
                        </Link>

                        <div className="flex-1 min-w-0">
                          <Link href={`/movie/${item.movie_id}`}>
                            <h3 className="text-xl font-bold mb-2 hover:text-brand-primary transition-colors">
                              {item.movie.title}
                            </h3>
                          </Link>

                          <div className="flex flex-wrap gap-2 mb-3">
                            {item.watched && (
                              <Badge variant="success" size="sm">
                                Watched
                              </Badge>
                            )}
                            {item.movie.release_date && (
                              <Badge variant="outline" size="sm">
                                {extractYear(item.movie.release_date)}
                              </Badge>
                            )}
                            {item.movie.runtime && (
                              <Badge variant="outline" size="sm">
                                {formatRuntime(item.movie.runtime)}
                              </Badge>
                            )}
                          </div>

                          <p className="text-sm text-text-secondary line-clamp-2 mb-4">
                            {item.movie.overview}
                          </p>

                          <div className="flex gap-2">
                            <Button
                              size="sm"
                              variant={item.watched ? 'outline' : 'primary'}
                              icon={<Check className="h-4 w-4" />}
                              onClick={() =>
                                updateWatchlistStatus({
                                  movieId: item.movie_id,
                                  watched: !item.watched,
                                })
                              }
                            >
                              {item.watched ? 'Watched' : 'Mark Watched'}
                            </Button>
                            <Button
                              size="sm"
                              variant="ghost"
                              icon={<Trash2 className="h-4 w-4" />}
                              onClick={() => removeFromWatchlist(item.movie_id)}
                            >
                              Remove
                            </Button>
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )
          ) : (
            <Card variant="glass">
              <CardContent className="p-12 text-center">
                <Heart className="h-16 w-16 mx-auto mb-4 text-text-tertiary" />
                <h3 className="text-2xl font-bold mb-2">Your watchlist is empty</h3>
                <p className="text-text-secondary mb-6">
                  Start adding movies you want to watch
                </p>
                <Link href="/browse">
                  <Button variant="primary" size="lg">
                    Browse Movies
                  </Button>
                </Link>
              </CardContent>
            </Card>
          )}
        </div>
      </section>
    </div>
  );
}
