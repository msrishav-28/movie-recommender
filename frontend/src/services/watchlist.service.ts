/**
 * Watchlist Service
 * Handles all watchlist operations matching backend schema
 */

import { apiClient } from './api.client';
import {
  WatchlistItemCreate,
  WatchlistItemUpdate,
  WatchlistItem,
  WatchlistItemWithMovie,
  WatchlistResponse,
  WatchlistStats,
} from '@/types/api.types';

export const watchlistService = {
  /**
   * Get user's watchlist with filters
   */
  async getWatchlist(
    watched?: boolean,
    sortBy: 'priority' | 'added_at' = 'priority',
    page: number = 1,
    pageSize: number = 20
  ): Promise<WatchlistResponse> {
    const response = await apiClient.get('/watchlist', {
      params: {
        watched,
        sort_by: sortBy,
        page,
        page_size: pageSize,
      },
    });
    return response.data;
  },

  /**
   * Add movie to watchlist
   */
  async addToWatchlist(data: WatchlistItemCreate): Promise<WatchlistItem> {
    const response = await apiClient.post('/watchlist', data);
    return response.data;
  },

  /**
   * Update watchlist item
   */
  async updateWatchlistItem(
    itemId: number,
    data: WatchlistItemUpdate
  ): Promise<WatchlistItem> {
    const response = await apiClient.put(`/watchlist/${itemId}`, data);
    return response.data;
  },

  /**
   * Remove from watchlist
   */
  async removeFromWatchlist(itemId: number): Promise<void> {
    await apiClient.delete(`/watchlist/${itemId}`);
  },

  /**
   * Mark as watched
   */
  async markAsWatched(itemId: number): Promise<WatchlistItem> {
    return this.updateWatchlistItem(itemId, { watched: true });
  },

  /**
   * Mark as unwatched
   */
  async markAsUnwatched(itemId: number): Promise<WatchlistItem> {
    return this.updateWatchlistItem(itemId, { watched: false });
  },

  /**
   * Get watchlist statistics
   */
  async getWatchlistStats(): Promise<WatchlistStats> {
    const response = await apiClient.get('/watchlist/stats');
    return response.data;
  },

  /**
   * Check if movie is in watchlist
   */
  async isInWatchlist(movieId: number): Promise<boolean> {
    try {
      const response = await apiClient.get(`/watchlist/check/${movieId}`);
      return response.data.in_watchlist;
    } catch (error) {
      return false;
    }
  },

  /**
   * Bulk operations
   */
  async bulkOperation(
    movieIds: number[],
    operation: 'add' | 'remove' | 'mark_watched'
  ): Promise<{ success: number; failed: number }> {
    const response = await apiClient.post('/watchlist/bulk', {
      movie_ids: movieIds,
      operation,
    });
    return response.data;
  },
};
