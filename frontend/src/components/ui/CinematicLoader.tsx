'use client';

import { motion } from 'framer-motion';

interface CinematicLoaderProps {
    className?: string;
}

export function CinematicLoader({ className }: CinematicLoaderProps) {
    return (
        <div className={`flex flex-col items-center justify-center gap-4 ${className}`}>
            {/* Abstract Film Strip */}
            <div className="flex gap-1.5 h-8 items-center">
                {[...Array(5)].map((_, i) => (
                    <motion.div
                        key={i}
                        className="w-1.5 h-8 bg-electric-teal"
                        initial={{ scaleY: 0.2, opacity: 0.2 }}
                        animate={{
                            scaleY: [0.2, 1, 0.2],
                            opacity: [0.2, 1, 0.2],
                            backgroundColor: ["#00D9FF", "#002FA7", "#00D9FF"]
                        }}
                        transition={{
                            duration: 1,
                            repeat: Infinity,
                            delay: i * 0.1,
                            ease: "easeInOut"
                        }}
                    />
                ))}
            </div>

            {/* Loading Text */}
            <motion.p
                className="font-mono text-xs tracking-[0.3em] text-text-tech uppercase"
                animate={{ opacity: [0.3, 1, 0.3] }}
                transition={{ duration: 2, repeat: Infinity }}
            >
                Initializing
            </motion.p>
        </div>
    );
}
