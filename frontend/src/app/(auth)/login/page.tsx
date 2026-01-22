'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Film, Mail, Lock } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card';
import { useAuth } from '@/hooks/useAuth';

const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

type LoginFormData = z.infer<typeof loginSchema>;

export default function LoginPage() {
  const { login, isLoading } = useAuth();
  const [error, setError] = useState<string>('');

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (data: LoginFormData) => {
    try {
      setError('');
      await login(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed. Please try again.');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center relative">
      <div className="w-full max-w-md px-4 relative z-10">
        {/* Logo */}
        <Link href="/" className="flex items-center justify-center gap-2 mb-8">
          <Film className="h-10 w-10 text-klein-blue" />
          <span className="font-cinematic text-3xl tracking-wider">CINEAESTHETE</span>
        </Link>

        <Card variant="glass" className="backdrop-blur-xl">
          <CardHeader>
            <CardTitle>Welcome Back</CardTitle>
            <CardDescription>Sign in to your account to continue</CardDescription>
          </CardHeader>

          <CardContent>
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              {/* Email */}
              <Input
                type="email"
                label="Email"
                placeholder="your@email.com"
                prefix={<Mail className="h-5 w-5" />}
                error={errors.email?.message}
                {...register('email')}
              />

              {/* Password */}
              <Input
                type="password"
                label="Password"
                placeholder="••••••••"
                prefix={<Lock className="h-5 w-5" />}
                showPasswordToggle
                error={errors.password?.message}
                {...register('password')}
              />

              {/* Error Message */}
              {error && (
                <div className="p-3 rounded-md bg-signal-red/10 border border-signal-red">
                  <p className="text-sm text-signal-red">{error}</p>
                </div>
              )}

              {/* Forgot Password */}
              <div className="flex justify-end">
                <Link
                  href="/forgot-password"
                  className="text-sm text-klein-blue hover:underline"
                >
                  Forgot password?
                </Link>
              </div>

              {/* Submit Button */}
              <Button
                type="submit"
                variant="primary"
                size="lg"
                fullWidth
                loading={isLoading}
                glow
              >
                Sign In
              </Button>

              {/* Divider */}
              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-white/10" />
                </div>
                <div className="relative flex justify-center text-sm">
                  <span className="px-2 bg-void-deep text-white/40">or</span>
                </div>
              </div>

              {/* Register Link */}
              <div className="text-center">
                <p className="text-sm text-text-secondary">
                  Don&apos;t have an account?{' '}
                  <Link href="/register" className="text-klein-blue hover:underline font-medium">
                    Sign up
                  </Link>
                </p>
              </div>
            </form>
          </CardContent>
        </Card>

        {/* Back to Home */}
        <div className="mt-6 text-center">
          <Link href="/" className="text-sm text-white/40 hover:text-text-primary transition-colors">
            ← Back to home
          </Link>
        </div>
      </div>
    </div>
  );
}
