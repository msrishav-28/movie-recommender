import { Suspense } from 'react';
import Link from 'next/link';
import { Film, Sparkles, TrendingUp, Search } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { MovieGrid } from '@/components/movie/MovieGrid';
import { movieService } from '@/services/movie.service';

async function getTrendingMovies() {
  try {
    const data = await movieService.getTrending(1, 12);
    return data.items;
  } catch (error) {
    console.error('Failed to fetch trending movies:', error);
    return [];
  }
}

async function getPopularMovies() {
  try {
    const data = await movieService.getPopular(1, 12);
    return data.items;
  } catch (error) {
    console.error('Failed to fetch popular movies:', error);
    return [];
  }
}

export default async function HomePage() {
  const trendingMovies = await getTrendingMovies();
  const popularMovies = await getPopularMovies();

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
        {/* Background gradient */}
        <div className="absolute inset-0 gradient-mesh opacity-50" />
        
        <div className="container-padding relative z-10 text-center">
          <div className="max-w-4xl mx-auto space-y-8">
            {/* Badge */}
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass-medium backdrop-blur-md border border-border">
              <Sparkles className="h-4 w-4 text-brand-primary" />
              <span className="text-sm font-medium">World's First Aesthetic Movie Search</span>
            </div>

            {/* Main Heading */}
            <h1 className="font-cinematic text-6xl sm:text-7xl md:text-8xl tracking-wider">
              DISCOVER MOVIES
              <br />
              <span className="text-brand-primary">BY VIBE</span>
            </h1>

            {/* Subtitle */}
            <p className="text-xl md:text-2xl text-text-secondary max-w-2xl mx-auto">
              Search for films by aesthetic atmosphere, visual mood, and cinematic vibes.
              Powered by AI.
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
              <Link href="/aesthetic">
                <Button size="lg" variant="primary" icon={<Sparkles className="h-5 w-5" />} glow>
                  Try Aesthetic Search
                </Button>
              </Link>
              <Link href="/browse">
                <Button size="lg" variant="glass" icon={<Search className="h-5 w-5" />}>
                  Browse Movies
                </Button>
              </Link>
            </div>

            {/* Example Queries */}
            <div className="pt-8">
              <p className="text-sm text-text-tertiary mb-4">Try searching for:</p>
              <div className="flex flex-wrap items-center justify-center gap-2">
                {[
                  'rain with neon lights',
                  'cozy autumn vibes',
                  'cyberpunk cityscape',
                  'dreamy sunset',
                  'dark mysterious atmosphere',
                ].map((query) => (
                  <Link key={query} href={`/aesthetic?q=${encodeURIComponent(query)}`}>
                    <span className="px-4 py-2 rounded-full glass-light hover:glass-medium cursor-pointer transition-all text-sm">
                      {query}
                    </span>
                  </Link>
                ))}
              </div>
            </div>

            {/* Scroll Indicator */}
            <div className="pt-16 animate-bounce-slow">
              <svg
                className="mx-auto h-6 w-6 text-text-tertiary"
                fill="none"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path d="M19 14l-7 7m0 0l-7-7m7 7V3"></path>
              </svg>
            </div>
          </div>
        </div>
      </section>

      {/* Value Proposition Section */}
      <section className="section-spacing">
        <div className="container-padding">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                icon: <Sparkles className="h-12 w-12" />,
                title: 'AI-Powered Search',
                description: 'Describe the vibe you want. Our AI finds movies that match your aesthetic.',
              },
              {
                icon: <Film className="h-12 w-12" />,
                title: 'Visual Discovery',
                description: 'Browse through movie frames and color palettes to find your perfect film.',
              },
              {
                icon: <TrendingUp className="h-12 w-12" />,
                title: 'Smart Recommendations',
                description: 'Get personalized suggestions based on your unique taste and viewing habits.',
              },
            ].map((feature, index) => (
              <div
                key={index}
                className="p-8 rounded-2xl glass-medium backdrop-blur-md hover:glass-heavy transition-all group"
              >
                <div className="text-brand-primary mb-4 group-hover:scale-110 transition-transform">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-bold mb-3">{feature.title}</h3>
                <p className="text-text-secondary">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Trending Movies Section */}
      <section className="section-spacing bg-surface/50">
        <div className="container-padding">
          <div className="flex items-center justify-between mb-8">
            <div>
              <h2 className="text-3xl md:text-4xl font-bold mb-2">Trending Now</h2>
              <p className="text-text-secondary">Popular movies this week</p>
            </div>
            <Link href="/trending">
              <Button variant="ghost">View All</Button>
            </Link>
          </div>
          
          <Suspense fallback={<div className="animate-pulse">Loading...</div>}>
            <MovieGrid movies={trendingMovies} size="medium" />
          </Suspense>
        </div>
      </section>

      {/* Popular Movies Section */}
      <section className="section-spacing">
        <div className="container-padding">
          <div className="flex items-center justify-between mb-8">
            <div>
              <h2 className="text-3xl md:text-4xl font-bold mb-2">Popular Movies</h2>
              <p className="text-text-secondary">Most watched by our community</p>
            </div>
            <Link href="/browse">
              <Button variant="ghost">Browse All</Button>
            </Link>
          </div>
          
          <Suspense fallback={<div className="animate-pulse">Loading...</div>}>
            <MovieGrid movies={popularMovies} size="medium" />
          </Suspense>
        </div>
      </section>

      {/* Final CTA Section */}
      <section className="section-spacing bg-gradient-to-r from-brand-primary to-brand-secondary">
        <div className="container-padding text-center">
          <div className="max-w-3xl mx-auto space-y-6">
            <h2 className="text-4xl md:text-5xl font-bold text-white">
              Start Discovering Your Next Favorite Film
            </h2>
            <p className="text-xl text-white/90">
              Join thousands of movie lovers finding films through aesthetic vibes
            </p>
            <div className="pt-4">
              <Link href="/register">
                <Button size="xl" variant="glass" className="bg-white/20 hover:bg-white/30">
                  Get Started Free
                </Button>
              </Link>
            </div>
            <p className="text-sm text-white/70">No credit card required</p>
          </div>
        </div>
      </section>
    </div>
  );
}
