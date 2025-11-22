'use client';

import { useState } from 'react';
import { Star } from 'lucide-react';
import { cn } from '@/lib/utils';

export interface RatingStarsProps {
  value?: number;
  onChange?: (value: number) => void;
  max?: number;
  size?: 'sm' | 'md' | 'lg';
  readonly?: boolean;
  showValue?: boolean;
}

export function RatingStars({
  value = 0,
  onChange,
  max = 10,
  size = 'md',
  readonly = false,
  showValue = false,
}: RatingStarsProps) {
  const [hoverValue, setHoverValue] = useState<number | null>(null);

  const sizes = {
    sm: 'h-4 w-4',
    md: 'h-5 w-5',
    lg: 'h-6 w-6',
  };

  const displayValue = hoverValue ?? value;
  const starCount = 5;
  const valuePerStar = max / starCount;

  const handleClick = (starIndex: number) => {
    if (!readonly && onChange) {
      const newValue = (starIndex + 1) * valuePerStar;
      onChange(newValue);
    }
  };

  return (
    <div className="flex items-center gap-2">
      <div className="flex items-center gap-1">
        {Array.from({ length: starCount }).map((_, index) => {
          const starValue = (index + 1) * valuePerStar;
          const isFilled = displayValue >= starValue;
          const isPartial = displayValue >= starValue - valuePerStar && displayValue < starValue;
          const partialPercent = isPartial
            ? ((displayValue - (starValue - valuePerStar)) / valuePerStar) * 100
            : 0;

          return (
            <button
              key={index}
              type="button"
              onClick={() => handleClick(index)}
              onMouseEnter={() => !readonly && setHoverValue((index + 1) * valuePerStar)}
              onMouseLeave={() => !readonly && setHoverValue(null)}
              disabled={readonly}
              className={cn(
                'relative transition-transform',
                !readonly && 'hover:scale-110 cursor-pointer',
                readonly && 'cursor-default'
              )}
            >
              {isPartial ? (
                <div className="relative">
                  <Star className={cn(sizes[size], 'text-text-tertiary')} />
                  <div
                    className="absolute inset-0 overflow-hidden"
                    style={{ width: `${partialPercent}%` }}
                  >
                    <Star className={cn(sizes[size], 'fill-brand-tertiary text-brand-tertiary')} />
                  </div>
                </div>
              ) : (
                <Star
                  className={cn(
                    sizes[size],
                    isFilled
                      ? 'fill-brand-tertiary text-brand-tertiary'
                      : 'text-text-tertiary'
                  )}
                />
              )}
            </button>
          );
        })}
      </div>

      {showValue && (
        <span className="text-sm font-medium">
          {value.toFixed(1)} / {max}
        </span>
      )}
    </div>
  );
}
