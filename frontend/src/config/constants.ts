/**
 * Application constants and configuration
 */

export const APP_NAME = 'CineAesthete';
export const APP_DESCRIPTION = "The world's first aesthetic-based movie discovery platform";

// API Configuration
export const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
export const API_BASE_PATH = process.env.NEXT_PUBLIC_API_BASE_PATH || '/api/v1';
export const API_TIMEOUT = 30000; // 30 seconds

// TMDb Configuration
export const TMDB_IMAGE_BASE_URL =
  process.env.NEXT_PUBLIC_TMDB_IMAGE_BASE_URL || 'https://image.tmdb.org/t/p';

// Pagination
export const DEFAULT_PAGE_SIZE = 24;
export const MOVIES_PER_ROW_DESKTOP = 6;
export const MOVIES_PER_ROW_TABLET = 4;
export const MOVIES_PER_ROW_MOBILE = 2;

// Cache Duration (in seconds)
export const CACHE_DURATION = {
  SHORT: 60, // 1 minute
  MEDIUM: 300, // 5 minutes
  LONG: 1800, // 30 minutes
  VERY_LONG: 86400, // 24 hours
};

// Query Keys for React Query
export const QUERY_KEYS = {
  USER: 'user',
  MOVIES: 'movies',
  MOVIE_DETAIL: 'movie-detail',
  RECOMMENDATIONS: 'recommendations',
  SIMILAR_MOVIES: 'similar-movies',
  AESTHETIC_SEARCH: 'aesthetic-search',
  WATCHLIST: 'watchlist',
  RATINGS: 'ratings',
  REVIEWS: 'reviews',
  TRENDING: 'trending',
  POPULAR: 'popular',
  GENRES: 'genres',
  STREAMING: 'streaming',
} as const;

// Local Storage Keys
export const STORAGE_KEYS = {
  ACCESS_TOKEN: 'cine_access_token',
  REFRESH_TOKEN: 'cine_refresh_token',
  USER: 'cine_user',
  THEME: 'cine_theme',
  SEARCH_HISTORY: 'cine_search_history',
  ONBOARDING_COMPLETED: 'cine_onboarding',
} as const;

// Genre List (matching TMDb)
export const GENRES = [
  { id: 28, name: 'Action' },
  { id: 12, name: 'Adventure' },
  { id: 16, name: 'Animation' },
  { id: 35, name: 'Comedy' },
  { id: 80, name: 'Crime' },
  { id: 99, name: 'Documentary' },
  { id: 18, name: 'Drama' },
  { id: 10751, name: 'Family' },
  { id: 14, name: 'Fantasy' },
  { id: 36, name: 'History' },
  { id: 27, name: 'Horror' },
  { id: 10402, name: 'Music' },
  { id: 9648, name: 'Mystery' },
  { id: 10749, name: 'Romance' },
  { id: 878, name: 'Science Fiction' },
  { id: 10770, name: 'TV Movie' },
  { id: 53, name: 'Thriller' },
  { id: 10752, name: 'War' },
  { id: 37, name: 'Western' },
] as const;

// Mood Tags for Aesthetic Search
export const MOOD_TAGS = [
  'Cozy',
  'Dark',
  'Dreamy',
  'Energetic',
  'Epic',
  'Gritty',
  'Melancholic',
  'Mysterious',
  'Nostalgic',
  'Peaceful',
  'Romantic',
  'Suspenseful',
  'Uplifting',
  'Whimsical',
] as const;

// Visual Tags
export const VISUAL_TAGS = [
  'Neon lights',
  'Golden hour',
  'Rain',
  'Snow',
  'Cityscape',
  'Nature',
  'Desert',
  'Ocean',
  'Forest',
  'Mountains',
  'Night sky',
  'Sunset',
  'Sunrise',
  'Fog',
  'Cyberpunk',
  'Vintage',
  'Minimalist',
  'Colorful',
  'Monochrome',
] as const;

// Decades
export const DECADES = [
  { value: '2020s', label: '2020s', min: 2020, max: 2029 },
  { value: '2010s', label: '2010s', min: 2010, max: 2019 },
  { value: '2000s', label: '2000s', min: 2000, max: 2009 },
  { value: '1990s', label: '1990s', min: 1990, max: 1999 },
  { value: '1980s', label: '1980s', min: 1980, max: 1989 },
  { value: '1970s', label: '1970s', min: 1970, max: 1979 },
  { value: '1960s', label: '1960s', min: 1960, max: 1969 },
  { value: '1950s', label: '1950s', min: 1950, max: 1959 },
] as const;

// Languages
export const LANGUAGES = [
  { code: 'en', name: 'English' },
  { code: 'es', name: 'Spanish' },
  { code: 'fr', name: 'French' },
  { code: 'de', name: 'German' },
  { code: 'it', name: 'Italian' },
  { code: 'ja', name: 'Japanese' },
  { code: 'ko', name: 'Korean' },
  { code: 'zh', name: 'Chinese' },
  { code: 'hi', name: 'Hindi' },
  { code: 'ru', name: 'Russian' },
] as const;

// Rating Scale
export const RATING_SCALE = {
  MIN: 0,
  MAX: 10,
  STEP: 0.5,
} as const;

// Feature Flags
export const FEATURES = {
  AESTHETIC_SEARCH:
    process.env.NEXT_PUBLIC_ENABLE_AESTHETIC_SEARCH === 'true',
  SOCIAL_FEATURES:
    process.env.NEXT_PUBLIC_ENABLE_SOCIAL_FEATURES === 'true',
  ANALYTICS: process.env.NEXT_PUBLIC_ENABLE_ANALYTICS === 'true',
} as const;

// Animation Durations (in ms)
export const ANIMATION_DURATION = {
  INSTANT: 100,
  FAST: 200,
  NORMAL: 300,
  SLOW: 500,
  SLOWER: 800,
  SLOWEST: 1200,
} as const;

// Breakpoints (must match Tailwind config)
export const BREAKPOINTS = {
  XS: 320,
  SM: 640,
  MD: 768,
  LG: 1024,
  XL: 1280,
  '2XL': 1536,
  '3XL': 1920,
} as const;

// Toast Configuration
export const TOAST_DURATION = {
  SUCCESS: 3000,
  ERROR: 6000,
  WARNING: 5000,
  INFO: 4000,
} as const;

// Validation Rules
export const VALIDATION = {
  USERNAME: {
    MIN_LENGTH: 3,
    MAX_LENGTH: 50,
    PATTERN: /^[a-zA-Z0-9_-]+$/,
  },
  PASSWORD: {
    MIN_LENGTH: 8,
    MAX_LENGTH: 100,
  },
  BIO: {
    MAX_LENGTH: 500,
  },
  REVIEW: {
    MIN_LENGTH: 10,
    MAX_LENGTH: 5000,
  },
  SEARCH_QUERY: {
    MIN_LENGTH: 1,
    MAX_LENGTH: 200,
  },
} as const;

// Social Media Links
export const SOCIAL_LINKS = {
  TWITTER: 'https://twitter.com/cineaesthete',
  INSTAGRAM: 'https://instagram.com/cineaesthete',
  GITHUB: 'https://github.com/cineaesthete',
} as const;

// External Links
export const EXTERNAL_LINKS = {
  TMDB: 'https://www.themoviedb.org',
  IMDB: 'https://www.imdb.com',
} as const;

// Error Messages
export const ERROR_MESSAGES = {
  GENERIC: 'Something went wrong. Please try again.',
  NETWORK: 'Network error. Please check your connection.',
  UNAUTHORIZED: 'You must be logged in to perform this action.',
  FORBIDDEN: 'You do not have permission to perform this action.',
  NOT_FOUND: 'The requested resource was not found.',
  VALIDATION: 'Please check your input and try again.',
  SERVER: 'Server error. Please try again later.',
} as const;

// Success Messages
export const SUCCESS_MESSAGES = {
  LOGIN: 'Welcome back!',
  LOGOUT: 'Logged out successfully',
  REGISTER: 'Account created successfully!',
  RATING_ADDED: 'Rating added successfully',
  RATING_UPDATED: 'Rating updated successfully',
  REVIEW_POSTED: 'Review posted successfully',
  WATCHLIST_ADDED: 'Added to watchlist',
  WATCHLIST_REMOVED: 'Removed from watchlist',
  PROFILE_UPDATED: 'Profile updated successfully',
} as const;
