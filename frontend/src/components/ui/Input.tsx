import { forwardRef, type InputHTMLAttributes, type ReactNode, useState } from 'react';
import { cn } from '@/lib/utils';
import { AlertCircle, Eye, EyeOff, X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export interface InputProps extends Omit<InputHTMLAttributes<HTMLInputElement>, 'prefix' | 'size'> {
  label?: string;
  helperText?: string;
  error?: string;
  prefix?: ReactNode;
  suffix?: ReactNode;
  showPasswordToggle?: boolean;
  showClearButton?: boolean;
  onClear?: () => void;
  /** Command line style - large monospace font, cyberpunk feel */
  variant?: 'default' | 'command' | 'glass';
  /** Size of the input */
  size?: 'sm' | 'md' | 'lg';
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  (
    {
      className,
      type = 'text',
      label,
      helperText,
      error,
      prefix,
      suffix,
      showPasswordToggle = false,
      showClearButton = false,
      onClear,
      disabled,
      required,
      value,
      variant = 'default',
      size = 'md',
      ...props
    },
    ref
  ) => {
    const [showPassword, setShowPassword] = useState(false);
    const [isFocused, setIsFocused] = useState(false);
    const inputType = showPasswordToggle && showPassword ? 'text' : type;

    const sizeStyles = {
      sm: 'py-2 text-sm',
      md: 'py-3 text-base',
      lg: 'py-4 text-xl',
    };

    const variantStyles = {
      default: 'border-b border-white/20 focus:border-electric-teal bg-transparent',
      command: 'border-b-2 border-white/30 focus:border-klein-blue bg-transparent text-lg tracking-wide',
      glass: 'glass-light rounded-lg px-4 border border-white/10 focus:border-electric-teal/50',
    };

    return (
      <div className="w-full space-y-2">
        {label && (
          <motion.label
            className="block text-xs font-mono tracking-widest uppercase text-text-tech"
            initial={{ opacity: 0, y: -8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, ease: [0.22, 1, 0.36, 1] }}
          >
            {label}
            {required && <span className="ml-1 text-signal-red">*</span>}
          </motion.label>
        )}

        <div className="relative group">
          {prefix && (
            <div className="pointer-events-none absolute left-0 top-1/2 -translate-y-1/2 text-text-secondary">
              {prefix}
            </div>
          )}

          <input
            ref={ref}
            type={inputType}
            className={cn(
              'peer w-full bg-transparent px-0 text-text-primary transition-all duration-300',
              'placeholder:text-white/30 focus:outline-none',
              'caret-electric-teal font-mono',
              'disabled:cursor-not-allowed disabled:opacity-50',
              sizeStyles[size],
              variantStyles[variant],
              error && 'border-signal-red focus:border-signal-red',
              prefix && 'pl-8',
              (suffix || showPasswordToggle || showClearButton) && 'pr-10',
              className
            )}
            disabled={disabled}
            value={value}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
            {...props}
          />

          {/* Animated Glow Line - Appears on focus */}
          <motion.div
            className="absolute bottom-0 left-0 h-[2px] bg-gradient-to-r from-klein-blue via-electric-teal to-klein-blue"
            initial={{ scaleX: 0, opacity: 0 }}
            animate={{
              scaleX: isFocused ? 1 : 0,
              opacity: isFocused ? 1 : 0
            }}
            transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
            style={{
              originX: 0,
              boxShadow: isFocused ? '0 0 20px rgba(0, 217, 255, 0.5), 0 0 40px rgba(0, 47, 167, 0.3)' : 'none'
            }}
          />

          {/* Shimmer Effect on Focus */}
          <AnimatePresence>
            {isFocused && (
              <motion.div
                className="absolute inset-0 pointer-events-none overflow-hidden"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
              >
                <motion.div
                  className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent"
                  initial={{ x: '-100%' }}
                  animate={{ x: '100%' }}
                  transition={{ duration: 1.5, ease: 'linear', repeat: Infinity, repeatDelay: 2 }}
                />
              </motion.div>
            )}
          </AnimatePresence>

          {(suffix || showPasswordToggle || showClearButton) && (
            <div className="absolute right-0 top-1/2 flex -translate-y-1/2 items-center gap-2">
              {showClearButton && value && (
                <motion.button
                  type="button"
                  onClick={onClear}
                  className="text-text-secondary hover:text-white transition-colors p-1 rounded hover:bg-white/5"
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <X className="h-4 w-4" />
                </motion.button>
              )}

              {showPasswordToggle && type === 'password' && (
                <motion.button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="text-text-secondary hover:text-white transition-colors p-1 rounded hover:bg-white/5"
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.95 }}
                >
                  {showPassword ? (
                    <EyeOff className="h-4 w-4" />
                  ) : (
                    <Eye className="h-4 w-4" />
                  )}
                </motion.button>
              )}

              {suffix && <div className="text-text-secondary">{suffix}</div>}
            </div>
          )}
        </div>

        {/* Error/Helper Text with Animation */}
        <AnimatePresence>
          {(helperText || error) && (
            <motion.div
              className="flex items-start gap-1.5 text-xs font-mono"
              initial={{ opacity: 0, y: -4, height: 0 }}
              animate={{ opacity: 1, y: 0, height: 'auto' }}
              exit={{ opacity: 0, y: -4, height: 0 }}
              transition={{ duration: 0.2 }}
            >
              {error && <AlertCircle className="h-3 w-3 mt-0.5 text-signal-red shrink-0" />}
              <p className={cn(error ? 'text-signal-red' : 'text-text-tech')}>
                {error || helperText}
              </p>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    );
  }
);

Input.displayName = 'Input';

export { Input };
