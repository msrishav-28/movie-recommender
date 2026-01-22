import { type HTMLAttributes } from 'react';
import { cn } from '@/lib/utils';

export interface BadgeProps extends HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'primary' | 'secondary' | 'success' | 'warning' | 'error' | 'outline';
  size?: 'sm' | 'md' | 'lg';
}

export function Badge({ className, variant = 'default', size = 'md', ...props }: BadgeProps) {
  const variants = {
    default: 'bg-white/5 text-text-primary',
    primary: 'bg-klein-blue/15 text-klein-blue border border-klein-blue/50',
    secondary: 'bg-electric-teal/15 text-electric-teal border border-electric-teal/50',
    success: 'bg-emerald-500/15 text-emerald-400 border border-emerald-500/50',
    warning: 'bg-amber-500/15 text-amber-400 border border-amber-500/50',
    error: 'bg-signal-red/15 text-signal-red border border-signal-red/50',
    outline: 'border border-white/10 text-text-secondary',
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
