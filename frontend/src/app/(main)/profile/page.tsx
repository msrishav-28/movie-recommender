'use client';

import { useState } from 'react';
import { User, Mail, Calendar, Heart, Star, Film, Edit2 } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { Tabs } from '@/components/ui/Tabs';
import { MovieGrid } from '@/components/movie/MovieGrid';
import { useAuth } from '@/hooks/useAuth';
import { useWatchlist } from '@/hooks/useWatchlist';
import Link from 'next/link';

export default function ProfilePage() {
  const { user } = useAuth();
  const { watchlist } = useWatchlist();
  const [isEditing, setIsEditing] = useState(false);

  const stats = [
    { label: 'Movies Watched', value: watchlist?.filter((i) => i.watched).length || 0, icon: <Film className="h-5 w-5" /> },
    { label: 'Watchlist', value: watchlist?.length || 0, icon: <Heart className="h-5 w-5" /> },
    { label: 'Ratings', value: 0, icon: <Star className="h-5 w-5" /> },
    { label: 'Reviews', value: 0, icon: <Edit2 className="h-5 w-5" /> },
  ];

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Card variant="glass">
          <CardContent className="p-12 text-center">
            <User className="h-16 w-16 mx-auto mb-4 text-text-tertiary" />
            <h3 className="text-2xl font-bold mb-2">Not logged in</h3>
            <p className="text-text-secondary mb-6">Please log in to view your profile</p>
            <Link href="/login">
              <Button variant="primary" size="lg">
                Login
              </Button>
            </Link>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      {/* Profile Header */}
      <section className="bg-gradient-mesh py-12">
        <div className="container-padding">
          <div className="flex flex-col md:flex-row items-start gap-6">
            {/* Avatar */}
            <div className="w-32 h-32 rounded-full bg-gradient-to-br from-brand-primary to-brand-secondary flex items-center justify-center text-4xl font-bold text-white">
              {user.username.charAt(0).toUpperCase()}
            </div>

            {/* Info */}
            <div className="flex-1">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h1 className="text-4xl font-bold mb-2">{user.username}</h1>
                  <div className="flex items-center gap-2 text-text-secondary">
                    <Mail className="h-4 w-4" />
                    <span>{user.email}</span>
                  </div>
                </div>
                <Link href="/settings">
                  <Button variant="outline" icon={<Edit2 className="h-4 w-4" />}>
                    Edit Profile
                  </Button>
                </Link>
              </div>

              <div className="flex items-center gap-2 mb-4">
                <Calendar className="h-4 w-4 text-text-tertiary" />
                <span className="text-sm text-text-secondary">
                  Member since {new Date(user.created_at).toLocaleDateString('en-US', { month: 'long', year: 'numeric' })}
                </span>
              </div>

              {/* Stats */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
                {stats.map((stat) => (
                  <div key={stat.label} className="text-center">
                    <div className="flex items-center justify-center mb-2 text-brand-primary">
                      {stat.icon}
                    </div>
                    <div className="text-2xl font-bold">{stat.value}</div>
                    <div className="text-xs text-text-secondary">{stat.label}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Content Tabs */}
      <section className="section-spacing">
        <div className="container-padding">
          <Tabs
            tabs={[
              {
                id: 'watchlist',
                label: 'Watchlist',
                icon: <Heart className="h-5 w-5" />,
                content: (
                  <div className="space-y-6">
                    {watchlist && watchlist.length > 0 ? (
                      <>
                        <div className="flex justify-between items-center">
                          <p className="text-text-secondary">
                            {watchlist.length} movies in your watchlist
                          </p>
                          <Link href="/watchlist">
                            <Button variant="ghost">View All</Button>
                          </Link>
                        </div>
                        <MovieGrid
                          movies={watchlist.slice(0, 12).map((item) => item.movie)}
                          size="medium"
                        />
                      </>
                    ) : (
                      <Card variant="glass">
                        <CardContent className="p-12 text-center">
                          <Heart className="h-16 w-16 mx-auto mb-4 text-text-tertiary" />
                          <h3 className="text-xl font-bold mb-2">No movies in watchlist</h3>
                          <p className="text-text-secondary mb-4">
                            Start adding movies you want to watch
                          </p>
                          <Link href="/browse">
                            <Button variant="primary">Browse Movies</Button>
                          </Link>
                        </CardContent>
                      </Card>
                    )}
                  </div>
                ),
              },
              {
                id: 'watched',
                label: 'Watched',
                icon: <Film className="h-5 w-5" />,
                content: (
                  <div className="space-y-6">
                    {watchlist && watchlist.filter((i) => i.watched).length > 0 ? (
                      <MovieGrid
                        movies={watchlist
                          .filter((item) => item.watched)
                          .map((item) => item.movie)}
                        size="medium"
                      />
                    ) : (
                      <Card variant="glass">
                        <CardContent className="p-12 text-center">
                          <Film className="h-16 w-16 mx-auto mb-4 text-text-tertiary" />
                          <h3 className="text-xl font-bold mb-2">No watched movies yet</h3>
                          <p className="text-text-secondary">
                            Mark movies as watched from your watchlist
                          </p>
                        </CardContent>
                      </Card>
                    )}
                  </div>
                ),
              },
              {
                id: 'ratings',
                label: 'Ratings',
                icon: <Star className="h-5 w-5" />,
                content: (
                  <Card variant="glass">
                    <CardContent className="p-12 text-center">
                      <Star className="h-16 w-16 mx-auto mb-4 text-text-tertiary" />
                      <h3 className="text-xl font-bold mb-2">No ratings yet</h3>
                      <p className="text-text-secondary">
                        Start rating movies to get better recommendations
                      </p>
                    </CardContent>
                  </Card>
                ),
              },
              {
                id: 'reviews',
                label: 'Reviews',
                icon: <Edit2 className="h-5 w-5" />,
                content: (
                  <Card variant="glass">
                    <CardContent className="p-12 text-center">
                      <Edit2 className="h-16 w-16 mx-auto mb-4 text-text-tertiary" />
                      <h3 className="text-xl font-bold mb-2">No reviews yet</h3>
                      <p className="text-text-secondary">
                        Share your thoughts about movies you've watched
                      </p>
                    </CardContent>
                  </Card>
                ),
              },
            ]}
            defaultTab="watchlist"
            variant="pills"
          />
        </div>
      </section>
    </div>
  );
}
