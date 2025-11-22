import { Suspense } from 'react';
import Image from 'next/image';
import { Star, Clock, Calendar, Play, Plus, Share2 } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { Card, CardContent } from '@/components/ui/Card';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/Tabs';
import { MovieGrid } from '@/components/movie/MovieGrid';
import { ReviewList } from '@/components/movie/ReviewList';
import { movieService } from '@/services/movie.service';
import { recommendationService } from '@/services/recommendation.service';
import { getBackdropUrl, getTmdbImageUrl, formatRuntime, extractYear } from '@/lib/utils';
import { MovieRatingSection } from './MovieRatingSection';

interface MoviePageProps {
  params: {
    id: string;
  };
}

async function getMovieData(id: number) {
  try {
    const movie = await movieService.getMovieById(id);
    return movie;
  } catch (error) {
    console.error('Failed to fetch movie:', error);
    return null;
  }
}

async function getSimilarMovies(id: number) {
  try {
    const movies = await recommendationService.getSimilarMovies(id, 6);
    return movies;
  } catch (error) {
    console.error('Failed to fetch similar movies:', error);
    return [];
  }
}

export default async function MovieDetailPage({ params }: MoviePageProps) {
  const movieId = parseInt(params.id);
  const movie = await getMovieData(movieId);
  const similarMovies = await getSimilarMovies(movieId);

  if (!movie) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold mb-2">Movie Not Found</h1>
          <p className="text-text-secondary">The movie you're looking for doesn't exist.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      {/* Hero Section with Backdrop */}
      <section className="relative h-[70vh] overflow-hidden">
        {/* Backdrop Image */}
        <div className="absolute inset-0">
          <Image
            src={getBackdropUrl(movie.backdrop_path, 'original')}
            alt={movie.title}
            fill
            className="object-cover"
            priority
          />
          <div className="absolute inset-0 bg-gradient-to-t from-background via-background/60 to-background/20" />
        </div>

        {/* Content */}
        <div className="container-padding relative h-full flex items-end pb-12">
          <div className="grid grid-cols-1 md:grid-cols-12 gap-8 w-full">
            {/* Poster */}
            <div className="md:col-span-3">
              <div className="relative aspect-[2/3] rounded-lg overflow-hidden shadow-2xl">
                <Image
                  src={getTmdbImageUrl(movie.poster_path, 'w500')}
                  alt={movie.title}
                  fill
                  className="object-cover"
                  priority
                />
              </div>
            </div>

            {/* Info */}
            <div className="md:col-span-9 space-y-4">
              <div className="flex flex-wrap gap-2">
                {movie.genres.map((genre) => (
                  <Badge key={genre.id} variant="primary">
                    {genre.name}
                  </Badge>
                ))}
              </div>

              <h1 className="text-5xl md:text-6xl font-bold">{movie.title}</h1>

              {movie.tagline && (
                <p className="text-xl text-text-secondary italic">"{movie.tagline}"</p>
              )}

              <div className="flex flex-wrap items-center gap-4 text-text-secondary">
                {movie.release_date && (
                  <span className="flex items-center gap-2">
                    <Calendar className="h-5 w-5" />
                    {extractYear(movie.release_date)}
                  </span>
                )}
                {movie.runtime && (
                  <span className="flex items-center gap-2">
                    <Clock className="h-5 w-5" />
                    {formatRuntime(movie.runtime)}
                  </span>
                )}
                {movie.vote_average && (
                  <span className="flex items-center gap-2">
                    <Star className="h-5 w-5 fill-brand-tertiary text-brand-tertiary" />
                    {movie.vote_average.toFixed(1)} / 10
                  </span>
                )}
              </div>

              {/* Action Buttons */}
              <div className="flex flex-wrap gap-3 pt-4">
                <Button size="lg" variant="primary" icon={<Play className="h-5 w-5" />} glow>
                  Watch Trailer
                </Button>
                <Button size="lg" variant="glass" icon={<Plus className="h-5 w-5" />}>
                  Add to Watchlist
                </Button>
                <Button size="lg" variant="glass" icon={<Share2 className="h-5 w-5" />}>
                  Share
                </Button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Movie Details */}
      <section className="section-spacing">
        <div className="container-padding">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Main Content */}
            <div className="lg:col-span-2 space-y-8">
              {/* Overview */}
              <div>
                <h2 className="text-2xl font-bold mb-4">Overview</h2>
                <p className="text-lg text-text-secondary leading-relaxed">{movie.overview}</p>
              </div>

              {/* Cast */}
              {movie.cast && movie.cast.length > 0 && (
                <div>
                  <h2 className="text-2xl font-bold mb-4">Cast</h2>
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                    {movie.cast.slice(0, 6).map((person) => (
                      <Card key={person.id} variant="glass">
                        <CardContent className="p-4">
                          <div className="flex items-center gap-3">
                            {person.profile_path && (
                              <div className="relative h-16 w-16 rounded-full overflow-hidden shrink-0">
                                <Image
                                  src={getTmdbImageUrl(person.profile_path, 'w185')}
                                  alt={person.name}
                                  fill
                                  className="object-cover"
                                />
                              </div>
                            )}
                            <div className="min-w-0">
                              <p className="font-semibold truncate">{person.name}</p>
                              {person.character && (
                                <p className="text-sm text-text-tertiary truncate">{person.character}</p>
                              )}
                            </div>
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Sidebar */}
            <div className="space-y-6">
              {/* Facts */}
              <Card variant="glass">
                <CardContent className="p-6 space-y-4">
                  <h3 className="text-lg font-bold">Details</h3>

                  {movie.status && (
                    <div>
                      <p className="text-sm text-text-tertiary mb-1">Status</p>
                      <p className="font-medium">{movie.status}</p>
                    </div>
                  )}

                  {movie.original_language && (
                    <div>
                      <p className="text-sm text-text-tertiary mb-1">Original Language</p>
                      <p className="font-medium">{movie.original_language.toUpperCase()}</p>
                    </div>
                  )}

                  {movie.budget && movie.budget > 0 && (
                    <div>
                      <p className="text-sm text-text-tertiary mb-1">Budget</p>
                      <p className="font-medium">${(movie.budget / 1000000).toFixed(0)}M</p>
                    </div>
                  )}

                  {movie.revenue && movie.revenue > 0 && (
                    <div>
                      <p className="text-sm text-text-tertiary mb-1">Revenue</p>
                      <p className="font-medium">${(movie.revenue / 1000000).toFixed(0)}M</p>
                    </div>
                  )}
                </CardContent>
              </Card>

              {/* Keywords/Tags could go here */}
            </div>
          </div>
        </div>
      </section>

      {/* Ratings & Reviews */}
      <section className="section-spacing">
        <div className="container-padding">
          <h2 className="text-3xl font-bold mb-8">Ratings & Reviews</h2>
          
          <Tabs defaultValue="reviews">
            <TabsList>
              <TabsTrigger value="reviews">Reviews</TabsTrigger>
              <TabsTrigger value="rate">Rate This Movie</TabsTrigger>
            </TabsList>

            <TabsContent value="reviews" className="mt-8">
              <Suspense fallback={<div>Loading reviews...</div>}>
                <ReviewList movieId={movieId} />
              </Suspense>
            </TabsContent>

            <TabsContent value="rate" className="mt-8">
              <MovieRatingSection movieId={movieId} movieTitle={movie.title} />
            </TabsContent>
          </Tabs>
        </div>
      </section>

      {/* Similar Movies */}
      {similarMovies.length > 0 && (
        <section className="section-spacing bg-surface/50">
          <div className="container-padding">
            <h2 className="text-3xl font-bold mb-8">Similar Movies</h2>
            <Suspense fallback={<div>Loading...</div>}>
              <MovieGrid movies={similarMovies} size="medium" />
            </Suspense>
          </div>
        </section>
      )}
    </div>
  );
}
