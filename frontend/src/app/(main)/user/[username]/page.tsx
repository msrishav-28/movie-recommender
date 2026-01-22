'use client';

import { useState, useEffect } from 'react';
import { User, Calendar, Lock, Loader, Mail, Shield, Film, Star } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { userService, UserProfile } from '@/services/user.service';
import { formatDate, getInitials } from '@/lib/utils';
import { toast } from 'sonner';
import { motion, AnimatePresence } from 'framer-motion';
import { CinematicLoader } from '@/components/ui/CinematicLoader';

interface UserProfilePageProps {
  params: {
    username: string;
  };
}

// Stagger animation variants (VISUAL_DNA: Motion Choreography)
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.08,
      delayChildren: 0.1,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 30 },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.6,
      ease: [0.22, 1, 0.36, 1], // Quintic Out
    },
  },
};

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



  // ... (existing imports)

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-void">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="flex flex-col items-center gap-4"
        >
          <div className="relative">
            <CinematicLoader />
          </div>
        </motion.div>
      </div>
    );
  }

  if (isPrivate) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-void px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
        >
          <Card variant="glass" className="max-w-md">
            <CardContent className="p-12 text-center">
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 0.2, type: 'spring', stiffness: 200 }}
              >
                <Lock className="h-16 w-16 text-white/40 mx-auto mb-6" />
              </motion.div>
              <h1 className="text-3xl font-bold mb-3 font-cinematic tracking-wide">PRIVATE PROFILE</h1>
              <p className="text-text-secondary font-light">
                This user&apos;s profile is private
              </p>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-void px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
        >
          <Card variant="glass" className="max-w-md">
            <CardContent className="p-12 text-center">
              <User className="h-16 w-16 text-white/40 mx-auto mb-6" />
              <h1 className="text-3xl font-bold mb-3 font-cinematic tracking-wide">USER NOT FOUND</h1>
              <p className="text-text-secondary font-light">
                The user you&apos;re looking for doesn&apos;t exist
              </p>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-void">
      {/* Cinematic Header */}
      <motion.div
        initial={{ y: -100, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
        className="sticky top-[64px] z-30 bg-void/80 backdrop-blur-xl border-b border-white/5"
      >
        <div className="container-padding py-10">
          <motion.div
            className="flex flex-col md:flex-row items-center gap-8"
            variants={containerVariants}
            initial="hidden"
            animate="visible"
          >
            {/* Avatar with Glow */}
            <motion.div variants={itemVariants} className="relative group">
              {profile.avatar_url ? (
                <div className="relative">
                  <img
                    src={profile.avatar_url}
                    alt={profile.username}
                    className="h-28 w-28 rounded-full object-cover ring-2 ring-white/10 group-hover:ring-electric-teal/50 transition-all duration-500"
                  />
                  <div className="absolute inset-0 rounded-full bg-electric-teal/20 blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                </div>
              ) : (
                <div className="relative">
                  <div className="h-28 w-28 rounded-full bg-gradient-to-br from-electric-teal via-klein-blue to-electric-teal flex items-center justify-center shadow-lg">
                    <span className="text-4xl font-bold text-white font-headline">
                      {getInitials(profile.full_name || profile.username)}
                    </span>
                  </div>
                  <div className="absolute inset-0 rounded-full bg-klein-blue/30 blur-2xl" />
                </div>
              )}
              {profile.is_verified && (
                <motion.div
                  className="absolute -bottom-1 -right-1 bg-emerald-500 text-black p-1.5 rounded-full border-2 border-void"
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 0.5, type: 'spring', stiffness: 300 }}
                >
                  <Shield className="w-4 h-4 fill-current" />
                </motion.div>
              )}
            </motion.div>

            <div className="flex-1 text-center md:text-left">
              {/* Cinematic Name Display */}
              <motion.h1
                variants={itemVariants}
                className="text-5xl md:text-6xl font-cinematic leading-none mb-2 tracking-wide"
              >
                {(profile.full_name || profile.username).toUpperCase()}
              </motion.h1>

              <motion.p
                variants={itemVariants}
                className="text-lg text-electric-teal font-mono mb-4"
              >
                @{profile.username}
              </motion.p>

              {profile.bio && (
                <motion.p
                  variants={itemVariants}
                  className="text-text-secondary max-w-xl mb-4 italic font-light"
                >
                  &quot;{profile.bio}&quot;
                </motion.p>
              )}

              <motion.div
                variants={itemVariants}
                className="flex items-center justify-center md:justify-start gap-6 text-xs text-text-tech font-mono tracking-widest uppercase"
              >
                <span className="flex items-center gap-2">
                  <Calendar className="w-3 h-3 text-klein-blue" />
                  Joined {formatDate(profile.created_at, 'short')}
                </span>
              </motion.div>
            </div>
          </motion.div>
        </div>
      </motion.div>

      <div className="container-padding section-spacing">
        {/* Public Activity Section */}
        <motion.div
          className="mt-8"
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4, duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
        >
          <div className="flex items-baseline justify-between mb-8 border-b border-white/10 pb-4">
            <h2 className="text-2xl font-bold font-headline">Public Activity</h2>
            <span className="font-mono text-xs text-text-tech">SECTION: 01 // ACTIVITY</span>
          </div>

          <Card variant="glass" hover>
            <CardContent className="p-16 text-center">
              <motion.div
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 0.4, scale: 1 }}
                transition={{ delay: 0.6, duration: 0.4 }}
              >
                <Film className="h-16 w-16 mx-auto mb-6 text-white/30" />
              </motion.div>
              <p className="text-xl font-mono text-text-secondary mb-2">
                No Activity Yet
              </p>
              <p className="text-sm text-text-tech">
                This user hasn&apos;t rated or reviewed any films
              </p>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </div>
  );
}
