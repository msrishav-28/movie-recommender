'use client';

import * as DialogPrimitive from '@radix-ui/react-dialog';
import { X } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Button } from './Button';
import type { ReactNode } from 'react';

const Dialog = DialogPrimitive.Root;
// Radix Dialog Content usually needs Portal, but we'll try basic first or strictly follow existing logic if it was custom
const DialogContent = DialogPrimitive.Content;
const DialogTitle = DialogPrimitive.Title;
const DialogDescription = DialogPrimitive.Description;

const DialogHeader = ({ className, children }: { className?: string; children: ReactNode }) => (
  <div className={className}>{children}</div>
);
const DialogFooter = ({ className, children }: { className?: string; children: ReactNode }) => (
  <div className={className}>{children}</div>
);

export interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  description?: string;
  children: ReactNode;
  footer?: ReactNode;
  size?: 'sm' | 'md' | 'lg' | 'xl' | 'full';
  showCloseButton?: boolean;
}

export function Modal({
  isOpen,
  onClose,
  title,
  description,
  children,
  footer,
  size = 'md',
  showCloseButton = true,
}: ModalProps) {
  const sizes = {
    sm: 'max-w-sm',
    md: 'max-w-md',
    lg: 'max-w-2xl',
    xl: 'max-w-4xl',
    full: 'max-w-7xl',
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent
        className={cn(
          'fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-[210]',
          'w-full glass-heavy backdrop-blur-xl rounded-2xl shadow-2xl',
          'p-6 animate-fade-in',
          sizes[size]
        )}
      >
        {/* Header */}
        {(title || showCloseButton) && (
          <DialogHeader className="flex items-start justify-between mb-4">
            <div>
              {title && (
                <DialogTitle className="text-2xl font-bold">{title}</DialogTitle>
              )}
              {description && (
                <DialogDescription className="text-text-secondary mt-2">
                  {description}
                </DialogDescription>
              )}
            </div>
            {showCloseButton && (
              <button
                onClick={onClose}
                className="shrink-0 rounded-md p-2 hover:bg-white/5 transition-colors"
              >
                <X className="h-5 w-5" />
              </button>
            )}
          </DialogHeader>
        )}

        {/* Content */}
        <div className="overflow-y-auto max-h-[70vh]">{children}</div>

        {/* Footer */}
        {footer && (
          <DialogFooter className="flex items-center justify-end gap-3 mt-6 pt-6 border-t border-white/10">
            {footer}
          </DialogFooter>
        )}
      </DialogContent>

      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-void/80 backdrop-blur-sm z-[200]"
        onClick={onClose}
      />
    </Dialog>
  );
}
