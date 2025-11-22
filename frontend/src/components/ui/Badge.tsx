import { type HTMLAttributes } from 'react';
import { cn } from '@/lib/utils';

export interface BadgeProps extends HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'primary' | 'secondary' | 'success' | 'warning' | 'error' | 'outline';
  size?: 'sm' | 'md' | 'lg';
}

export function Badge({ className, variant = 'default', size = 'md', ...props }: BadgeProps) {
  const variants = {
    default: 'bg-glass-medium text-text-primary',
    primary: 'bg-brand-primary-light text-brand-primary border border-brand-primary',
    secondary: 'bg-brand-secondary-light text-brand-secondary border border-brand-secondary',
    success: 'bg-semantic-success-light text-semantic-success border border-semantic-success',
    warning: 'bg-semantic-warning-light text-semantic-warning border border-semantic-warning',
    error: 'bg-semantic-error-light text-semantic-error border border-semantic-error',
    outline: 'border border-border text-text-secondary',
  };

  const sizes = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-2.5 py-1 text-sm',
    lg: 'px-3 py-1.5 text-base',
  };

  return (
    <div
      className={cn(
        'inline-flex items-center rounded-full font-medium transition-colors',
        variants[variant],
        sizes[size],
        className
      )}
      {...props}
    />
  );
}
