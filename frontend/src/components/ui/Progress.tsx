import { cn } from '@/lib/utils';

export interface ProgressProps {
  value: number;
  max?: number;
  size?: 'sm' | 'md' | 'lg';
  variant?: 'default' | 'success' | 'warning' | 'error';
  showValue?: boolean;
  label?: string;
}

export function Progress({
  value,
  max = 100,
  size = 'md',
  variant = 'default',
  showValue = false,
  label,
}: ProgressProps) {
  const percentage = Math.min(100, Math.max(0, (value / max) * 100));

  const sizes = {
    sm: 'h-1',
    md: 'h-2',
    lg: 'h-3',
  };

  const variants = {
    default: 'bg-klein-blue',
    success: 'bg-emerald-500',
    warning: 'bg-amber-500',
    error: 'bg-signal-red',
  };

  return (
    <div className="w-full space-y-2">
      {(label || showValue) && (
        <div className="flex items-center justify-between">
          {label && <span className="text-sm font-medium">{label}</span>}
          {showValue && (
            <span className="text-sm font-medium">{Math.round(percentage)}%</span>
          )}
        </div>
      )}

      <div className={cn('w-full rounded-full bg-white/10 overflow-hidden', sizes[size])}>
        <div
          className={cn('h-full transition-all duration-300', variants[variant])}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}
