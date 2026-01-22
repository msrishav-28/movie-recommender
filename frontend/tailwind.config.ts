import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  darkMode: ['class'],
  theme: {
    extend: {
      // VISUAL DNA: The Digital Theater System
      colors: {
        // The "Void" Palette
        'void': '#050505',       // Global Background (Infinite Dark)
        'void-deep': '#0A0A0A',  // Secondary Depth

        // Surface & Background Aliases (for legacy compatibility)
        'surface': '#0A0A0A',    // Alias for void-deep
        'background': '#050505', // Alias for void
        'border': 'rgba(255, 255, 255, 0.1)', // Standard border

        // Glass System (The "Lens")
        glass: {
          base: 'rgba(255, 255, 255, 0.03)',
          light: 'rgba(255, 255, 255, 0.05)',
          medium: 'rgba(255, 255, 255, 0.08)',
          heavy: 'rgba(255, 255, 255, 0.12)',
          border: 'rgba(255, 255, 255, 0.08)',
          highlight: 'rgba(255, 255, 255, 0.05)',
        },

        // The "Power" Accents (Neon & Laser)
        'klein-blue': '#002FA7',   // Primary Action / High Energy
        'electric-teal': '#00D9FF', // AI/Tech Indicators / Cyberpunk Cyan
        'cinema-gold': '#FFB800',   // Awards / Ratings / Golden Hour
        'signal-red': '#DC2626',    // Errors / Live Status / Recording Light

        // Brand Aliases (Legacy Compatibility → Maps to VISUAL_DNA colors)
        'brand-primary': '#002FA7',        // → klein-blue
        'brand-primary-light': 'rgba(0, 47, 167, 0.15)',
        'brand-secondary': '#00D9FF',      // → electric-teal
        'brand-secondary-light': 'rgba(0, 217, 255, 0.15)',
        'brand-tertiary': '#FFB800',       // → cinema-gold

        // Semantic Colors (Consistent with VISUAL_DNA accents)
        semantic: {
          error: '#DC2626',         // → signal-red
          'error-light': 'rgba(220, 38, 38, 0.15)',
          success: '#10B981',       // Emerald green
          'success-light': 'rgba(16, 185, 129, 0.15)',
          warning: '#F59E0B',       // Amber
          'warning-light': 'rgba(245, 158, 11, 0.15)',
          info: '#00D9FF',          // → electric-teal
        },

        // Text Hierarchy (Opacity based on White)
        text: {
          primary: 'rgba(255, 255, 255, 0.9)',
          secondary: 'rgba(255, 255, 255, 0.6)',
          tertiary: 'rgba(255, 255, 255, 0.4)',
          tech: 'rgba(255, 255, 255, 0.4)',
        },
      },

      // Z-Index Scale
      zIndex: {
        'dropdown': '50',
        'sticky': '100',
        'modal-backdrop': '200',
        'modal': '210',
        'tooltip': '300',
        'toast': '400',
      },

      // Typography System (The "Cast")
      fontFamily: {
        // The "Punch" / "Voice of God"
        headline: ['var(--font-manrope)', 'Manrope', 'sans-serif'],
        cinematic: ['var(--font-bebas)', 'Bebas Neue', 'sans-serif'],

        // The "Lens" / "Narrator"
        body: ['var(--font-satoshi)', 'Satoshi', 'sans-serif'],

        // The "Director's Monitor"
        mono: ['var(--font-jetbrains)', 'JetBrains Mono', 'monospace'],
      },

      // Letter Spacing (Tracking)
      letterSpacing: {
        tighter: '-0.04em',
        tight: '-0.02em',
        normal: '0',
        wide: '0.02em',
        widest: '0.1em',
      },

      // Line Height (Leading)
      lineHeight: {
        none: '0.85', // Aggressive headlines
        tight: '1.0',
        normal: '1.5',
        relaxed: '1.6',
      },

      // Animations & Keyframes
      animation: {
        'fade-in': 'fade-in 0.6s cubic-bezier(0.22, 1, 0.36, 1) forwards',
        'fade-in-up': 'fade-in-up 0.8s cubic-bezier(0.22, 1, 0.36, 1) forwards',
        'scale-up': 'scale-up 0.6s cubic-bezier(0.22, 1, 0.36, 1) forwards',
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        'fade-in': {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        'fade-in-up': {
          '0%': { opacity: '0', transform: 'translateY(40px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'scale-up': {
          '0%': { transform: 'scale(0.95)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        }
      },

      // Extended Spacing
      spacing: {
        '18': '4.5rem',
        '112': '28rem',
        '128': '32rem',
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('@tailwindcss/forms'),
  ],
}

export default config
