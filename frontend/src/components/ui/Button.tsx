import { forwardRef, type ButtonHTMLAttributes, type ReactNode } from 'react';
import { cn } from '@/lib/utils';
import { Loader2 } from 'lucide-react';
import { motion, HTMLMotionProps } from 'framer-motion';
import Magnetic from './Magnetic';
import { useAudioUI } from '@/hooks/use-audio-ui';

export interface ButtonProps extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, 'onAnimationStart' | 'onDragStart' | 'onDragEnd' | 'onDrag' | 'ref'> {
  variant?: 'primary' | 'secondary' | 'tertiary' | 'ghost' | 'glass' | 'outline' | 'text' | 'gradient' | 'danger';
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
  icon?: ReactNode;
  iconPosition?: 'left' | 'right';
  loading?: boolean;
  glow?: boolean;
  fullWidth?: boolean;
  magnetic?: boolean;
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
      magnetic = false,
      children,
      disabled,
      ...props
    },
    ref
  ) => {
    // Removed standard transition classes: transition-all duration-200 active:scale-98
    const baseStyles = 'inline-flex items-center justify-center gap-2 rounded-md font-medium focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-electric-teal focus-visible:ring-offset-2 focus-visible:ring-offset-void disabled:pointer-events-none disabled:opacity-50';

    const variants = {
      primary: 'bg-klein-blue text-white shadow-md hover:bg-klein-blue/90',
      secondary: 'bg-electric-teal text-void shadow-md hover:bg-electric-teal/90',
      tertiary: 'bg-cinema-gold text-void shadow-md hover:bg-cinema-gold/90',
      ghost: 'bg-transparent hover:bg-white/5',
      glass: 'glass-heavy',
      outline: 'border border-white/10 bg-transparent hover:bg-white/5',
      text: 'bg-transparent hover:bg-white/5 underline-offset-4 hover:underline',
      gradient: 'bg-gradient-to-r from-klein-blue to-electric-teal text-white shadow-md',
      danger: 'bg-signal-red text-white shadow-md hover:bg-signal-red/90',
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
      secondary: 'glow-teal',
      tertiary: 'glow-gold',
      ghost: '',
      glass: '',
      outline: '',
      text: '',
      gradient: 'glow-primary',
      danger: 'glow-red',
    };

    const { playSound } = useAudioUI();

    const buttonContent = (
      <motion.button
        ref={ref as any}
        className={cn(
          baseStyles,
          variants[variant],
          sizes[size],
          glow && glowStyles[variant],
          fullWidth && 'w-full',
          className
        )}
        disabled={disabled || loading}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onMouseEnter={() => playSound('hover')}
        onMouseDown={() => playSound('click')}
        transition={{ type: 'spring', stiffness: 400, damping: 10 }}
        {...(props as HTMLMotionProps<"button">)}
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
      </motion.button>
    );

    if (magnetic) {
      return <Magnetic>{buttonContent}</Magnetic>;
    }

    return buttonContent;
  }
);

Button.displayName = 'Button';

export { Button };
