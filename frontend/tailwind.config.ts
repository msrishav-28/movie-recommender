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
      // Design System - Color Tokens
      colors: {
        // Cinematic Background System
        background: {
          DEFAULT: '#0A0E13',
          secondary: '#131921',
          tertiary: '#1C2633',
          quaternary: '#2A3544',
        },
        // Surface Colors
        surface: {
          DEFAULT: '#131921',
          hover: '#1C2633',
          active: '#2A3544',
        },
        // Text Hierarchy
        text: {
          primary: '#F8F9FA',
          secondary: '#B8BFC7',
          tertiary: '#6C7580',
          disabled: '#404854',
        },
        // Brand Accent Colors
        brand: {
          primary: '#E50914',
          'primary-hover': '#F21A24',
          'primary-active': '#CC0812',
          'primary-light': 'rgba(229, 9, 20, 0.1)',
          secondary: '#00D9FF',
          'secondary-hover': '#1AE0FF',
          'secondary-active': '#00C2E6',
          'secondary-light': 'rgba(0, 217, 255, 0.1)',
          tertiary: '#FFB800',
          'tertiary-hover': '#FFC51A',
          'tertiary-active': '#E6A600',
          'tertiary-light': 'rgba(255, 184, 0, 0.1)',
        },
        // Semantic Colors
        semantic: {
          success: '#00FF88',
          'success-light': 'rgba(0, 255, 136, 0.1)',
          warning: '#FFB800',
          'warning-light': 'rgba(255, 184, 0, 0.1)',
          error: '#FF4757',
          'error-light': 'rgba(255, 71, 87, 0.1)',
          info: '#5D9CEC',
          'info-light': 'rgba(93, 156, 236, 0.1)',
        },
        // Glass Effect Colors
        glass: {
          light: 'rgba(255, 255, 255, 0.05)',
          'light-hover': 'rgba(255, 255, 255, 0.08)',
          medium: 'rgba(255, 255, 255, 0.08)',
          'medium-hover': 'rgba(255, 255, 255, 0.12)',
          heavy: 'rgba(255, 255, 255, 0.12)',
          'heavy-hover': 'rgba(255, 255, 255, 0.16)',
        },
        // Border Colors
        border: {
          DEFAULT: 'rgba(255, 255, 255, 0.1)',
          hover: 'rgba(255, 255, 255, 0.2)',
          focus: '#00D9FF',
          error: 'rgba(255, 71, 87, 0.5)',
          disabled: 'rgba(255, 255, 255, 0.05)',
        },
      },

      // Typography Scale
      fontSize: {
        xs: ['clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem)', { lineHeight: '1.5' }],
        sm: ['clamp(0.875rem, 0.825rem + 0.25vw, 1rem)', { lineHeight: '1.5' }],
        base: ['clamp(1rem, 0.95rem + 0.25vw, 1.125rem)', { lineHeight: '1.5' }],
        lg: ['clamp(1.125rem, 1.05rem + 0.375vw, 1.25rem)', { lineHeight: '1.5' }],
        xl: ['clamp(1.25rem, 1.15rem + 0.5vw, 1.5rem)', { lineHeight: '1.375' }],
        '2xl': ['clamp(1.5rem, 1.35rem + 0.75vw, 2rem)', { lineHeight: '1.25' }],
        '3xl': ['clamp(2rem, 1.7rem + 1.5vw, 3rem)', { lineHeight: '1.25' }],
        '4xl': ['clamp(3rem, 2.4rem + 3vw, 5rem)', { lineHeight: '1.1' }],
        '5xl': ['clamp(4rem, 3rem + 5vw, 8rem)', { lineHeight: '1' }],
        '6xl': ['clamp(5rem, 3.75rem + 6.25vw, 10rem)', { lineHeight: '1' }],
      },

      fontFamily: {
        display: ['var(--font-inter)', 'Inter', 'sans-serif'],
        body: ['var(--font-sf-pro)', 'SF Pro Display', 'Inter', 'sans-serif'],
        cinematic: ['var(--font-bebas)', 'Bebas Neue', 'Impact', 'sans-serif'],
        mono: ['var(--font-jetbrains)', 'JetBrains Mono', 'Consolas', 'monospace'],
      },

      // Spacing System (8-point grid)
      spacing: {
        '0.5': '0.125rem',
        '1.5': '0.375rem',
        '2.5': '0.625rem',
        '3.5': '0.875rem',
        '4.5': '1.125rem',
        '18': '4.5rem',
        '22': '5.5rem',
        '26': '6.5rem',
        '30': '7.5rem',
      },

      // Border Radius Scale
      borderRadius: {
        xs: '0.25rem',
        sm: '0.375rem',
        DEFAULT: '0.5rem',
        md: '0.5rem',
        lg: '0.75rem',
        xl: '1rem',
        '2xl': '1.5rem',
        '3xl': '2rem',
      },

      // Elevation & Shadows
      boxShadow: {
        xs: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        sm: '0 2px 8px 0 rgba(0, 0, 0, 0.12), 0 1px 2px 0 rgba(0, 0, 0, 0.08)',
        DEFAULT: '0 4px 16px 0 rgba(0, 0, 0, 0.16), 0 2px 8px 0 rgba(0, 0, 0, 0.08)',
        md: '0 4px 16px 0 rgba(0, 0, 0, 0.16), 0 2px 8px 0 rgba(0, 0, 0, 0.08)',
        lg: '0 8px 32px 0 rgba(0, 0, 0, 0.24), 0 4px 16px 0 rgba(0, 0, 0, 0.12)',
        xl: '0 16px 64px 0 rgba(0, 0, 0, 0.32), 0 8px 32px 0 rgba(0, 0, 0, 0.16)',
        '2xl': '0 24px 96px 0 rgba(0, 0, 0, 0.4), 0 12px 48px 0 rgba(0, 0, 0, 0.2)',
        inner: 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)',
        'inner-lg': 'inset 0 4px 8px 0 rgba(0, 0, 0, 0.12)',
        glow: '0 0 20px rgba(229, 9, 20, 0.4)',
        'glow-secondary': '0 0 20px rgba(0, 217, 255, 0.4)',
        'glow-success': '0 0 20px rgba(0, 255, 136, 0.4)',
      },

      // Animation Durations & Easings
      transitionDuration: {
        '0': '0ms',
        '100': '100ms',
        '200': '200ms',
        '300': '300ms',
        '400': '400ms',
        '500': '500ms',
        '800': '800ms',
        '1200': '1200ms',
      },

      transitionTimingFunction: {
        'smooth': 'cubic-bezier(0.76, 0, 0.24, 1)',
        'expo': 'cubic-bezier(0.87, 0, 0.13, 1)',
        'back': 'cubic-bezier(0.34, 1.56, 0.64, 1)',
        'elastic': 'cubic-bezier(0.68, -0.55, 0.265, 1.55)',
      },

      // Breakpoints (already configured but explicitly documented)
      screens: {
        'xs': '320px',
        'sm': '640px',
        'md': '768px',
        'lg': '1024px',
        'xl': '1280px',
        '2xl': '1536px',
        '3xl': '1920px',
      },

      // Z-index Layering
      zIndex: {
        '0': '0',
        '10': '10',
        '20': '20',
        '30': '30',
        '40': '40',
        '50': '50',
        'dropdown': '1000',
        'sticky': '1100',
        'fixed': '1200',
        'modal-backdrop': '1300',
        'modal': '1400',
        'popover': '1500',
        'tooltip': '1600',
        'notification': '1700',
        'max': '9999',
      },

      // Backdrop Blur
      backdropBlur: {
        'xs': '8px',
        'sm': '12px',
        'DEFAULT': '16px',
        'md': '24px',
        'lg': '32px',
        'xl': '48px',
      },

      // Animation Keyframes
      keyframes: {
        'fade-in': {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        'fade-out': {
          '0%': { opacity: '1' },
          '100%': { opacity: '0' },
        },
        'slide-up': {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        'slide-down': {
          '0%': { transform: 'translateY(-20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        'slide-left': {
          '0%': { transform: 'translateX(20px)', opacity: '0' },
          '100%': { transform: 'translateX(0)', opacity: '1' },
        },
        'slide-right': {
          '0%': { transform: 'translateX(-20px)', opacity: '0' },
          '100%': { transform: 'translateX(0)', opacity: '1' },
        },
        'scale-in': {
          '0%': { transform: 'scale(0.9)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
        shimmer: {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(100%)' },
        },
        pulse: {
          '0%, 100%': { opacity: '0.5' },
          '50%': { opacity: '1' },
        },
        spin: {
          '0%': { transform: 'rotate(0deg)' },
          '100%': { transform: 'rotate(360deg)' },
        },
        bounce: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        },
      },

      animation: {
        'fade-in': 'fade-in 0.3s ease-out',
        'fade-out': 'fade-out 0.2s ease-in',
        'slide-up': 'slide-up 0.4s ease-out',
        'slide-down': 'slide-down 0.4s ease-out',
        'slide-left': 'slide-left 0.3s ease-out',
        'slide-right': 'slide-right 0.3s ease-out',
        'scale-in': 'scale-in 0.3s ease-out',
        'shimmer': 'shimmer 2s linear infinite',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'spin-slow': 'spin 3s linear infinite',
        'bounce-slow': 'bounce 2s infinite',
      },

      // Container Widths
      maxWidth: {
        'content': '1800px',
        'reading': '680px',
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('@tailwindcss/forms'),
  ],
}

export default config
