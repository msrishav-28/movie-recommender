'use client';

import { Sparkles, TrendingUp, Clock, Heart } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { MovieGrid } from '@/components/movie/MovieGrid';
import { usePersonalizedRecommendations } from '@/hooks/useRecommendations';
import { useWatchlist } from '@/hooks/useWatchlist';
import { useAuth } from '@/hooks/useAuth';
import { useTrendingMovies } from '@/hooks/useMovies';
import Link from 'next/link';

export default function DashboardPage() {
  const { user } = useAuth();
  const { data: recommendations, isLoading: recsLoading } = usePersonalizedRecommendations(12);
  const { watchlist, isLoading: watchlistLoading } = useWatchlist();
  const { data: trending } = useTrendingMovies(1, 12);

  const stats = [
    {
      title: 'Movies Watched',
      value: watchlist?.filter((item) => item.watched).length || 0,
      icon: <Clock className="h-5 w-5" />,
      color: 'text-brand-primary',
    },
    {
      title: 'In Watchlist',
      value: watchlist?.length || 0,
      icon: <Heart className="h-5 w-5" />,
      color: 'text-semantic-success',
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
    <div className="min-h-screen">
      {/* Welcome Section */}
      <section className="bg-gradient-mesh py-12">
        <div className="container-padding">
          <div className="space-y-4">
            <h1 className="text-4xl md:text-5xl font-bold">
              Welcome back, <span className="text-brand-primary">{user?.username}</span>
            </h1>
            <p className="text-xl text-text-secondary">
              Your personalized movie discovery awaits
            </p>
          </div>
        </div>
      </section>

      {/* Stats Grid */}
      <section className="section-spacing">
        <div className="container-padding">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {stats.map((stat) => (
              <Card key={stat.title} variant="glass" hover>
                <CardContent className="p-6">
                  <div className="flex items-center justify-between mb-4">
                    <div className={stat.color}>{stat.icon}</div>
                  </div>
                  <div className="text-3xl font-bold mb-1">{stat.value}</div>
                  <div className="text-sm text-text-secondary">{stat.title}</div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Personalized Recommendations */}
      <section className="section-spacing bg-surface/50">
        <div className="container-padding">
          <div className="flex items-center justify-between mb-8">
            <div>
              <h2 className="text-3xl font-bold mb-2">Recommended For You</h2>
              <p className="text-text-secondary">Based on your taste and viewing history</p>
            </div>
            <Sparkles className="h-8 w-8 text-brand-primary" />
          </div>
          
          {recommendations && recommendations.length > 0 ? (
            <MovieGrid movies={recommendations} isLoading={recsLoading} size="medium" />
          ) : (
            <Card variant="glass">
              <CardContent className="p-12 text-center">
                <Sparkles className="h-16 w-16 mx-auto mb-4 text-text-tertiary" />
                <h3 className="text-xl font-bold mb-2">No recommendations yet</h3>
                <p className="text-text-secondary mb-4">
                  Rate some movies to get personalized recommendations
                </p>
                <Link href="/browse">
                  <Button variant="primary">Browse Movies</Button>
                </Link>
              </CardContent>
            </Card>
          )}
        </div>
      </section>

      {/* Continue Watching */}
      {watchlist && watchlist.length > 0 && (
        <section className="section-spacing">
          <div className="container-padding">
            <div className="flex items-center justify-between mb-8">
              <div>
                <h2 className="text-3xl font-bold mb-2">Your Watchlist</h2>
                <p className="text-text-secondary">Movies you've saved to watch</p>
              </div>
              <Link href="/watchlist">
                <Button variant="ghost">View All</Button>
              </Link>
            </div>

            <MovieGrid 
              movies={watchlist.slice(0, 6).map(item => item.movie)} 
              isLoading={watchlistLoading}
              size="medium" 
            />
          </div>
        </section>
      )}

      {/* Trending */}
      {trending && (
        <section className="section-spacing bg-surface/50">
          <div className="container-padding">
            <div className="flex items-center justify-between mb-8">
              <div>
                <h2 className="text-3xl font-bold mb-2">Trending Now</h2>
                <p className="text-text-secondary">What everyone's watching</p>
              </div>
              <Link href="/trending">
                <Button variant="ghost">View All</Button>
              </Link>
            </div>

            <MovieGrid movies={trending.items.slice(0, 6)} size="medium" />
          </div>
        </section>
      )}
    </div>
  );
}
