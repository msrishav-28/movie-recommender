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
            'flex items-center justify-center w-5 h-5 rounded border-2 transition-all duration-300',
            checked
              ? 'bg-klein-blue border-klein-blue shadow-[0_0_10px_rgba(0,47,167,0.5)]'
              : 'border-white/20 bg-white/5 hover:border-klein-blue',
            error && 'border-signal-red',
            disabled && 'cursor-not-allowed opacity-50'
          )}
        >
          <Check className={cn("h-3 w-3 text-white transition-all duration-300", checked ? "scale-100 opacity-100" : "scale-0 opacity-0")} />
        </button>
        {label && <span className="text-sm select-none">{label}</span>}
      </label>
      {error && <p className="text-xs text-signal-red ml-7">{error}</p>}
    </div>
  );
}
