'use client';

import { useState, useEffect } from 'react';
import { User, Calendar, Lock, Loader } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { userService, UserProfile } from '@/services/user.service';
import { formatDate, getInitials } from '@/lib/utils';
import { toast } from 'sonner';

interface UserProfilePageProps {
  params: {
    username: string;
  };
}

export default function UserProfilePage({ params }: UserProfilePageProps) {
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isPrivate, setIsPrivate] = useState(false);

  useEffect(() => {
    loadProfile();
  }, [params.username]);

  const loadProfile = async () => {
    try {
      setIsLoading(true);
      const data = await userService.getUserProfile(params.username);
      setProfile(data);
    } catch (error: any) {
      if (error.response?.status === 403) {
        setIsPrivate(true);
      } else {
        toast.error('Failed to load profile');
      }
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader className="h-8 w-8 animate-spin text-brand-primary" />
      </div>
    );
  }

  if (isPrivate) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Card variant="glass" className="max-w-md">
          <CardContent className="p-12 text-center">
            <Lock className="h-16 w-16 text-text-tertiary mx-auto mb-4" />
            <h1 className="text-2xl font-bold mb-2">Private Profile</h1>
            <p className="text-text-secondary">
              This user's profile is private
            </p>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Card variant="glass" className="max-w-md">
          <CardContent className="p-12 text-center">
            <User className="h-16 w-16 text-text-tertiary mx-auto mb-4" />
            <h1 className="text-2xl font-bold mb-2">User Not Found</h1>
            <p className="text-text-secondary">
              The user you're looking for doesn't exist
            </p>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen section-spacing">
      <div className="container-padding">
        {/* Profile Header */}
        <Card variant="glass">
          <CardContent className="p-8">
            <div className="flex flex-col md:flex-row items-center gap-6">
              {/* Avatar */}
              <div className="relative">
                {profile.avatar_url ? (
                  <img
                    src={profile.avatar_url}
                    alt={profile.username}
                    className="h-24 w-24 rounded-full object-cover"
                  />
                ) : (
                  <div className="h-24 w-24 rounded-full bg-brand-primary/20 flex items-center justify-center">
                    <span className="text-3xl font-bold text-brand-primary">
                      {getInitials(profile.full_name || profile.username)}
                    </span>
                  </div>
                )}
                {profile.is_premium && (
                  <Badge
                    variant="primary"
                    className="absolute -bottom-2 left-1/2 -translate-x-1/2"
                  >
                    Premium
                  </Badge>
                )}
              </div>

              {/* Info */}
              <div className="flex-1 text-center md:text-left">
                <div className="flex items-center gap-2 justify-center md:justify-start mb-2">
                  <h1 className="text-3xl font-bold">{profile.full_name || profile.username}</h1>
                  {profile.is_verified && (
                    <Badge variant="success">Verified</Badge>
                  )}
                </div>
                <p className="text-text-secondary mb-4">@{profile.username}</p>
                
                {profile.bio && (
                  <p className="text-text-secondary mb-4 max-w-2xl">{profile.bio}</p>
                )}

                <div className="flex items-center gap-2 text-sm text-text-tertiary justify-center md:justify-start">
                  <Calendar className="h-4 w-4" />
                  <span>Joined {formatDate(profile.created_at, 'short')}</span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Public Activity */}
        <div className="mt-8">
          <h2 className="text-2xl font-bold mb-4">Public Activity</h2>
          <Card variant="glass">
            <CardContent className="p-12 text-center">
              <p className="text-text-secondary">
                No public activity to display
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
