import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { watchlistService } from '@/services/watchlist.service';
import { 
  WatchlistItemCreate, 
  WatchlistItemUpdate,
  WatchlistResponse 
} from '@/types/api.types';
import { toast } from 'sonner';

/**
 * Hook to get watchlist
 */
export function useWatchlist(
  watched?: boolean,
  sortBy: 'priority' | 'added_at' = 'priority',
  page: number = 1,
  pageSize: number = 20
) {
  return useQuery<WatchlistResponse>({
    queryKey: ['watchlist', watched, sortBy, page, pageSize],
    queryFn: () => watchlistService.getWatchlist(watched, sortBy, page, pageSize),
  });
}

/**
 * Hook to add to watchlist
 */
export function useAddToWatchlist() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: WatchlistItemCreate) => watchlistService.addToWatchlist(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['watchlist'] });
      toast.success('Added to watchlist!');
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to add to watchlist');
    },
  });
}

/**
 * Hook to remove from watchlist
 */
export function useRemoveFromWatchlist() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (itemId: number) => watchlistService.removeFromWatchlist(itemId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['watchlist'] });
      toast.success('Removed from watchlist');
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to remove from watchlist');
    },
  });
}

/**
 * Hook to update watchlist item
 */
export function useUpdateWatchlistItem() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ itemId, data }: { itemId: number; data: WatchlistItemUpdate }) => 
      watchlistService.updateWatchlistItem(itemId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['watchlist'] });
      toast.success('Watchlist updated');
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to update watchlist');
    },
  });
}
