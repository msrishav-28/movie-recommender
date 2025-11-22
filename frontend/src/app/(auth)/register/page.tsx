'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Film, Mail, Lock, User } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card';
import { useAuth } from '@/hooks/useAuth';

const registerSchema = z.object({
  username: z.string().min(3, 'Username must be at least 3 characters'),
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ['confirmPassword'],
});

type RegisterFormData = z.infer<typeof registerSchema>;

export default function RegisterPage() {
  const { register: registerUser, isLoading } = useAuth();
  const [error, setError] = useState<string>('');

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
  });

  const onSubmit = async (data: RegisterFormData) => {
    try {
      setError('');
      await registerUser({
        username: data.username,
        email: data.email,
        password: data.password,
      });
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Registration failed. Please try again.');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-mesh py-12">
      <div className="w-full max-w-md px-4">
        {/* Logo */}
        <Link href="/" className="flex items-center justify-center gap-2 mb-8">
          <Film className="h-10 w-10 text-brand-primary" />
          <span className="font-cinematic text-3xl tracking-wider">CINEAESTHETE</span>
        </Link>

        <Card variant="glass" className="backdrop-blur-xl">
          <CardHeader>
            <CardTitle>Create Account</CardTitle>
            <CardDescription>Join thousands of movie enthusiasts</CardDescription>
          </CardHeader>

          <CardContent>
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              {/* Username */}
              <Input
                type="text"
                label="Username"
                placeholder="johndoe"
                prefix={<User className="h-5 w-5" />}
                error={errors.username?.message}
                {...register('username')}
              />

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
                helperText="At least 8 characters"
                {...register('password')}
              />

              {/* Confirm Password */}
              <Input
                type="password"
                label="Confirm Password"
                placeholder="••••••••"
                prefix={<Lock className="h-5 w-5" />}
                showPasswordToggle
                error={errors.confirmPassword?.message}
                {...register('confirmPassword')}
              />

              {/* Error Message */}
              {error && (
                <div className="p-3 rounded-md bg-semantic-error/10 border border-semantic-error">
                  <p className="text-sm text-semantic-error">{error}</p>
                </div>
              )}

              {/* Terms */}
              <p className="text-xs text-text-tertiary">
                By signing up, you agree to our{' '}
                <Link href="/terms" className="text-brand-primary hover:underline">
                  Terms of Service
                </Link>{' '}
                and{' '}
                <Link href="/privacy" className="text-brand-primary hover:underline">
                  Privacy Policy
                </Link>
              </p>

              {/* Submit Button */}
              <Button
                type="submit"
                variant="primary"
                size="lg"
                fullWidth
                loading={isLoading}
                glow
              >
                Create Account
              </Button>

              {/* Divider */}
              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-border" />
                </div>
                <div className="relative flex justify-center text-sm">
                  <span className="px-2 bg-surface text-text-tertiary">or</span>
                </div>
              </div>

              {/* Login Link */}
              <div className="text-center">
                <p className="text-sm text-text-secondary">
                  Already have an account?{' '}
                  <Link href="/login" className="text-brand-primary hover:underline font-medium">
                    Sign in
                  </Link>
                </p>
              </div>
            </form>
          </CardContent>
        </Card>

        {/* Back to Home */}
        <div className="mt-6 text-center">
          <Link href="/" className="text-sm text-text-tertiary hover:text-text-primary transition-colors">
            ← Back to home
          </Link>
        </div>
      </div>
    </div>
  );
}
