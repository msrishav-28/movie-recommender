'use client';

import { useState } from 'react';
import { ThumbsUp, AlertTriangle, Eye, EyeOff } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { Review } from '@/services/rating.service';
import { formatDistanceToNow } from '@/lib/utils';

interface ReviewCardProps {
  review: Review;
  onLike?: () => void;
}

export function ReviewCard({ review, onLike }: ReviewCardProps) {
  const [showSpoiler, setShowSpoiler] = useState(false);
  const [isLiked, setIsLiked] = useState(false);

  const handleLike = () => {
    setIsLiked(!isLiked);
    onLike?.();
  };

  const getSentimentColor = (label?: string) => {
    switch (label?.toLowerCase()) {
      case 'positive':
        return 'success';
      case 'negative':
        return 'error';
      default:
        return 'default';
    }
  };

  return (
    <Card variant="glass">
      <CardContent className="p-6">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div>
            {review.title && (
              <h4 className="font-semibold text-lg mb-1">{review.title}</h4>
            )}
            <div className="flex items-center gap-2 text-sm text-text-tertiary">
              <span>{review.user?.username || 'Anonymous'}</span>
              <span>•</span>
              <span>{formatDistanceToNow(review.created_at)}</span>
            </div>
          </div>

          {/* Sentiment Badge */}
          {review.sentiment_label && (
            <Badge variant={getSentimentColor(review.sentiment_label)}>
              {review.sentiment_label}
            </Badge>
          )}
        </div>

        {/* Spoiler Warning */}
        {review.is_spoiler && !showSpoiler && (
          <div className="p-4 bg-warning/10 border border-warning/20 rounded-lg mb-4">
            <div className="flex items-center gap-2 mb-2">
              <AlertTriangle className="h-5 w-5 text-warning" />
              <p className="font-medium text-warning">Spoiler Warning</p>
            </div>
            <p className="text-sm text-text-secondary mb-3">
              This review contains spoilers. Click to reveal.
            </p>
            <Button
              size="sm"
              variant="outline"
              onClick={() => setShowSpoiler(true)}
              icon={<Eye className="h-4 w-4" />}
            >
              Show Review
            </Button>
          </div>
        )}

        {/* Content */}
        {(!review.is_spoiler || showSpoiler) && (
          <>
            <p className="text-text-secondary leading-relaxed mb-4">{review.content}</p>

            {/* Actions */}
            <div className="flex items-center gap-4 pt-4 border-t border-white/10">
              <Button
                size="sm"
                variant={isLiked ? 'primary' : 'ghost'}
                icon={<ThumbsUp className={`h-4 w-4 ${isLiked ? 'fill-current' : ''}`} />}
                onClick={handleLike}
              >
                {review.likes_count + (isLiked ? 1 : 0)} Helpful
              </Button>

              {review.is_spoiler && showSpoiler && (
                <Button
                  size="sm"
                  variant="ghost"
                  icon={<EyeOff className="h-4 w-4" />}
                  onClick={() => setShowSpoiler(false)}
                >
                  Hide
                </Button>
              )}
            </div>
          </>
        )}
      </CardContent>
    </Card>
  );
}
