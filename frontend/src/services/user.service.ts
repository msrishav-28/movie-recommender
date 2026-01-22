/**
 * User Service
 * Handles user profile and preferences
 */

import { apiClient } from './api.client';

// Types
export interface UserProfile {
  id: string;
  email: string;
  username: string;
  full_name?: string;
  bio?: string;
  avatar_url?: string;
  is_verified: boolean;
  is_premium: boolean;
  created_at: string;
}

export interface UpdateProfileRequest {
  full_name?: string;
  bio?: string;
  avatar_url?: string;
}

export interface UserPreferences {
  favorite_genres: string[];
  disliked_genres: string[];
  preferred_moods?: string[];
  diversity_preference: number;
  profile_public: boolean;
}

export interface UpdatePreferencesRequest {
  favorite_genres?: string[];
  disliked_genres?: string[];
  preferred_moods?: string[];
  diversity_preference?: number;
  profile_public?: boolean;
}

export const userService = {
  /**
   * Get current user's profile
   */
  async getMyProfile(): Promise<UserProfile> {
    return await apiClient.get<UserProfile>('/users/me/profile');
  },

  /**
   * Update current user's profile
   */
  async updateProfile(data: UpdateProfileRequest): Promise<UserProfile> {
    return await apiClient.put<UserProfile>('/users/me/profile', data);
  },

  /**
   * Get current user's preferences
   */
  async getMyPreferences(): Promise<UserPreferences> {
    return await apiClient.get<UserPreferences>('/users/me/preferences');
  },

  /**
   * Update current user's preferences
   */
  async updatePreferences(data: UpdatePreferencesRequest): Promise<UserPreferences> {
    return await apiClient.put<UserPreferences>('/users/me/preferences', data);
  },

  /**
   * Get public user profile by username
   */
  async getUserProfile(username: string): Promise<UserProfile> {
    return await apiClient.get<UserProfile>(`/users/${username}`);
  },
};
