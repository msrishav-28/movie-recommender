/**
 * Custom Lists Hook
 * React Query hooks for managing custom movie lists
 */

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { listService, UserList, CreateListRequest, AddToListRequest } from '@/services/list.service';
import { toast } from 'sonner';

/**
 * Hook to get user's lists
 */
export function useMyLists() {
  return useQuery({
    queryKey: ['lists', 'my'],
    queryFn: () => listService.getMyLists(),
  });
}

/**
 * Hook to create a new list
 */
export function useCreateList() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateListRequest) => listService.createList(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['lists', 'my'] });
      toast.success('List created successfully!');
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to create list');
    },
  });
}

/**
 * Hook to add movie to a list
 */
export function useAddToList() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ listId, data }: { listId: number; data: AddToListRequest }) =>
      listService.addToList(listId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['lists'] });
      toast.success('Added to list!');
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to add to list');
    },
  });
}

/**
 * Hook to delete a list
 */
export function useDeleteList() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (listId: number) => listService.deleteList(listId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['lists', 'my'] });
      toast.success('List deleted');
    },
    onError: (error: any) => {
      toast.error('Failed to delete list');
    },
  });
}
