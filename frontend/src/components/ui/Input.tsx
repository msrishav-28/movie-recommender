import { forwardRef, type InputHTMLAttributes, type ReactNode } from 'react';
import { cn } from '@/lib/utils';
import { AlertCircle, Eye, EyeOff, X } from 'lucide-react';

export interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  helperText?: string;
  error?: string;
  prefix?: ReactNode;
  suffix?: ReactNode;
  showPasswordToggle?: boolean;
  showClearButton?: boolean;
  onClear?: () => void;
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
      ...props
    },
    ref
  ) => {
    const [showPassword, setShowPassword] = React.useState(false);
    const inputType = showPasswordToggle && showPassword ? 'text' : type;

    return (
      <div className="w-full space-y-2">
        {label && (
          <label className="block text-sm font-medium text-text-primary">
            {label}
            {required && <span className="ml-1 text-semantic-error">*</span>}
          </label>
        )}

        <div className="relative">
          {prefix && (
            <div className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-text-secondary">
              {prefix}
            </div>
          )}

          <input
            ref={ref}
            type={inputType}
            className={cn(
              'w-full rounded-md border border-border bg-surface px-4 py-2.5 text-text-primary transition-colors duration-200',
              'placeholder:text-text-tertiary',
              'focus:border-brand-secondary focus:outline-none focus:ring-2 focus:ring-brand-secondary/20',
              'disabled:cursor-not-allowed disabled:opacity-50',
              error && 'border-semantic-error focus:border-semantic-error focus:ring-semantic-error/20',
              prefix && 'pl-10',
              (suffix || showPasswordToggle || showClearButton) && 'pr-10',
              className
            )}
            disabled={disabled}
            value={value}
            {...props}
          />

          {(suffix || showPasswordToggle || showClearButton) && (
            <div className="absolute right-3 top-1/2 flex -translate-y-1/2 items-center gap-2">
              {showClearButton && value && (
                <button
                  type="button"
                  onClick={onClear}
                  className="text-text-secondary hover:text-text-primary transition-colors"
                >
                  <X className="h-4 w-4" />
                </button>
              )}

              {showPasswordToggle && type === 'password' && (
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="text-text-secondary hover:text-text-primary transition-colors"
                >
                  {showPassword ? (
                    <EyeOff className="h-4 w-4" />
                  ) : (
                    <Eye className="h-4 w-4" />
                  )}
                </button>
              )}

              {suffix && <div className="text-text-secondary">{suffix}</div>}
            </div>
          )}
        </div>

        {(helperText || error) && (
          <div className="flex items-start gap-1 text-xs">
            {error && <AlertCircle className="h-3 w-3 mt-0.5 text-semantic-error shrink-0" />}
            <p className={cn(error ? 'text-semantic-error' : 'text-text-tertiary')}>
              {error || helperText}
            </p>
          </div>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';

export { Input };

// Fix React hook error
import React from 'react';
