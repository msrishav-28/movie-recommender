import { Suspense } from 'react';
import Link from 'next/link';
import { Search } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import Magnetic from '@/components/ui/Magnetic';
import { movieService } from '@/services/movie.service';
import { MasonryGrid } from '@/components/ui/MasonryGrid';

async function getTrendingMovies() {
  try {
    const data = await movieService.getTrending(1, 12);
    return data.items;
  } catch (error) {
    console.error('Failed to fetch trending movies:', error);
    return [];
  }
}

async function getPopularMovies() {
  try {
    const data = await movieService.getPopular(1, 12);
    return data.items;
  } catch (error) {
    console.error('Failed to fetch popular movies:', error);
    return [];
  }
}

export default async function HomePage() {
  const trendingMovies = await getTrendingMovies();
  // const popularMovies = await getPopularMovies(); // Keep for future use or mixing

  return (
    <div className="min-h-screen relative z-10 w-full overflow-x-hidden">

      {/* 
         THE HERO SECTION ("The Hook")
         Staggered, massive text reveal.
      */}
      <section className="relative min-h-[90vh] flex flex-col justify-center px-4 md:px-12 lg:px-24 pt-32">
        <div className="max-w-[1920px] mx-auto w-full">

          {/* Massive Type */}
          <div className="flex flex-col select-none">
            <h1 className="font-headline font-extrabold text-[15vw] leading-[0.8] tracking-tighter text-white mix-blend-difference animate-slide-up opacity-0" style={{ animationDelay: '0.2s' }}>
              CINEMA
            </h1>
            <div className="flex items-center justify-between w-full">
              <p className="hidden md:block font-mono text-sm tracking-widest text-text-tech mt-4 max-w-xs animate-fade-in opacity-0" style={{ animationDelay: '1.2s' }}>
                DIGITAL THEATER SYSTEM<br />
                AUDIO: DOLBY ATMOS<br />
                VISUAL: 4K HDR
              </p>
              <h1 className="font-headline font-extrabold text-[15vw] leading-[0.8] tracking-tighter text-white mix-blend-difference text-right animate-slide-up opacity-0" style={{ animationDelay: '0.4s' }}>
                REDEFINED
              </h1>
            </div>
          </div>

          {/* Magnetic Interaction Zone */}
          <div className="mt-24 flex flex-col md:flex-row items-center justify-between gap-12 animate-fade-in-up opacity-0" style={{ animationDelay: '0.8s' }}>

            <div className="flex items-center gap-6">
              <Magnetic>
                <Link href="/aesthetic">
                  <button className="group relative flex items-center justify-center w-24 h-24 rounded-full border border-white/20 bg-glass-base backdrop-blur-md transition-all duration-500 hover:scale-125 hover:border-klein-blue hover:shadow-glow-blue">
                    <Search className="w-8 h-8 text-white transition-transform duration-500 group-hover:scale-90" />
                  </button>
                </Link>
              </Magnetic>
              <span className="font-mono text-xs tracking-[0.2em] text-text-tech uppercase">
                Start Sequence
              </span>
            </div>

            <div className="flex gap-4">
              {['NOIR', 'SCIFI', 'ANIME'].map((tag) => (
                <Link key={tag} href={`/aesthetic?q=${tag.toLowerCase()}`}>
                  <span className="px-4 py-2 border border-white/10 rounded-full text-xs font-mono tracking-widest hover:bg-white hover:text-black transition-colors duration-300">
                    {tag}
                  </span>
                </Link>
              ))}
            </div>
          </div>

        </div>
      </section>

      {/* 
         THE INFINITE FILM STRIP 
         (Currently using MovieGrid as placeholder for Masonry)
      */}
      <section className="relative w-full py-32 px-4 md:px-12">
        <div className="flex items-end justify-between mb-16 border-b border-white/10 pb-4">
          <h2 className="font-cinematic text-6xl text-white">NOW SHOWING</h2>
          <span className="font-mono text-xs text-text-tech">SECTION: 01 // TRENDING</span>
        </div>

        <Suspense fallback={<div className="w-full h-96 flex items-center justify-center text-text-tech font-mono">LOADING_ASSETS...</div>}>
          <MasonryGrid items={trendingMovies} />
        </Suspense>
      </section>

    </div>
  );
}
