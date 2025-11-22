'use client';

import { Check } from 'lucide-react';
import { cn } from '@/lib/utils';

export interface CheckboxProps {
  checked?: boolean;
  onChange?: (checked: boolean) => void;
  label?: string;
  disabled?: boolean;
  error?: string;
}

export function Checkbox({ checked = false, onChange, label, disabled, error }: CheckboxProps) {
  return (
    <div className="space-y-1">
      <label className={cn('flex items-center gap-2 cursor-pointer', disabled && 'opacity-50 cursor-not-allowed')}>
        <button
          type="button"
          role="checkbox"
          aria-checked={checked}
          onClick={() => !disabled && onChange?.(!checked)}
          disabled={disabled}
          className={cn(
            'flex items-center justify-center w-5 h-5 rounded border-2 transition-all',
            checked
              ? 'bg-brand-primary border-brand-primary'
              : 'border-border bg-surface hover:border-brand-primary',
            error && 'border-semantic-error',
            disabled && 'cursor-not-allowed'
          )}
        >
          {checked && <Check className="h-3 w-3 text-white" />}
        </button>
        {label && <span className="text-sm select-none">{label}</span>}
      </label>
      {error && <p className="text-xs text-semantic-error ml-7">{error}</p>}
    </div>
  );
}
