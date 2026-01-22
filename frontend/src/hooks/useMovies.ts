import { useQuery, useInfiniteQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { movieService } from '@/services/movie.service';
import type { SearchFilters } from '@/types';
import { QUERY_KEYS, CACHE_DURATION } from '@/config/constants';

export function useMovies(filters: SearchFilters = {}, page: number = 1, pageSize: number = 24) {
  return useQuery({
    queryKey: [QUERY_KEYS.MOVIES, filters, page, pageSize],
    queryFn: () => movieService.searchMovies(filters, page, pageSize),
    staleTime: CACHE_DURATION.MEDIUM * 1000,
  });
}

export function useInfiniteMovies(filters: SearchFilters = {}, pageSize: number = 24) {
  return useInfiniteQuery({
    queryKey: [QUERY_KEYS.MOVIES, 'infinite', filters],
    queryFn: ({ pageParam = 1 }) => movieService.searchMovies(filters, pageParam, pageSize),
    getNextPageParam: (lastPage) => {
      if (lastPage.page < lastPage.total_pages) {
        return lastPage.page + 1;
      }
      return undefined;
    },
    initialPageParam: 1,
    staleTime: CACHE_DURATION.MEDIUM * 1000,
  });
}

export function useMovie(id: number) {
  return useQuery({
    queryKey: [QUERY_KEYS.MOVIE_DETAIL, id],
    queryFn: () => movieService.getMovieById(id),
    staleTime: CACHE_DURATION.LONG * 1000,
    enabled: !!id,
  });
}

export function useTrendingMovies(page: number = 1, pageSize: number = 24) {
  return useQuery({
    queryKey: [QUERY_KEYS.TRENDING, page],
    queryFn: () => movieService.getTrending(page, pageSize),
    staleTime: CACHE_DURATION.SHORT * 1000,
  });
}

export function useInfiniteTrendingMovies(pageSize: number = 24) {
  return useInfiniteQuery({
    queryKey: [QUERY_KEYS.TRENDING, 'infinite'],
    queryFn: ({ pageParam = 1 }) => movieService.getTrending(pageParam, pageSize),
    getNextPageParam: (lastPage) => {
      if (lastPage.page < lastPage.total_pages) {
        return lastPage.page + 1;
      }
      return undefined;
    },
    initialPageParam: 1,
    staleTime: CACHE_DURATION.SHORT * 1000,
  });
}

export function usePopularMovies(page: number = 1, pageSize: number = 24) {
  return useQuery({
    queryKey: [QUERY_KEYS.POPULAR, page],
    queryFn: () => movieService.getPopular(page, pageSize),
    staleTime: CACHE_DURATION.MEDIUM * 1000,
  });
}

export function useTopRatedMovies(page: number = 1, pageSize: number = 24) {
  return useQuery({
    queryKey: ['top-rated', page],
    queryFn: () => movieService.getTopRated(page, pageSize),
    staleTime: CACHE_DURATION.LONG * 1000,
  });
}

export function useInfiniteTopRatedMovies(pageSize: number = 24) {
  return useInfiniteQuery({
    queryKey: ['top-rated', 'infinite'],
    queryFn: ({ pageParam = 1 }) => movieService.getTopRated(pageParam, pageSize),
    getNextPageParam: (lastPage) => {
      if (lastPage.page < lastPage.total_pages) {
        return lastPage.page + 1;
      }
      return undefined;
    },
    initialPageParam: 1,
    staleTime: CACHE_DURATION.LONG * 1000,
  });
}

export function useMoviesByGenre(genreId: number, page: number = 1, pageSize: number = 24) {
  return useQuery({
    queryKey: ['movies-by-genre', genreId, page],
    queryFn: () => movieService.getByGenre(genreId, page, pageSize),
    staleTime: CACHE_DURATION.MEDIUM * 1000,
    enabled: !!genreId,
  });
}
