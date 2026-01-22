import type { Metadata, Viewport } from 'next';
import { Manrope, Bebas_Neue, JetBrains_Mono, Inter } from 'next/font/google';
import './globals.css';
import { Providers } from '@/components/providers';
import { Header } from '@/components/layout/Header';
import { Footer } from '@/components/layout/Footer';
import { Dock } from '@/components/layout/Dock'; // Imported Dock
import { Toaster } from 'sonner';
import SmoothScrolling from '@/components/ui/SmoothScrolling';
import dynamic from 'next/dynamic';

const CinematicBackground = dynamic(() => import('@/components/Three/CinematicBackground'), {
  ssr: false,
});

const CustomCursor = dynamic(() => import('@/components/ui/CustomCursor'), {
  ssr: false,
});

// Font Configuration
const manrope = Manrope({
  subsets: ['latin'],
  variable: '--font-manrope',
  display: 'swap',
});

const bebasNeue = Bebas_Neue({
  weight: '400',
  subsets: ['latin'],
  variable: '--font-bebas',
  display: 'swap',
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ['latin'],
  variable: '--font-jetbrains',
  display: 'swap',
});

// Using Inter as fallback/body if Satoshi is not available via Google Fonts
// In a real scenario, we'd setup local font for Satoshi. 
// For now, mapping 'Satoshi' variable to Inter for safety.
const inter = Inter({
  subsets: ['latin'],
  variable: '--font-satoshi',
  display: 'swap',
});

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 5,
  userScalable: true,
  themeColor: '#050505',
};

export const metadata: Metadata = {
  title: {
    default: 'CineAesthete - Digital Theater',
    template: '%s | CineAesthete',
  },
  description:
    "Experience cinema through a digital lens. Discovery reimagined.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="en"
      className={`${manrope.variable} ${inter.variable} ${bebasNeue.variable} ${jetbrainsMono.variable}`}
      suppressHydrationWarning
    >
      <body className="bg-void font-body text-text-primary antialiased selection:bg-klein-blue selection:text-white overflow-x-hidden">
        <SmoothScrolling>
          <Providers>
            {/* Atmospheric Layers */}
            <CinematicBackground />
            <div className="film-grain" />
            <CustomCursor />

            {/* Content Layer */}
            <div className="relative z-10 flex min-h-screen flex-col pb-24"> {/* Added padding bottom for Dock */}
              <div className="hidden md:block">
                {/* Optional: We can hide the full header on desktop if we want only the dock, but keeping it for now for Auth/Logo is safer unless we refactor Header completely. 
                     The USER request was "Implement Bottom Dock". Let's keep Header visible for now to avoid breaking Auth flow, but maybe minimal. 
                     Let's leave Header as is. It acts as a top bar. 
                 */}
                <Header />
              </div>
              {/* Mobile Header is handled inside Header component logic (it shows menu button on mobile) */}

              <main className="flex-1">{children}</main>
              <Footer />
            </div>

            {/* The Dock - Fixed Bottom */}
            <Dock />

            <Toaster
              position="bottom-right"
              toastOptions={{
                duration: 4000,
                className: '!bg-void-deep !border-white/10 !text-white',
                style: {
                  backdropFilter: 'blur(12px)',
                },
              }}
            />
          </Providers>
        </SmoothScrolling>
      </body>
    </html>
  );
}
