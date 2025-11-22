import { forwardRef, type ButtonHTMLAttributes, type ReactNode } from 'react';
import { cn } from '@/lib/utils';
import { Loader2 } from 'lucide-react';

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'tertiary' | 'ghost' | 'glass' | 'outline' | 'text' | 'gradient' | 'danger';
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
  icon?: ReactNode;
  iconPosition?: 'left' | 'right';
  loading?: boolean;
  glow?: boolean;
  fullWidth?: boolean;
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      className,
      variant = 'primary',
      size = 'md',
      icon,
      iconPosition = 'left',
      loading = false,
      glow = false,
      fullWidth = false,
      children,
      disabled,
      ...props
    },
    ref
  ) => {
    const baseStyles = 'inline-flex items-center justify-center gap-2 rounded-md font-medium transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-secondary focus-visible:ring-offset-2 focus-visible:ring-offset-background disabled:pointer-events-none disabled:opacity-50 active:scale-98';

    const variants = {
      primary: 'bg-brand-primary text-white hover:bg-brand-primary-hover active:bg-brand-primary-active shadow-md hover:shadow-lg',
      secondary: 'bg-brand-secondary text-background hover:bg-brand-secondary-hover active:bg-brand-secondary-active shadow-md hover:shadow-lg',
      tertiary: 'bg-brand-tertiary text-background hover:bg-brand-tertiary-hover active:bg-brand-tertiary-active shadow-md hover:shadow-lg',
      ghost: 'bg-transparent hover:bg-glass-light active:bg-glass-medium',
      glass: 'glass-heavy hover:glass-heavy-hover backdrop-blur-lg',
      outline: 'border border-border bg-transparent hover:bg-glass-light active:bg-glass-medium',
      text: 'bg-transparent hover:bg-glass-light active:bg-glass-medium underline-offset-4 hover:underline',
      gradient: 'bg-gradient-to-r from-brand-primary to-brand-secondary text-white shadow-md hover:shadow-lg hover:scale-102',
      danger: 'bg-semantic-error text-white hover:brightness-110 active:brightness-90 shadow-md hover:shadow-lg',
    };

    const sizes = {
      xs: 'h-7 px-3 text-xs',
      sm: 'h-8 px-4 text-sm',
      md: 'h-10 px-6 text-base',
      lg: 'h-12 px-8 text-lg',
      xl: 'h-14 px-10 text-xl',
    };

    const glowStyles = {
      primary: 'glow-primary',
      secondary: 'glow-secondary',
      tertiary: '',
      ghost: '',
      glass: '',
      outline: '',
      text: '',
      gradient: 'glow-primary',
      danger: '',
    };

    return (
      <button
        ref={ref}
        className={cn(
          baseStyles,
          variants[variant],
          sizes[size],
          glow && glowStyles[variant],
          fullWidth && 'w-full',
          className
        )}
        disabled={disabled || loading}
        {...props}
      >
        {loading ? (
          <Loader2 className="h-4 w-4 animate-spin" />
        ) : (
          <>
            {icon && iconPosition === 'left' && <span className="shrink-0">{icon}</span>}
            {children}
            {icon && iconPosition === 'right' && <span className="shrink-0">{icon}</span>}
          </>
        )}
      </button>
    );
  }
);

Button.displayName = 'Button';

export { Button };
