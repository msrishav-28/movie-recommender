import { Suspense } from 'react';
import Image from 'next/image';
import { Star, Clock, Calendar, Play, Plus, Share2, Film, Quote, Globe, DollarSign, User } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { Card, CardContent } from '@/components/ui/Card';
import { Tabs } from '@/components/ui/Tabs';
import { MasonryGrid } from '@/components/ui/MasonryGrid';
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
    const movies = await recommendationService.getSimilarMovies(id, 10);
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
      <div className="min-h-screen flex items-center justify-center bg-void text-center">
        <div className="space-y-4">
          <Film className="w-16 h-16 mx-auto text-white/40" />
          <h1 className="text-2xl font-bold font-headline">Movie Not Found</h1>
          <p className="text-text-secondary">The reel you are looking for seems to be missing.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-void">
      {/* Hero Section with Backdrop */}
      <section className="relative min-h-[85vh] flex items-end overflow-hidden">
        {/* Backdrop Image */}
        <div className="absolute inset-0 z-0 select-none">
          <Image
            src={getBackdropUrl(movie.backdrop_path, 'original')}
            alt={movie.title}
            fill
            className="object-cover animate-pan-slow opacity-60"
            priority
          />
          {/* Cinematic Gradients */}
          <div className="absolute inset-0 bg-gradient-to-t from-void via-void/60 to-transparent" />
          <div className="absolute inset-0 bg-gradient-to-r from-void via-void/40 to-transparent" />
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_transparent_0%,_#050505_120%)]" />
        </div>

        {/* Content */}
        <div className="container-padding relative z-10 pb-16 w-full">
          <div className="grid grid-cols-1 md:grid-cols-12 gap-8 lg:gap-12 items-end">
            {/* Poster - Floating Glass Effect */}
            <div className="hidden md:block md:col-span-3 lg:col-span-3">
              <div className="relative aspect-[2/3] rounded-lg overflow-hidden shadow-[0_20px_60px_-15px_rgba(0,0,0,0.8)] border border-white/10 group perspective-1000 transform transition-transform hover:scale-[1.02]">
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
            <div className="md:col-span-9 lg:col-span-9 space-y-6">
              {/* Meta Badges */}
              <div className="flex flex-wrap gap-2 animate-in fade-in slide-in-from-bottom-4 duration-700 delay-100">
                {movie.status === 'Released' && (
                  <Badge variant="success" className="bg-emerald-500/10 text-emerald-400 border-emerald-500/20">Now Showing</Badge>
                )}
                {movie.genres.map((genre) => (
                  <Badge key={genre.id} variant="outline" className="backdrop-blur-sm">
                    {genre.name}
                  </Badge>
                ))}
              </div>

              {/* Title */}
              <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold font-headline leading-none text-white drop-shadow-xl animate-in fade-in slide-in-from-bottom-6 duration-700 delay-200">
                {movie.title}
              </h1>

              {/* Tagline */}
              {movie.tagline && (
                <div className="flex items-center gap-2 text-xl md:text-2xl text-text-secondary italic font-light animate-in fade-in slide-in-from-bottom-6 duration-700 delay-300">
                  <span className="w-8 h-[1px] bg-klein-blue/50"></span>
                  &quot;{movie.tagline}&quot;
                </div>
              )}

              {/* Stats Row */}
              <div className="flex flex-wrap items-center gap-6 text-sm md:text-base font-mono text-text-secondary animate-in fade-in slide-in-from-bottom-6 duration-700 delay-400">
                {movie.release_date && (
                  <span className="flex items-center gap-2 text-white/80">
                    <Calendar className="h-4 w-4 text-klein-blue" />
                    {extractYear(movie.release_date)}
                  </span>
                )}
                {movie.runtime && (
                  <span className="flex items-center gap-2 text-white/80">
                    <Clock className="h-4 w-4 text-klein-blue" />
                    {formatRuntime(movie.runtime)}
                  </span>
                )}
                {movie.vote_average && (
                  <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-yellow-500/10 border border-yellow-500/20 text-yellow-500">
                    <Star className="h-4 w-4 fill-current" />
                    <span className="font-bold">{movie.vote_average.toFixed(1)}</span>
                  </div>
                )}
                <div className="flex items-center gap-2">
                  <Globe className="h-4 w-4 text-electric-teal" />
                  <span className="uppercase">{movie.original_language}</span>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex flex-wrap gap-4 pt-6 animate-in fade-in slide-in-from-bottom-6 duration-700 delay-500">
                <Button size="lg" variant="primary" icon={<Play className="h-5 w-5 fill-current" />} glow className="h-14 px-8 text-lg">
                  Watch Trailer
                </Button>
                <div className="flex gap-2">
                  <Button size="lg" variant="glass" icon={<Plus className="h-5 w-5" />} className="h-14 w-14 p-0 rounded-full" />
                  <Button size="lg" variant="glass" icon={<Share2 className="h-5 w-5" />} className="h-14 w-14 p-0 rounded-full" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Main Content Area */}
      <section className="section-spacing relative z-10">
        <div className="container-padding">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-12">

            {/* Left Column (Details) */}
            <div className="lg:col-span-8 space-y-12">
              {/* Overview */}
              <div>
                <h2 className="text-2xl font-bold font-headline mb-6 flex items-center gap-2">
                  <Quote className="w-5 h-5 text-klein-blue" />
                  Synopsis
                </h2>
                <div className="prose prose-invert prose-lg max-w-none text-text-secondary leading-relaxed font-light">
                  <p>{movie.overview}</p>
                </div>
              </div>

              {/* Top Cast */}
              {movie.cast && movie.cast.length > 0 && (
                <div>
                  <h2 className="text-2xl font-bold font-headline mb-6">Top Cast</h2>
                  <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
                    {movie.cast.slice(0, 6).map((person) => (
                      <div key={person.id} className="group relative overflow-hidden rounded-lg bg-void-deep/30 hover:bg-void-deep/50 transition-colors border border-white/5">
                        <div className="flex items-center gap-4 p-3">
                          <div className="relative h-12 w-12 rounded-full overflow-hidden shrink-0 border border-white/10">
                            {person.profile_path ? (
                              <Image
                                src={getTmdbImageUrl(person.profile_path, 'w185')}
                                alt={person.name}
                                fill
                                className="object-cover"
                              />
                            ) : (
                              <div className="w-full h-full bg-white/10 flex items-center justify-center">
                                <User className="w-5 h-5 text-white/50" />
                              </div>
                            )}
                          </div>
                          <div className="min-w-0">
                            <p className="font-bold text-sm text-white truncate group-hover:text-klein-blue transition-colors">{person.name}</p>
                            <p className="text-xs text-white/40 truncate font-mono">{person.character}</p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Ratings & Reviews Tab Section */}
              <div>
                <Tabs
                  defaultTab="reviews"
                  variant="pills"
                  tabs={[
                    {
                      id: 'reviews',
                      label: 'Community Reviews',
                      icon: <Quote className="w-4 h-4" />,
                      content: (
                        <div className="mt-8">
                          <Suspense fallback={
                            <div className="flex items-center justify-center py-12">
                              <div className="w-8 h-8 border-2 border-klein-blue border-t-transparent rounded-full animate-spin" />
                            </div>
                          }>
                            <ReviewList movieId={movieId} />
                          </Suspense>
                        </div>
                      ),
                    },
                    {
                      id: 'rate',
                      label: 'Rate Movie',
                      icon: <Star className="w-4 h-4" />,
                      content: (
                        <div className="mt-8">
                          <Card variant="glass">
                            <CardContent className="p-8">
                              <MovieRatingSection movieId={movieId} movieTitle={movie.title} />
                            </CardContent>
                          </Card>
                        </div>
                      ),
                    },
                  ]}
                />
              </div>
            </div>

            {/* Right Column (Sidebar Stats) */}
            <div className="lg:col-span-4 space-y-8">
              <Card variant="glass" className="bg-void-deep/20 backdrop-blur-md border-white/5 sticky top-24">
                <CardContent className="p-6 space-y-6">
                  <h3 className="text-lg font-bold font-headline border-b border-white/10 pb-4">Film Data</h3>

                  <div className="grid grid-cols-1 gap-4 text-sm">
                    <div className="flex justify-between items-center">
                      <span className="text-white/40">Status</span>
                      <Badge variant="outline">{movie.status}</Badge>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-white/40">Original Language</span>
                      <span className="font-mono uppercase">{movie.original_language}</span>
                    </div>
                    {movie.budget && movie.budget > 0 && (
                      <div className="flex justify-between items-center">
                        <span className="text-white/40">Budget</span>
                        <span className="font-mono text-white flex items-center gap-1">
                          <DollarSign className="w-3 h-3 text-emerald-500" />
                          {(movie.budget / 1000000).toFixed(1)}M
                        </span>
                      </div>
                    )}
                    {movie.revenue && movie.revenue > 0 && (
                      <div className="flex justify-between items-center">
                        <span className="text-white/40">Revenue</span>
                        <span className="font-mono text-white flex items-center gap-1">
                          <DollarSign className="w-3 h-3 text-emerald-500" />
                          {(movie.revenue / 1000000).toFixed(1)}M
                        </span>
                      </div>
                    )}
                  </div>

                  {movie.production_companies && movie.production_companies.length > 0 && (
                    <div className="pt-4 border-t border-white/10">
                      <span className="text-xs text-white/40 uppercase tracking-wider block mb-3">Production</span>
                      <div className="flex flex-wrap gap-2">
                        {movie.production_companies.map((company: any) => (
                          <span key={company.id} className="text-xs px-2 py-1 rounded bg-white/5 border border-white/5 text-text-secondary">
                            {company.name}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>
            </div>

          </div>
        </div>
      </section>

      {/* Similar Movies - Infinite Strip Style */}
      {similarMovies.length > 0 && (
        <section className="section-spacing pt-0 pb-24">
          <div className="container-padding">
            <div className="flex items-baseline justify-between mb-8 border-b border-white/5 pb-4">
              <h2 className="text-2xl font-bold font-headline">More Like This</h2>
            </div>
            <Suspense fallback={<div>Loading...</div>}>
              <MasonryGrid items={similarMovies} />
            </Suspense>
          </div>
        </section>
      )}
    </div>
  );
}
