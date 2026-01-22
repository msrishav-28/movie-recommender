'use client';

import Link from 'next/link';
import { Mail, ArrowLeft } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { useState } from 'react';
import { toast } from 'sonner';

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      // TODO: Implement forgot password API call
      await new Promise((resolve) => setTimeout(resolve, 1000));
      setSubmitted(true);
      toast.success('Password reset email sent');
    } catch (error) {
      toast.error('Failed to send reset email');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center relative">
      <div className="w-full max-w-md px-4 relative z-10">
        <Card variant="glass" className="backdrop-blur-xl">
          <CardHeader>
            <CardTitle>Forgot Password</CardTitle>
            <CardDescription>
              {submitted
                ? 'Check your email for reset instructions'
                : 'Enter your email to reset your password'}
            </CardDescription>
          </CardHeader>

          <CardContent>
            {!submitted ? (
              <form onSubmit={handleSubmit} className="space-y-4">
                <Input
                  type="email"
                  label="Email"
                  placeholder="your@email.com"
                  prefix={<Mail className="h-5 w-5" />}
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />

                <Button
                  type="submit"
                  variant="primary"
                  size="lg"
                  fullWidth
                  loading={isLoading}
                >
                  Send Reset Link
                </Button>

                <div className="text-center">
                  <Link href="/login" className="text-sm text-klein-blue hover:underline inline-flex items-center gap-1">
                    <ArrowLeft className="h-4 w-4" />
                    Back to Login
                  </Link>
                </div>
              </form>
            ) : (
              <div className="text-center space-y-4">
                <Mail className="h-16 w-16 mx-auto text-klein-blue" />
                <p className="text-text-secondary">
                  We&apos;ve sent a password reset link to <strong>{email}</strong>
                </p>
                <Link href="/login">
                  <Button variant="primary" size="lg" fullWidth>
                    Return to Login
                  </Button>
                </Link>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
