import type { Metadata, Viewport } from 'next';
import { Inter, JetBrains_Mono } from 'next/font/google';
import localFont from 'next/font/local';
import './globals.css';
import { Providers } from '@/components/providers';
import { Header } from '@/components/layout/Header';
import { Footer } from '@/components/layout/Footer';
import { Toaster } from 'sonner';

// Font Configuration
const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
  preload: true,
  fallback: ['system-ui', 'arial'],
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ['latin'],
  variable: '--font-jetbrains',
  display: 'swap',
  weight: ['400', '500', '600', '700'],
});

const sfPro = localFont({
  src: [
    {
      path: '../fonts/SF-Pro-Display-Regular.woff2',
      weight: '400',
      style: 'normal',
    },
    {
      path: '../fonts/SF-Pro-Display-Medium.woff2',
      weight: '500',
      style: 'normal',
    },
    {
      path: '../fonts/SF-Pro-Display-Semibold.woff2',
      weight: '600',
      style: 'normal',
    },
    {
      path: '../fonts/SF-Pro-Display-Bold.woff2',
      weight: '700',
      style: 'normal',
    },
  ],
  variable: '--font-sf-pro',
  display: 'swap',
  fallback: ['Inter', 'system-ui'],
});

const bebasNeue = localFont({
  src: '../fonts/BebasNeue-Regular.woff2',
  variable: '--font-bebas',
  display: 'swap',
  weight: '400',
});

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 5,
  userScalable: true,
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#FAFBFC' },
    { media: '(prefers-color-scheme: dark)', color: '#0A0E13' },
  ],
};

export const metadata: Metadata = {
  title: {
    default: 'CineAesthete - Discover Movies by Vibe',
    template: '%s | CineAesthete',
  },
  description:
    "The world's first aesthetic-based movie discovery platform. Search for films by visual vibes, mood, and cinematic atmosphere. Powered by AI.",
  keywords: [
    'movies',
    'aesthetic search',
    'vibe-based',
    'film discovery',
    'recommendations',
    'AI-powered',
    'cinematic',
  ],
  authors: [{ name: 'CineAesthete Team' }],
  creator: 'CineAesthete',
  publisher: 'CineAesthete',
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://cineaesthete.com',
    title: 'CineAesthete - Discover Movies by Vibe',
    description:
      'Search for movies by aesthetic vibes and visual atmosphere. AI-powered film discovery platform.',
    siteName: 'CineAesthete',
    images: [
      {
        url: '/og-image.jpg',
        width: 1200,
        height: 630,
        alt: 'CineAesthete',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'CineAesthete - Discover Movies by Vibe',
    description:
      'Search for movies by aesthetic vibes and visual atmosphere. AI-powered film discovery.',
    images: ['/og-image.jpg'],
    creator: '@cineaesthete',
  },
  icons: {
    icon: [
      { url: '/favicon.ico' },
      { url: '/icon.png', type: 'image/png', sizes: '32x32' },
    ],
    apple: [
      { url: '/apple-icon.png', sizes: '180x180', type: 'image/png' },
    ],
  },
  manifest: '/manifest.json',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="en"
      className={`${inter.variable} ${sfPro.variable} ${bebasNeue.variable} ${jetbrainsMono.variable}`}
      suppressHydrationWarning
    >
      <body className="bg-background font-body text-text-primary antialiased">
        <Providers>
          <div className="relative flex min-h-screen flex-col">
            <Header />
            <main className="flex-1">{children}</main>
            <Footer />
          </div>
          <Toaster
            position="top-right"
            toastOptions={{
              duration: 4000,
              className: 'glass-heavy border-border',
              style: {
                background: 'rgba(255, 255, 255, 0.12)',
                backdropFilter: 'blur(24px)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                color: '#F8F9FA',
              },
            }}
          />
        </Providers>
      </body>
    </html>
  );
}
