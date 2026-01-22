'use client';

import { Sparkles, TrendingUp, Clock, Heart } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { MasonryGrid } from '@/components/ui/MasonryGrid';
import { usePersonalizedRecommendations } from '@/hooks/useRecommendations';
import { useWatchlist } from '@/hooks/useWatchlist';
import { useAuth } from '@/hooks/useAuth';
import { useTrendingMovies } from '@/hooks/useMovies';
import Link from 'next/link';

export default function DashboardPage() {
  const { user } = useAuth();
  const { data: recommendations, isLoading: recsLoading } = usePersonalizedRecommendations(12);
  const { data: watchlistData, isLoading: watchlistLoading } = useWatchlist();
  const watchlist = watchlistData?.items || [];
  const { data: trending } = useTrendingMovies(1, 12);

  const stats = [
    {
      title: 'Movies Watched',
      value: watchlist?.filter((item) => item.watched).length || 0,
      icon: <Clock className="h-5 w-5" />,
      color: 'text-klein-blue',
    },
    {
      title: 'In Watchlist',
      value: watchlist?.length || 0,
      icon: <Heart className="h-5 w-5" />,
      color: 'text-emerald-500',
    },
    {
      title: 'Recommendations',
      value: recommendations?.length || 0,
      icon: <Sparkles className="h-5 w-5" />,
      color: 'text-brand-secondary',
    },
    {
      title: 'Ratings Given',
      value: 0, // TODO: Implement ratings count
      icon: <TrendingUp className="h-5 w-5" />,
      color: 'text-brand-tertiary',
    },
  ];

  return (
    <div className="min-h-screen bg-void">
      {/* Welcome Section */}
      <section className="relative py-12 md:py-20 overflow-hidden">
        {/* Cinematic Background Elements */}
        <div className="absolute inset-0 bg-void/50 backdrop-blur-3xl z-0" />
        <div className="absolute top-0 right-0 w-1/2 h-full bg-klein-blue/10 blur-[120px] rounded-full opacity-30 pointer-events-none" />

        <div className="container-padding relative z-10">
          <div className="space-y-4 max-w-4xl">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-white/10 bg-white/5 backdrop-blur-md shadow-glow animate-fade-in mb-4">
              <Sparkles className="h-4 w-4 text-klein-blue" />
              <span className="text-sm font-medium font-mono text-klein-blue tracking-wide uppercase">Your Personal Theater</span>
            </div>
            <h1 className="text-4xl md:text-6xl font-bold font-headline leading-tight">
              Welcome back, <span className="text-transparent bg-clip-text bg-gradient-to-r from-klein-blue to-electric-teal">{user?.username}</span>
            </h1>
            <p className="text-xl text-text-secondary font-light max-w-2xl">
              Your personalized movie discovery awaits. Dive back into your collection or explore new worlds.
            </p>
          </div>
        </div>
      </section>

      {/* Stats Grid (Bento Style) */}
      <section className="section-spacing">
        <div className="container-padding">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 auto-rows-[160px]">
            {/* Main Key Metric - Movies Watched (Large) */}
            <Card variant="glass" hover className="md:col-span-2 relative overflow-hidden group">
              <div className="absolute inset-0 bg-gradient-to-br from-klein-blue/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
              <CardContent className="h-full flex flex-col justify-between p-8 relative z-10">
                <div className="flex items-center justify-between">
                  <div className="text-klein-blue bg-klein-blue/10 p-3 rounded-xl">
                    <Clock className="h-6 w-6" />
                  </div>
                  <span className="text-xs font-mono text-klein-blue/80 uppercase tracking-widest border border-klein-blue/20 px-2 py-1 rounded">
                    Total Runtime
                  </span>
                </div>
                <div>
                  <div className="text-5xl font-bold mb-1 tracking-tight text-white">{watchlist?.filter((item) => item.watched).length || 0}</div>
                  <div className="text-lg text-text-secondary font-medium">Movies Watched</div>
                </div>
              </CardContent>
            </Card>

            {/* In Watchlist (Tall/Vertical) for visual variation? No, keep standard for now, maybe square */}
            <Card variant="glass" hover className="md:col-span-1 md:row-span-1 relative group">
              <CardContent className="h-full flex flex-col justify-center items-center p-6 text-center">
                <div className="text-emerald-500 mb-4 group-hover:scale-110 transition-transform duration-300">
                  <Heart className="h-8 w-8" />
                </div>
                <div className="text-3xl font-bold text-white mb-1">{watchlist?.length || 0}</div>
                <div className="text-xs text-text-secondary uppercase tracking-wider font-mono">Watchlist</div>
              </CardContent>
            </Card>

            {/* Recommendations (Square) */}
            <Card variant="glass" hover className="md:col-span-1 relative group">
              <CardContent className="h-full flex flex-col justify-center items-center p-6 text-center">
                <div className="text-brand-secondary mb-4 group-hover:rotate-12 transition-transform duration-300">
                  <Sparkles className="h-8 w-8" />
                </div>
                <div className="text-3xl font-bold text-white mb-1">{recommendations?.length || 0}</div>
                <div className="text-xs text-text-secondary uppercase tracking-wider font-mono">For You</div>
              </CardContent>
            </Card>

            {/* Ratings (Wide bottom) - Optional, or fit into 4th slot. Let's make it a long distinct bar? Or just fill the grid.
                 Actually, we have 4 cols.
                 [ 2 ] [ 1 ] [ 1 ]
                 Let's add a "Activity Map" or something later. For now, just another card.
             */}
            <Card variant="glass" hover className="md:col-span-4 relative overflow-hidden group">
              <div className="absolute inset-0 bg-gradient-to-r from-brand-tertiary/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
              <CardContent className="h-full flex items-center justify-between p-6 px-12">
                <div className="flex items-center gap-4">
                  <div className="text-brand-tertiary bg-brand-tertiary/10 p-2 rounded-lg">
                    <TrendingUp className="h-5 w-5" />
                  </div>
                  <div>
                    <div className="text-xl font-bold text-white">Ratings & Reviews</div>
                    <div className="text-sm text-text-secondary">Contribute to get better recommendations</div>
                  </div>
                </div>
                <div className="text-3xl font-bold text-white">0</div>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Personalized Recommendations */}
      <section className="section-spacing relative z-10">
        <div className="container-padding">
          <div className="flex items-center justify-between mb-8 border-b border-white/5 pb-4">
            <div>
              <h2 className="text-3xl font-bold mb-2 font-headline">Recommended For You</h2>
              <p className="text-text-secondary font-mono text-sm">Based on your taste and viewing history</p>
            </div>
            <Sparkles className="h-6 w-6 text-klein-blue" />
          </div>

          {recommendations && recommendations.length > 0 ? (
            <MasonryGrid items={recommendations.map(r => r.movie!)} />
          ) : (
            <Card variant="glass">
              <CardContent className="p-12 text-center">
                <Sparkles className="h-16 w-16 mx-auto mb-4 text-white/40" />
                <h3 className="text-xl font-bold mb-2">No recommendations yet</h3>
                <p className="text-text-secondary mb-4">
                  Rate some movies to get personalized recommendations
                </p>
                <Link href="/browse">
                  <Button variant="primary" glow>Browse Movies</Button>
                </Link>
              </CardContent>
            </Card>
          )}
        </div>
      </section>

      {/* Continue Watching */}
      {watchlist && watchlist.length > 0 && (
        <section className="section-spacing pt-0">
          <div className="container-padding">
            <div className="flex items-center justify-between mb-8 border-b border-white/5 pb-4">
              <div>
                <h2 className="text-3xl font-bold mb-2 font-headline">Your Watchlist</h2>
                <p className="text-text-secondary font-mono text-sm">Movies you&apos;ve saved to watch</p>
              </div>
              <Link href="/watchlist">
                <Button variant="ghost" size="sm">View All</Button>
              </Link>
            </div>

            <MasonryGrid items={watchlist.slice(0, 6).map(item => item.movie)} />
          </div>
        </section>
      )}

      {/* Trending */}
      {trending && (
        <section className="section-spacing pt-0 pb-24">
          <div className="container-padding">
            <div className="flex items-center justify-between mb-8 border-b border-white/5 pb-4">
              <div>
                <h2 className="text-3xl font-bold mb-2 font-headline">Trending Now</h2>
                <p className="text-text-secondary font-mono text-sm">What everyone&apos;s watching</p>
              </div>
              <Link href="/trending">
                <Button variant="ghost" size="sm">View All</Button>
              </Link>
            </div>

            <MasonryGrid items={trending.items.slice(0, 6)} />
          </div>
        </section>
      )}
    </div>
  );
}
