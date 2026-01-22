'use client';

import { useState } from 'react';
import { User, Mail, Calendar, Heart, Star, Film, Edit2, LogOut } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Tabs } from '@/components/ui/Tabs';
import { MasonryGrid } from '@/components/ui/MasonryGrid';
import { useAuth } from '@/hooks/useAuth';
import { useWatchlist } from '@/hooks/useWatchlist';
import Link from 'next/link';
import { motion } from 'framer-motion';

export default function ProfilePage() {
  const { user, logout } = useAuth();
  const { data: watchlistData } = useWatchlist();
  const watchlist = watchlistData?.items || [];

  const stats = [
    { label: 'Watched', value: watchlist?.filter((i) => i.watched).length || 0, icon: <Film className="h-4 w-4" /> },
    { label: 'Watchlist', value: watchlist?.length || 0, icon: <Heart className="h-4 w-4" /> },
    { label: 'Ratings', value: 0, icon: <Star className="h-4 w-4" /> },
    { label: 'Reviews', value: 0, icon: <Edit2 className="h-4 w-4" /> },
  ];

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-void">
        <Card variant="glass">
          <CardContent className="p-12 text-center">
            <User className="h-16 w-16 mx-auto mb-4 text-white/40" />
            <h3 className="text-2xl font-bold mb-2">Not logged in</h3>
            <p className="text-text-secondary mb-6">Please log in to view your profile</p>
            <Link href="/login">
              <Button variant="primary" size="lg" glow>
                Login
              </Button>
            </Link>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-void">
      {/* Sticky Header */}
      <motion.div
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        className="sticky top-[64px] z-30 z-header bg-void/80 backdrop-blur-md border-b border-white/5 shadow-lg"
      >
        <div className="container-padding py-6">
          <div className="flex flex-col md:flex-row items-center justify-between gap-6">
            <div className="flex items-center gap-6">
              <div className="w-16 h-16 rounded-full bg-gradient-to-br from-klein-blue to-electric-teal flex items-center justify-center text-2xl font-bold text-white shadow-glow">
                {user.username.charAt(0).toUpperCase()}
              </div>
              <div>
                <h1 className="text-3xl font-bold font-headline leading-none mb-1">{user.username}</h1>
                <div className="flex items-center gap-4 text-sm text-text-secondary font-mono">
                  <div className="flex items-center gap-2">
                    <Mail className="h-3 w-3" />
                    <span>{user.email}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Calendar className="h-3 w-3" />
                    <span>Joined {new Date(user.created_at).toLocaleDateString('en-US', { month: 'short', year: 'numeric' })}</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <Link href="/settings">
                <Button variant="outline" size="sm" icon={<Edit2 className="h-3 w-3" />}>
                  Edit
                </Button>
              </Link>
              <Button variant="ghost" size="sm" onClick={logout} icon={<LogOut className="h-3 w-3" />}>
                Logout
              </Button>
            </div>
          </div>

          {/* Quick Stats in Header */}
          <div className="flex items-center gap-8 mt-6 pt-4 border-t border-white/5">
            {stats.map((stat) => (
              <div key={stat.label} className="flex items-center gap-3">
                <div className="p-1.5 rounded bg-white/5 text-klein-blue">
                  {stat.icon}
                </div>
                <div className="flex flex-col">
                  <span className="text-lg font-bold leading-none">{stat.value}</span>
                  <span className="text-[10px] uppercase tracking-wider text-white/40">{stat.label}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </motion.div>

      {/* Content Tabs */}
      <section className="section-spacing pt-8">
        <div className="container-padding">
          <Tabs
            tabs={[
              {
                id: 'watchlist',
                label: 'Watchlist',
                icon: <Heart className="h-4 w-4" />,
                content: (
                  <div className="space-y-6">
                    {watchlist && watchlist.length > 0 ? (
                      <MasonryGrid
                        items={watchlist.map((item) => item.movie!).filter(Boolean)}
                      />
                    ) : (
                      <div className="flex flex-col items-center justify-center py-20 text-center opacity-50">
                        <Heart className="h-12 w-12 mb-4 text-white/40" />
                        <p className="text-lg">Your watchlist is empty</p>
                        <Link href="/browse" className="mt-4">
                          <Button variant="outline" size="sm">Browse Movies</Button>
                        </Link>
                      </div>
                    )}
                  </div>
                ),
              },
              {
                id: 'watched',
                label: 'Watched History',
                icon: <Film className="h-4 w-4" />,
                content: (
                  <div className="space-y-6">
                    {watchlist && watchlist.filter(i => i.watched).length > 0 ? (
                      <MasonryGrid
                        items={watchlist
                          .filter((item) => item.watched)
                          .map((item) => item.movie!)
                          .filter(Boolean)}
                      />
                    ) : (
                      <div className="flex flex-col items-center justify-center py-20 text-center opacity-50">
                        <Film className="h-12 w-12 mb-4 text-white/40" />
                        <p className="text-lg">No movies marked as watched yet</p>
                      </div>
                    )}
                  </div>
                ),
              },
              {
                id: 'ratings',
                label: 'My Ratings',
                icon: <Star className="h-4 w-4" />,
                content: (
                  <div className="flex flex-col items-center justify-center py-20 text-center opacity-50">
                    <Star className="h-12 w-12 mb-4 text-white/40" />
                    <p className="text-lg">No ratings yet</p>
                  </div>
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
