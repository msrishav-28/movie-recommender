'use client';

import { useState, useRef, useEffect, type ReactNode } from 'react';
import { ChevronDown } from 'lucide-react';
import { cn } from '@/lib/utils';

export interface DropdownOption {
  value: string;
  label: string;
  icon?: ReactNode;
  disabled?: boolean;
}

export interface DropdownProps {
  options: DropdownOption[];
  value?: string;
  onChange: (value: string) => void;
  placeholder?: string;
  label?: string;
  disabled?: boolean;
  error?: string;
}

export function Dropdown({
  options,
  value,
  onChange,
  placeholder = 'Select an option',
  label,
  disabled,
  error,
}: DropdownProps) {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const selectedOption = options.find((opt) => opt.value === value);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div className="w-full space-y-2">
      {label && (
        <label className="block text-sm font-medium text-text-primary">{label}</label>
      )}

      <div ref={dropdownRef} className="relative">
        <button
          type="button"
          onClick={() => !disabled && setIsOpen(!isOpen)}
          disabled={disabled}
          className={cn(
            'w-full flex items-center justify-between rounded-md border border-white/10 bg-void-deep px-4 py-2.5 text-left transition-colors',
            'hover:bg-white/5 focus:border-electric-teal focus:outline-none focus:ring-2 focus:ring-electric-teal/20',
            'disabled:cursor-not-allowed disabled:opacity-50',
            error && 'border-signal-red'
          )}
        >
          <span className={cn('flex items-center gap-2', !selectedOption && 'text-white/40')}>
            {selectedOption?.icon}
            {selectedOption?.label || placeholder}
          </span>
          <ChevronDown className={cn('h-5 w-5 transition-transform', isOpen && 'rotate-180')} />
        </button>

        {isOpen && (
          <div className="absolute z-50 mt-2 w-full rounded-md glass-heavy border border-white/10 shadow-2xl animate-fade-in">
            <div className="max-h-60 overflow-y-auto p-2">
              {options.map((option) => (
                <button
                  key={option.value}
                  onClick={() => {
                    if (!option.disabled) {
                      onChange(option.value);
                      setIsOpen(false);
                    }
                  }}
                  disabled={option.disabled}
                  className={cn(
                    'w-full flex items-center gap-2 rounded-md px-3 py-2 text-left transition-colors',
                    'hover:bg-white/5',
                    option.value === value && 'bg-klein-blue/15 text-klein-blue',
                    option.disabled && 'opacity-50 cursor-not-allowed'
                  )}
                >
                  {option.icon}
                  {option.label}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      {error && (
        <p className="text-xs text-signal-red">{error}</p>
      )}
    </div>
  );
}
