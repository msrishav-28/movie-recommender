import { useQuery } from '@tanstack/react-query';
import { recommendationService } from '@/services/recommendation.service';
import { QUERY_KEYS, CACHE_DURATION } from '@/config/constants';

export function usePersonalizedRecommendations(limit: number = 24) {
  return useQuery({
    queryKey: [QUERY_KEYS.RECOMMENDATIONS, 'personalized', limit],
    queryFn: () => recommendationService.getRecommendations(limit),
    staleTime: CACHE_DURATION.MEDIUM * 1000,
  });
}

export function useSimilarMovies(movieId: number, limit: number = 12) {
  return useQuery({
    queryKey: [QUERY_KEYS.RECOMMENDATIONS, 'similar', movieId, limit],
    queryFn: () => recommendationService.getSimilarMovies(movieId, limit),
    staleTime: CACHE_DURATION.LONG * 1000,
    enabled: !!movieId,
  });
}

export function useAestheticRecommendations(query: string, limit: number = 12) {
  return useQuery({
    queryKey: [QUERY_KEYS.RECOMMENDATIONS, 'aesthetic', query, limit],
    queryFn: () => recommendationService.getAestheticRecommendations(query, limit),
    staleTime: CACHE_DURATION.LONG * 1000,
    enabled: !!query,
  });
}

export function useColdStartRecommendations(genres?: string[], moods?: string[]) {
  return useQuery({
    queryKey: [QUERY_KEYS.RECOMMENDATIONS, 'cold-start', genres, moods],
    queryFn: () => recommendationService.getColdStartRecommendations({ genres, moods }),
    staleTime: CACHE_DURATION.MEDIUM * 1000,
  });
}
