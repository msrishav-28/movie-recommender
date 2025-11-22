import { useAuthStore } from '@/store/authStore';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';
import type { LoginCredentials, RegisterData } from '@/types';
import { toast } from 'sonner';
import { SUCCESS_MESSAGES, ERROR_MESSAGES } from '@/config/constants';

export function useAuth() {
  const router = useRouter();
  const {
    user,
    isAuthenticated,
    isLoading,
    error,
    login: loginStore,
    register: registerStore,
    logout: logoutStore,
    refreshUser,
    clearError,
  } = useAuthStore();

  // Refresh user on mount if authenticated
  useEffect(() => {
    if (isAuthenticated && !user) {
      refreshUser();
    }
  }, [isAuthenticated, user, refreshUser]);

  const login = async (credentials: LoginCredentials) => {
    try {
      await loginStore(credentials);
      toast.success(SUCCESS_MESSAGES.LOGIN);
      router.push('/dashboard');
    } catch (error: any) {
      toast.error(error.response?.data?.detail || ERROR_MESSAGES.GENERIC);
      throw error;
    }
  };

  const register = async (data: RegisterData) => {
    try {
      await registerStore(data);
      toast.success(SUCCESS_MESSAGES.REGISTER);
      router.push('/dashboard');
    } catch (error: any) {
      toast.error(error.response?.data?.detail || ERROR_MESSAGES.GENERIC);
      throw error;
    }
  };

  const logout = async () => {
    try {
      await logoutStore();
      toast.success(SUCCESS_MESSAGES.LOGOUT);
      router.push('/');
    } catch (error) {
      toast.error(ERROR_MESSAGES.GENERIC);
    }
  };

  const requireAuth = (redirectTo: string = '/login') => {
    if (!isAuthenticated) {
      router.push(redirectTo);
      return false;
    }
    return true;
  };

  return {
    user,
    isAuthenticated,
    isLoading,
    error,
    login,
    register,
    logout,
    refreshUser,
    clearError,
    requireAuth,
  };
}
