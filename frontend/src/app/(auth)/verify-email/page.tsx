'use client';

import { useEffect, useState } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import { CheckCircle, XCircle, Loader } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { apiClient } from '@/services/api.client';

export default function VerifyEmailPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');
  const [message, setMessage] = useState('');

  useEffect(() => {
    const token = searchParams.get('token');
    
    if (!token) {
      setStatus('error');
      setMessage('Invalid verification link');
      return;
    }

    verifyEmail(token);
  }, [searchParams]);

  const verifyEmail = async (token: string) => {
    try {
      await apiClient.post('/auth/verify-email', null, { params: { token } });
      setStatus('success');
      setMessage('Your email has been verified successfully!');
    } catch (error: any) {
      setStatus('error');
      setMessage(error.response?.data?.detail || 'Verification failed');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <Card variant="glass" className="max-w-md w-full">
        <CardContent className="p-8 text-center">
          {status === 'loading' && (
            <>
              <Loader className="h-16 w-16 animate-spin text-brand-primary mx-auto mb-4" />
              <h1 className="text-2xl font-bold mb-2">Verifying Email...</h1>
              <p className="text-text-secondary">Please wait while we verify your email address</p>
            </>
          )}

          {status === 'success' && (
            <>
              <CheckCircle className="h-16 w-16 text-semantic-success mx-auto mb-4" />
              <h1 className="text-2xl font-bold mb-2">Email Verified!</h1>
              <p className="text-text-secondary mb-6">{message}</p>
              <Button variant="primary" onClick={() => router.push('/login')} glow>
                Continue to Login
              </Button>
            </>
          )}

          {status === 'error' && (
            <>
              <XCircle className="h-16 w-16 text-semantic-error mx-auto mb-4" />
              <h1 className="text-2xl font-bold mb-2">Verification Failed</h1>
              <p className="text-text-secondary mb-6">{message}</p>
              <Button variant="outline" onClick={() => router.push('/login')}>
                Back to Login
              </Button>
            </>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
