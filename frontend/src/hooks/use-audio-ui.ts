'use client';

import { useCallback, useRef, useEffect } from 'react';

// Frequencies for our 'Digital Theater' sound palette
const SOUNDS = {
    hover: { freq: 400, type: 'sine', duration: 0.05, vol: 0.05 },
    click: { freq: 150, type: 'triangle', duration: 0.1, vol: 0.1 },
    success: { freq: 880, type: 'sine', duration: 0.2, vol: 0.1 },
} as const;

export function useAudioUI() {
    const audioContext = useRef<AudioContext | null>(null);

    useEffect(() => {
        // Lazy init audio context on first user interaction to comply with browser policies
        const initAudio = () => {
            if (!audioContext.current) {
                audioContext.current = new (window.AudioContext || (window as any).webkitAudioContext)();
            }
        };

        window.addEventListener('click', initAudio, { once: true });
        return () => window.removeEventListener('click', initAudio);
    }, []);

    const playSound = useCallback((type: keyof typeof SOUNDS) => {
        if (!audioContext.current) return;

        try {
            const ctx = audioContext.current;
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            const config = SOUNDS[type];

            osc.type = config.type as OscillatorType;
            osc.frequency.setValueAtTime(config.freq, ctx.currentTime);

            // Envelope
            gain.gain.setValueAtTime(0, ctx.currentTime);
            gain.gain.linearRampToValueAtTime(config.vol, ctx.currentTime + 0.01);
            gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + config.duration);

            osc.connect(gain);
            gain.connect(ctx.destination);

            osc.start();
            osc.stop(ctx.currentTime + config.duration + 0.1);
        } catch (e) {
            // Audio failed, fail silently
            console.warn('Audio UI Error:', e);
        }
    }, []);

    return { playSound };
}
