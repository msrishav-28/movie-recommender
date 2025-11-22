import { apiClient } from './api.client';
import type { AestheticSearchResult, AestheticFrame } from '@/types';

/**
 * Aesthetic Search Service
 */
export const aestheticService = {
  /**
   * Search movies by natural language aesthetic query
   */
  async searchByQuery(query: string, limit: number = 24): Promise<AestheticSearchResult[]> {
    return apiClient.get<AestheticSearchResult[]>(
      `/aesthetic-search?query=${encodeURIComponent(query)}&limit=${limit}`
    );
  },

  /**
   * Search movies by color palette
   */
  async searchByColor(colors: string[], limit: number = 24): Promise<AestheticSearchResult[]> {
    return apiClient.post<AestheticSearchResult[]>('/aesthetic-search/by-color', {
      colors,
      limit,
    });
  },

  /**
   * Search movies by reference image
   */
  async searchByImage(imageFile: File, limit: number = 24): Promise<AestheticSearchResult[]> {
    const formData = new FormData();
    formData.append('image', imageFile);
    formData.append('limit', limit.toString());

    return apiClient.post<AestheticSearchResult[]>('/aesthetic-search/by-image', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  /**
   * Get aesthetic frames for a movie
   */
  async getMovieFrames(movieId: number): Promise<AestheticFrame[]> {
    return apiClient.get<AestheticFrame[]>(`/aesthetic-search/frames/${movieId}`);
  },

  /**
   * Search movies with visual tags
   */
  async searchByTags(tags: string[], limit: number = 24): Promise<AestheticSearchResult[]> {
    return apiClient.post<AestheticSearchResult[]>('/aesthetic-search/by-tags', {
      tags,
      limit,
    });
  },

  /**
   * Get trending aesthetic searches
   */
  async getTrendingSearches(): Promise<string[]> {
    return apiClient.get<string[]>('/aesthetic-search/trending');
  },

  /**
   * Get suggested visual tags
   */
  async getSuggestedTags(): Promise<string[]> {
    return apiClient.get<string[]>('/aesthetic-search/suggested-tags');
  },
};
