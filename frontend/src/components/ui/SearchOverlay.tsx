'use client';

import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, X } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useRouter } from 'next/navigation';

interface SearchOverlayProps {
    isOpen: boolean;
    onClose: () => void;
}

export default function SearchOverlay({ isOpen, onClose }: SearchOverlayProps) {
    const [query, setQuery] = useState('');
    const inputRef = useRef<HTMLInputElement>(null);
    const router = useRouter();

    useEffect(() => {
        if (isOpen) {
            setTimeout(() => inputRef.current?.focus(), 100);
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = 'unset';
        }
        return () => { document.body.style.overflow = 'unset'; };
    }, [isOpen]);

    const handleSearch = (e: React.FormEvent) => {
        e.preventDefault();
        if (query.trim()) {
            router.push(`/aesthetic?q=${encodeURIComponent(query)}`);
            onClose();
        }
    };

    return (
        <AnimatePresence>
            {isOpen && (
                <div className="fixed inset-0 z-[9999] flex items-center justify-center">
                    {/* Backdrop (The Void) */}
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        onClick={onClose}
                        className="absolute inset-0 bg-void/95 backdrop-blur-xl"
                    />

                    {/* Search Container */}
                    <motion.div
                        initial={{ scale: 0.9, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        exit={{ scale: 0.9, opacity: 0 }}
                        transition={{ type: 'spring', damping: 20, stiffness: 300 }}
                        className="relative w-full max-w-4xl px-4 md:px-0 z-10"
                    >
                        <form onSubmit={handleSearch} className="relative group">
                            {/* Cyberpunk Decor */}
                            <div className="absolute -left-8 top-1/2 -translate-y-1/2 hidden md:block">
                                <span className="text-text-tech font-mono text-xs tracking-widest opacity-50">INPUT_STREAM_01</span>
                            </div>

                            <div className="relative flex items-center border-b-2 border-white/20 group-focus-within:border-white transition-colors duration-300 pb-4">
                                <Search className="w-8 h-8 text-white/50 mr-6 group-focus-within:text-electric-teal transition-colors" />

                                <input
                                    ref={inputRef}
                                    type="text"
                                    value={query}
                                    onChange={(e) => setQuery(e.target.value)}
                                    placeholder="Describe the vibe..."
                                    className="w-full bg-transparent text-4xl md:text-6xl font-headline font-bold text-white placeholder:text-white/20 focus:outline-none"
                                    autoComplete="off"
                                />

                                {/* Blinking Block Cursor (Visual only, usually hard to sync with real cursor, so effectively handled by native input caret, but we can add a visual block at the end if we want) */}
                                <motion.div
                                    animate={{ opacity: [1, 0] }}
                                    transition={{ repeat: Infinity, duration: 0.8 }}
                                    className="w-4 h-12 bg-electric-teal ml-2 hidden md:block" // Decorative cursor block
                                />
                            </div>

                            {/* Helper Text */}
                            <div className="mt-4 flex justify-between text-text-tech font-mono text-xs tracking-widest">
                                <span>PRESS ENTER TO SEARCH</span>
                                <span>ESC TO CLOSE</span>
                            </div>
                        </form>
                    </motion.div>

                    <button
                        onClick={onClose}
                        className="absolute top-8 right-8 text-white/50 hover:text-white transition-colors"
                    >
                        <div className="flex items-center gap-2 font-mono text-xs">
                            <span>CLOSE_MODAL</span>
                            <X className="w-6 h-6" />
                        </div>
                    </button>
                </div>
            )}
        </AnimatePresence>
    );
}
