'use client';

import { useState, useRef, useEffect } from 'react';
import { cn } from '@/lib/utils';

export interface SliderProps {
  min?: number;
  max?: number;
  step?: number;
  value?: number;
  defaultValue?: number;
  onChange?: (value: number) => void;
  label?: string;
  showValue?: boolean;
  disabled?: boolean;
}

export function Slider({
  min = 0,
  max = 100,
  step = 1,
  value,
  defaultValue = min,
  onChange,
  label,
  showValue = true,
  disabled = false,
}: SliderProps) {
  const [internalValue, setInternalValue] = useState(value ?? defaultValue);
  const sliderRef = useRef<HTMLDivElement>(null);
  const isDragging = useRef(false);

  const currentValue = value ?? internalValue;
  const percentage = ((currentValue - min) / (max - min)) * 100;

  const updateValue = (clientX: number) => {
    if (!sliderRef.current || disabled) return;

    const rect = sliderRef.current.getBoundingClientRect();
    const percent = Math.max(0, Math.min(1, (clientX - rect.left) / rect.width));
    const newValue = Math.round((min + percent * (max - min)) / step) * step;

    setInternalValue(newValue);
    onChange?.(newValue);
  };

  const handleMouseDown = (e: React.MouseEvent) => {
    if (disabled) return;
    isDragging.current = true;
    updateValue(e.clientX);
  };

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (isDragging.current) {
        updateValue(e.clientX);
      }
    };

    const handleMouseUp = () => {
      isDragging.current = false;
    };

    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [min, max, step, disabled]);

  return (
    <div className="w-full space-y-2">
      {(label || showValue) && (
        <div className="flex items-center justify-between">
          {label && <label className="text-sm font-medium">{label}</label>}
          {showValue && (
            <span className="text-sm font-medium text-klein-blue">{currentValue}</span>
          )}
        </div>
      )}

      <div
        ref={sliderRef}
        className={cn(
          'relative h-2 rounded-full bg-white/10 cursor-pointer',
          disabled && 'opacity-50 cursor-not-allowed'
        )}
        onMouseDown={handleMouseDown}
      >
        {/* Progress */}
        <div
          className="absolute h-full rounded-full bg-klein-blue transition-all shadow-[0_0_10px_rgba(0,47,167,0.5)]"
          style={{ width: `${percentage}%` }}
        />

        {/* Thumb */}
        <div
          className={cn(
            'absolute top-1/2 -translate-y-1/2 w-5 h-5 rounded-full bg-white border-2 border-klein-blue shadow-[0_0_15px_rgba(0,47,167,0.8)]',
            'transition-transform hover:scale-110',
            isDragging.current && 'scale-125 ring-2 ring-klein-blue/30'
          )}
          style={{ left: `calc(${percentage}% - 10px)` }}
        />
      </div>
    </div>
  );
}
