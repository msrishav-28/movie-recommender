'use client';

import { useState } from 'react';
import { MessageSquare, AlertTriangle } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Checkbox } from '@/components/ui/Checkbox';
import { Card, CardContent } from '@/components/ui/Card';
import { ratingService, CreateReviewRequest } from '@/services/rating.service';
import { toast } from 'sonner';

interface ReviewFormProps {
  movieId: number;
  ratingId: number;
  onSuccess?: () => void;
  onCancel?: () => void;
}

export function ReviewForm({ movieId, ratingId, onSuccess, onCancel }: ReviewFormProps) {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [isSpoiler, setIsSpoiler] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (content.length < 10) {
      toast.error('Review must be at least 10 characters long');
      return;
    }

    try {
      setIsLoading(true);

      const data: CreateReviewRequest = {
        movie_id: movieId,
        rating_id: ratingId,
        title: title.trim() || undefined,
        content: content.trim(),
        is_spoiler: isSpoiler,
      };

      await ratingService.createReview(data);
      toast.success('Review posted successfully!');
      onSuccess?.();

      // Reset form
      setTitle('');
      setContent('');
      setIsSpoiler(false);
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to post review');
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card variant="glass">
      <CardContent className="p-6">
        <div className="flex items-center gap-2 mb-4">
          <MessageSquare className="h-5 w-5 text-klein-blue" />
          <h3 className="text-lg font-semibold">Write a Review</h3>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Title */}
          <div>
            <Input
              label="Title (Optional)"
              placeholder="Sum up your review in one line"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              maxLength={500}
            />
          </div>

          {/* Content */}
          <div>
            <label className="block text-sm font-medium mb-2">
              Review <span className="text-klein-blue">*</span>
            </label>
            <textarea
              className="w-full px-4 py-3 bg-void-deep/50 border border-white/10 rounded-lg focus:outline-none focus:ring-2 focus:ring-klein-blue/50 text-text-primary placeholder:text-white/40 min-h-[120px] resize-y"
              placeholder="Share your thoughts about this movie..."
              value={content}
              onChange={(e) => setContent(e.target.value)}
              minLength={10}
              required
            />
            <p className="text-xs text-white/40 mt-1">
              {content.length < 10
                ? `At least ${10 - content.length} more characters needed`
                : `${content.length} characters`}
            </p>
          </div>

          {/* Spoiler Warning */}
          <div className="flex items-start gap-3 p-4 bg-amber-500/10 border border-amber-500/20 rounded-lg">
            <AlertTriangle className="h-5 w-5 text-amber-500 shrink-0 mt-0.5" />
            <div className="flex-1">
              <Checkbox
                label="This review contains spoilers"
                checked={isSpoiler}
                onChange={setIsSpoiler}
              />
              <p className="text-xs text-white/40 mt-1">
                Check this if your review reveals major plot points
              </p>
            </div>
          </div>

          {/* Actions */}
          <div className="flex justify-end gap-3 pt-2">
            {onCancel && (
              <Button type="button" variant="ghost" onClick={onCancel} disabled={isLoading}>
                Cancel
              </Button>
            )}
            <Button
              type="submit"
              variant="primary"
              loading={isLoading}
              disabled={content.length < 10}
            >
              Post Review
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}
