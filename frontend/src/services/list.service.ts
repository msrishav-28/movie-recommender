/**
 * Custom Lists Service
 * Handles creating and managing custom movie lists
 */

import { apiClient } from './api.client';

// Types
export interface CreateListRequest {
  name: string;
  description?: string;
  is_public: boolean;
}

export interface UserList {
  id: number;
  name: string;
  description?: string;
  is_public: boolean;
  likes_count: number;
  created_at: string;
}

export interface AddToListRequest {
  movie_id: number;
  notes?: string;
}

export const listService = {
  /**
   * Create a new custom list
   */
  async createList(data: CreateListRequest): Promise<UserList> {
    const response = await apiClient.post('/watchlist/lists', data);
    return response.data;
  },

  /**
   * Get current user's lists
   */
  async getMyLists(): Promise<UserList[]> {
    const response = await apiClient.get('/watchlist/lists');
    return response.data;
  },

  /**
   * Add movie to a list
   */
  async addToList(listId: number, data: AddToListRequest): Promise<void> {
    await apiClient.post(`/watchlist/lists/${listId}/items`, null, {
      params: data,
    });
  },

  /**
   * Delete a list
   */
  async deleteList(listId: number): Promise<void> {
    await apiClient.delete(`/watchlist/lists/${listId}`);
  },
};
