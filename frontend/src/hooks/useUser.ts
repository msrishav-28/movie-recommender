/**
 * User Profile and Preferences Hook
 * React Query hooks for user management
 */

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { 
  userService, 
  UserProfile, 
  UserPreferences,
  UpdateProfileRequest,
  UpdatePreferencesRequest 
} from '@/services/user.service';
import { toast } from 'sonner';

/**
 * Hook to get current user's profile
 */
export function useMyProfile() {
  return useQuery({
    queryKey: ['user', 'profile', 'me'],
    queryFn: () => userService.getMyProfile(),
  });
}

/**
 * Hook to get current user's preferences
 */
export function useMyPreferences() {
  return useQuery({
    queryKey: ['user', 'preferences', 'me'],
    queryFn: () => userService.getMyPreferences(),
  });
}

/**
 * Hook to get public user profile by username
 */
export function useUserProfile(username: string) {
  return useQuery({
    queryKey: ['user', 'profile', username],
    queryFn: () => userService.getUserProfile(username),
    enabled: !!username,
  });
}

/**
 * Hook to update profile
 */
export function useUpdateProfile() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: UpdateProfileRequest) => userService.updateProfile(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['user', 'profile', 'me'] });
      toast.success('Profile updated successfully!');
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to update profile');
    },
  });
}

/**
 * Hook to update preferences
 */
export function useUpdatePreferences() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: UpdatePreferencesRequest) => userService.updatePreferences(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['user', 'preferences', 'me'] });
      toast.success('Preferences updated successfully!');
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to update preferences');
    },
  });
}
