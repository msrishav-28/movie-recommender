/**
 * API Types
 * TypeScript types matching backend Pydantic schemas
 */

// ============================================================================
// Common Types
// ============================================================================

export interface TimestampMixin {
  created_at: string;
  updated_at?: string;
}

// ============================================================================
// Movie Types
// ============================================================================

export interface Genre {
  id: number;
  name: string;
}

export interface CastMember {
  id: number;
  name: string;
  character?: string;
  profile_path?: string;
  order?: number;
}

export interface CrewMember {
  id: number;
  name: string;
  job: string;
  department?: string;
  profile_path?: string;
}

export interface Movie {
  id: number;
  title: string;
  original_title?: string;
  overview?: string;
  release_date?: string;
  runtime?: number;
  vote_average?: number;
  vote_count?: number;
  popularity?: number;
  poster_path?: string;
  backdrop_path?: string;
  genres: Genre[];
  cast?: CastMember[];
  crew?: CrewMember[];
  tagline?: string;
  status?: string;
  original_language?: string;
  budget?: number;
  revenue?: number;
}

// ============================================================================
// Rating & Review Types
// ============================================================================

export interface RatingCreate {
  movie_id: number;
  overall_rating: number; // 0-5
  plot_rating?: number;
  acting_rating?: number;
  cinematography_rating?: number;
  soundtrack_rating?: number;
}

export interface Rating extends TimestampMixin {
  id: number;
  user_id: string;
  movie_id: number;
  overall_rating: number;
  plot_rating?: number;
  acting_rating?: number;
  cinematography_rating?: number;
  soundtrack_rating?: number;
}

export interface ReviewCreate {
  movie_id: number;
  rating_id?: number;
  title?: string;
  content: string;
  is_spoiler: boolean;
}

export interface Review extends TimestampMixin {
  id: number;
  user_id: string;
  movie_id: number;
  rating_id?: number;
  title?: string;
  content: string;
  is_spoiler: boolean;
  sentiment_score?: number;
  sentiment_label?: string;
  sentiment_confidence?: number;
  emotions?: Record<string, number>;
  aspect_sentiments?: Record<string, number>;
  likes_count: number;
  comments_count: number;
  helpful_count: number;
  not_helpful_count: number;
  is_verified_watch: boolean;
  is_flagged: boolean;
  is_hidden: boolean;
}

export interface ReviewWithUser extends Review {
  username: string;
  user_avatar?: string;
}

export interface MovieRatingsAggregate {
  movie_id: number;
  avg_overall_rating: number;
  avg_plot_rating?: number;
  avg_acting_rating?: number;
  avg_cinematography_rating?: number;
  avg_soundtrack_rating?: number;
  ratings_count: number;
  rating_distribution: Record<number, number>;
}

// ============================================================================
// Watchlist Types
// ============================================================================

export interface WatchlistItemCreate {
  movie_id: number;
  priority?: number; // 1-5
  notes?: string;
}

export interface WatchlistItemUpdate {
  priority?: number;
  notes?: string;
  watched?: boolean;
}

export interface WatchlistItem extends TimestampMixin {
  id: number;
  user_id: string;
  movie_id: number;
  priority?: number;
  notes?: string;
  watched: boolean;
  watched_at?: string;
}

export interface WatchlistItemWithMovie extends WatchlistItem {
  movie: Movie;
}

export interface WatchlistResponse {
  items: WatchlistItemWithMovie[];
  total_count: number;
  watched_count: number;
  unwatched_count: number;
}

export interface WatchlistStats {
  total_items: number;
  watched: number;
  unwatched: number;
  avg_priority?: number;
  genre_distribution: Record<string, number>;
  decade_distribution: Record<string, number>;
}

// ============================================================================
// Recommendation Types
// ============================================================================

export interface RecommendationRequest {
  top_k?: number; // default 20
  diversity?: number; // 0-1
  mood?: string;
  genres?: string[];
  min_year?: number;
  max_year?: number;
  exclude_watched?: boolean;
  context?: Record<string, any>;
}

export interface Recommendation {
  movie_id: number;
  score: number;
  components: Record<string, number>;
  explanation: string;
  confidence: number;
  metadata?: Record<string, any>;
}

export interface RecommendationsListResponse {
  recommendations: Recommendation[];
  generated_at: string;
  algorithm_version: string;
  diversity_score?: number;
  total_candidates?: number;
}

export interface RecommendationFeedback {
  movie_id: number;
  accepted: boolean;
  feedback_type?: 'clicked' | 'watched' | 'rated' | 'dismissed' | 'disliked';
  context?: Record<string, any>;
}

// ============================================================================
// User Types
// ============================================================================

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
  diversity_preference: number; // 0-10
  profile_public: boolean;
}

export interface UpdatePreferencesRequest {
  favorite_genres?: string[];
  disliked_genres?: string[];
  preferred_moods?: string[];
  diversity_preference?: number;
  profile_public?: boolean;
}

// ============================================================================
// Auth Types
// ============================================================================

export interface RegisterRequest {
  email: string;
  username: string;
  password: string;
  full_name?: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

// ============================================================================
// List Types
// ============================================================================

export interface CreateListRequest {
  name: string;
  description?: string;
  is_public: boolean;
}

export interface UserList extends TimestampMixin {
  id: number;
  user_id: string;
  name: string;
  description?: string;
  is_public: boolean;
  likes_count: number;
}

export interface ListItem extends TimestampMixin {
  id: number;
  list_id: number;
  movie_id: number;
  position: number;
  notes?: string;
  added_by: string;
}

// ============================================================================
// Aesthetic Search Types
// ============================================================================

export interface AestheticSearchResult {
  movie_id: number;
  score: number;
  num_matching_frames: number;
  best_frames: Array<{
    frame_number: number;
    timestamp: number;
    score: number;
    frame_path: string;
  }>;
  visual_summary: Record<string, any>;
}

export interface AestheticSearchResponse {
  results: AestheticSearchResult[];
  query: string;
  processing_time_ms: number;
}

// ============================================================================
// Pagination Types
// ============================================================================

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

// ============================================================================
// Error Types
// ============================================================================

export interface APIError {
  detail: string;
  status_code: number;
  errors?: Array<{
    field: string;
    message: string;
  }>;
}
