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
    return await apiClient.get<WatchlistResponse>('/watchlist', {
      params: {
        watched,
        sort_by: sortBy,
        page,
        page_size: pageSize,
      },
    });
  },

  /**
   * Add movie to watchlist
   */
  async addToWatchlist(data: WatchlistItemCreate): Promise<WatchlistItem> {
    return await apiClient.post<WatchlistItem>('/watchlist', data);
  },

  /**
   * Update watchlist item
   */
  async updateWatchlistItem(
    itemId: number,
    data: WatchlistItemUpdate
  ): Promise<WatchlistItem> {
    return await apiClient.put<WatchlistItem>(`/watchlist/${itemId}`, data);
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
    return await apiClient.get<WatchlistStats>('/watchlist/stats');
  },

  /**
   * Check if movie is in watchlist
   */
  async isInWatchlist(movieId: number): Promise<boolean> {
    try {
      const response = await apiClient.get<{ in_watchlist: boolean }>(`/watchlist/check/${movieId}`);
      return response.in_watchlist;
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
    return await apiClient.post<{ success: number; failed: number }>('/watchlist/bulk', {
      movie_ids: movieIds,
      operation,
    });
  },
};
