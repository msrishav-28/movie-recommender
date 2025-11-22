'use client';

import { useState } from 'react';
import { X, Star } from 'lucide-react';
import { Modal } from '@/components/ui/Modal';
import { Button } from '@/components/ui/Button';
import { Slider } from '@/components/ui/Slider';
import { ratingService, CreateRatingRequest } from '@/services/rating.service';
import { toast } from 'sonner';

interface RatingModalProps {
  movieId: number;
  movieTitle: string;
  isOpen: boolean;
  onClose: () => void;
  onSuccess?: () => void;
}

export function RatingModal({
  movieId,
  movieTitle,
  isOpen,
  onClose,
  onSuccess,
}: RatingModalProps) {
  const [overallRating, setOverallRating] = useState(5);
  const [plotRating, setPlotRating] = useState<number | null>(null);
  const [actingRating, setActingRating] = useState<number | null>(null);
  const [cinematographyRating, setCinematographyRating] = useState<number | null>(null);
  const [soundtrackRating, setSoundtrackRating] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async () => {
    try {
      setIsLoading(true);

      const data: CreateRatingRequest = {
        movie_id: movieId,
        overall_rating: overallRating / 2, // Convert 0-10 to 0-5
        plot_rating: plotRating ? plotRating / 2 : undefined,
        acting_rating: actingRating ? actingRating / 2 : undefined,
        cinematography_rating: cinematographyRating ? cinematographyRating / 2 : undefined,
        soundtrack_rating: soundtrackRating ? soundtrackRating / 2 : undefined,
      };

      await ratingService.rateMovie(data);
      toast.success('Rating submitted successfully!');
      onSuccess?.();
      onClose();
    } catch (error) {
      toast.error('Failed to submit rating');
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={`Rate: ${movieTitle}`}>
      <div className="space-y-6">
        {/* Overall Rating */}
        <div>
          <label className="block text-sm font-medium mb-3">
            Overall Rating <span className="text-brand-primary">*</span>
          </label>
          <div className="flex items-center gap-4">
            <Slider
              value={overallRating}
              onChange={setOverallRating}
              min={0}
              max={10}
              step={0.5}
            />
            <div className="flex items-center gap-1 min-w-[60px]">
              <Star className="h-5 w-5 fill-brand-tertiary text-brand-tertiary" />
              <span className="text-xl font-bold">{overallRating.toFixed(1)}</span>
            </div>
          </div>
        </div>

        {/* Detailed Ratings */}
        <div className="pt-4 border-t border-white/10">
          <p className="text-sm text-text-secondary mb-4">Detailed Ratings (Optional)</p>

          {/* Plot */}
          <div className="mb-4">
            <label className="block text-sm mb-2">Plot & Story</label>
            <div className="flex items-center gap-4">
              <Slider
                value={plotRating ?? 5}
                onChange={setPlotRating}
                min={0}
                max={10}
                step={0.5}
              />
              <span className="min-w-[60px] text-center">
                {plotRating ? plotRating.toFixed(1) : '-'}
              </span>
            </div>
          </div>

          {/* Acting */}
          <div className="mb-4">
            <label className="block text-sm mb-2">Acting & Performance</label>
            <div className="flex items-center gap-4">
              <Slider
                value={actingRating ?? 5}
                onChange={setActingRating}
                min={0}
                max={10}
                step={0.5}
              />
              <span className="min-w-[60px] text-center">
                {actingRating ? actingRating.toFixed(1) : '-'}
              </span>
            </div>
          </div>

          {/* Cinematography */}
          <div className="mb-4">
            <label className="block text-sm mb-2">Cinematography & Visuals</label>
            <div className="flex items-center gap-4">
              <Slider
                value={cinematographyRating ?? 5}
                onChange={setCinematographyRating}
                min={0}
                max={10}
                step={0.5}
              />
              <span className="min-w-[60px] text-center">
                {cinematographyRating ? cinematographyRating.toFixed(1) : '-'}
              </span>
            </div>
          </div>

          {/* Soundtrack */}
          <div>
            <label className="block text-sm mb-2">Soundtrack & Music</label>
            <div className="flex items-center gap-4">
              <Slider
                value={soundtrackRating ?? 5}
                onChange={setSoundtrackRating}
                min={0}
                max={10}
                step={0.5}
              />
              <span className="min-w-[60px] text-center">
                {soundtrackRating ? soundtrackRating.toFixed(1) : '-'}
              </span>
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="flex justify-end gap-3 pt-4">
          <Button variant="ghost" onClick={onClose} disabled={isLoading}>
            Cancel
          </Button>
          <Button variant="primary" onClick={handleSubmit} loading={isLoading}>
            Submit Rating
          </Button>
        </div>
      </div>
    </Modal>
  );
}
