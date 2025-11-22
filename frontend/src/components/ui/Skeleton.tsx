import { type HTMLAttributes } from 'react';
import { cn } from '@/lib/utils';

export interface SkeletonProps extends HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'shimmer';
}

export function Skeleton({ className, variant = 'shimmer', ...props }: SkeletonProps) {
  return (
    <div
      className={cn(
        'rounded-md bg-glass-light',
        variant === 'shimmer' ? 'skeleton-shimmer' : 'animate-pulse',
        className
      )}
      {...props}
    />
  );
}
