// Core type definitions matching backend schemas

export interface User {
  id: string;
  email: string;
  username: string;
  full_name?: string;
  bio?: string;
  avatar_url?: string;
  is_active: boolean;
  is_verified: boolean;
  is_premium: boolean;
  created_at: string;
}

export interface UserProfile extends User {
  ratings_count: number;
  reviews_count: number;
  watchlist_count: number;
  followers_count: number;
  following_count: number;
}

export interface Genre {
  id: number;
  name: string;
}

export interface CastMember {
  id: number;
  name: string;
  character?: string;
  profile_path?: string;
  order: number;
}

export interface CrewMember {
  id: number;
  name: string;
  job: string;
  department: string;
  profile_path?: string;
}

export interface Movie {
  id: number;
  title: string;
  original_title?: string;
  overview?: string;
  release_date?: string;
  poster_path?: string;
  backdrop_path?: string;
  genres: Genre[];
  vote_average?: number;
  vote_count: number;
  popularity: number;
  runtime?: number;
}

export interface MovieDetail extends Movie {
  tagline?: string;
  budget?: number;
  revenue?: number;
  original_language: string;
  spoken_languages: string[];
  production_countries: string[];
  cast: CastMember[];
  crew: CrewMember[];
  trailer_url?: string;
  imdb_id?: string;
  homepage?: string;
  status?: string;
  avg_rating?: number;
  ratings_count: number;
  avg_sentiment?: number;
  sentiment_distribution?: Record<string, number>;
}

export interface Rating {
  id: string;
  user_id: string;
  movie_id: number;
  overall_rating: number;
  plot_rating?: number;
  acting_rating?: number;
  cinematography_rating?: number;
  soundtrack_rating?: number;
  created_at: string;
  updated_at: string;
}

export interface Review {
  id: string;
  user_id: string;
  movie_id: number;
  rating: Rating;
  content: string;
  sentiment_score?: number;
  is_spoiler: boolean;
  likes_count: number;
  comments_count: number;
  created_at: string;
  updated_at: string;
  user?: User;
}

export interface WatchlistItem {
  id: string;
  user_id: string;
  movie_id: number;
  priority: 'low' | 'medium' | 'high';
  notes?: string;
  added_at: string;
  movie?: Movie;
}

export interface Recommendation {
  movie: Movie;
  score: number;
  explanation?: string;
  reasons: string[];
}

export interface AestheticSearchResult {
  movie: Movie;
  match_score: number;
  matched_frames: AestheticFrame[];
}

export interface AestheticFrame {
  frame_url: string;
  timestamp: number;
  color_palette: ColorPalette[];
  visual_tags: string[];
}

export interface ColorPalette {
  color: string;
  percentage: number;
}

export interface SearchFilters {
  query?: string;
  genres?: string[];
  min_year?: number;
  max_year?: number;
  min_rating?: number;
  max_rating?: number;
  min_runtime?: number;
  max_runtime?: number;
  languages?: string[];
  sort_by?: 'popularity' | 'rating' | 'release_date' | 'title';
  sort_order?: 'asc' | 'desc';
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface ApiError {
  detail: string;
  status_code: number;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  username: string;
  password: string;
  full_name?: string;
}

export interface UserPreferences {
  favorite_genres?: string[];
  disliked_genres?: string[];
  favorite_decades?: string[];
  preferred_languages?: string[];
  preferred_moods?: string[];
  diversity_preference?: number;
  include_adult_content?: boolean;
  min_rating_threshold?: number;
}

export interface StreamingService {
  id: string;
  name: string;
  logo_url: string;
  type: 'subscription' | 'rent' | 'buy';
}

export interface StreamingAvailability {
  movie_id: number;
  services: StreamingService[];
  last_updated: string;
}

export type ThemeMode = 'light' | 'dark' | 'system';

export type ToastType = 'success' | 'error' | 'warning' | 'info';
