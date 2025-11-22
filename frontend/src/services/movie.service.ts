import { apiClient } from './api.client';
import type {
  Movie,
  MovieDetail,
  SearchFilters,
  PaginatedResponse,
  StreamingAvailability,
} from '@/types';

/**
 * Movie Service
 */
export const movieService = {
  /**
   * Search movies with filters
   */
  async searchMovies(
    filters: SearchFilters,
    page: number = 1,
    pageSize: number = 24
  ): Promise<PaginatedResponse<Movie>> {
    const params = new URLSearchParams({
      page: page.toString(),
      page_size: pageSize.toString(),
      ...Object.fromEntries(
        Object.entries(filters).filter(([_, value]) => value !== undefined && value !== null)
      ),
    });

    return apiClient.get<PaginatedResponse<Movie>>(`/movies/search?${params}`);
  },

  /**
   * Get movie details by ID
   */
  async getMovieById(id: number): Promise<MovieDetail> {
    return apiClient.get<MovieDetail>(`/movies/${id}`);
  },

  /**
   * Get trending movies
   */
  async getTrending(page: number = 1, pageSize: number = 24): Promise<PaginatedResponse<Movie>> {
    return apiClient.get<PaginatedResponse<Movie>>(
      `/movies/trending?page=${page}&page_size=${pageSize}`
    );
  },

  /**
   * Get popular movies
   */
  async getPopular(page: number = 1, pageSize: number = 24): Promise<PaginatedResponse<Movie>> {
    return apiClient.get<PaginatedResponse<Movie>>(
      `/movies/popular?page=${page}&page_size=${pageSize}`
    );
  },

  /**
   * Get top rated movies
   */
  async getTopRated(page: number = 1, pageSize: number = 24): Promise<PaginatedResponse<Movie>> {
    return apiClient.get<PaginatedResponse<Movie>>(
      `/movies/top-rated?page=${page}&page_size=${pageSize}`
    );
  },

  /**
   * Get upcoming movies
   */
  async getUpcoming(page: number = 1, pageSize: number = 24): Promise<PaginatedResponse<Movie>> {
    return apiClient.get<PaginatedResponse<Movie>>(
      `/movies/upcoming?page=${page}&page_size=${pageSize}`
    );
  },

  /**
   * Get movies by genre
   */
  async getByGenre(
    genreId: number,
    page: number = 1,
    pageSize: number = 24
  ): Promise<PaginatedResponse<Movie>> {
    return apiClient.get<PaginatedResponse<Movie>>(
      `/movies/genre/${genreId}?page=${page}&page_size=${pageSize}`
    );
  },

  /**
   * Get streaming availability for a movie
   */
  async getStreamingAvailability(movieId: number): Promise<StreamingAvailability> {
    return apiClient.get<StreamingAvailability>(`/streaming/${movieId}`);
  },

  /**
   * Get all genres
   */
  async getGenres(): Promise<any[]> {
    return apiClient.get<any[]>('/movies/genres');
  },
};
