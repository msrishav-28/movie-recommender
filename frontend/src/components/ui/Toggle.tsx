'use client';

import { cn } from '@/lib/utils';

export interface ToggleProps {
  checked?: boolean;
  onChange?: (checked: boolean) => void;
  label?: string;
  disabled?: boolean;
  size?: 'sm' | 'md' | 'lg';
}

export function Toggle({ checked = false, onChange, label, disabled, size = 'md' }: ToggleProps) {
  const sizes = {
    sm: {
      track: 'w-8 h-4',
      thumb: 'w-3 h-3',
      translate: 'translate-x-4',
    },
    md: {
      track: 'w-11 h-6',
      thumb: 'w-5 h-5',
      translate: 'translate-x-5',
    },
    lg: {
      track: 'w-14 h-7',
      thumb: 'w-6 h-6',
      translate: 'translate-x-7',
    },
  };

  const sizeConfig = sizes[size];

  return (
    <label className={cn('flex items-center gap-3 cursor-pointer', disabled && 'opacity-50 cursor-not-allowed')}>
      <button
        type="button"
        role="switch"
        aria-checked={checked}
        onClick={() => !disabled && onChange?.(!checked)}
        disabled={disabled}
        className={cn(
          'relative rounded-full transition-all duration-300',
          sizeConfig.track,
          checked ? 'bg-electric-teal shadow-[0_0_15px_rgba(0,217,255,0.4)]' : 'bg-white/10 border border-white/10',
          disabled && 'cursor-not-allowed opacity-50'
        )}
      >
        <span
          className={cn(
            'absolute left-0.5 top-1/2 -translate-y-1/2 rounded-full bg-white shadow-md transition-transform duration-300',
            sizeConfig.thumb,
            checked && sizeConfig.translate
          )}
        />
      </button>
      {label && <span className="text-sm select-none">{label}</span>}
    </label>
  );
}
