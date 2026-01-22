'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Search, Menu, User, LogOut, Settings, Film } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { useAuthStore } from '@/store/authStore';
import { useUIStore } from '@/store/uiStore';
import { cn } from '@/lib/utils';

export function Header() {
  const pathname = usePathname();
  const { isAuthenticated, user, logout } = useAuthStore();
  const { toggleMobileMenu, setSearchOpen } = useUIStore();

  const navLinks = [
    { href: '/', label: 'Home' },
    { href: '/browse', label: 'Browse' },
    { href: '/aesthetic', label: 'Aesthetic Search' },
    { href: '/trending', label: 'Trending' },
  ];

  return (
    <header className="sticky top-0 z-[100] glass-heavy border-b border-white/10 safe-top">
      <div className="container-padding">
        <div className="flex h-16 items-center justify-between">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2 group">
            <Film className="h-8 w-8 text-klein-blue group-hover:scale-110 transition-transform" />
            <span className="font-cinematic text-2xl tracking-wider hidden sm:inline">
              CINEAESTHETE
            </span>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-6">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className={cn(
                  'text-sm font-medium transition-colors hover:text-klein-blue',
                  pathname === link.href ? 'text-text-primary' : 'text-text-secondary'
                )}
              >
                {link.label}
              </Link>
            ))}
          </nav>

          {/* Actions */}
          <div className="flex items-center gap-3">
            <Button
              variant="ghost"
              size="sm"
              icon={<Search className="h-5 w-5" />}
              onClick={() => setSearchOpen(true)}
              className="hidden sm:inline-flex"
            />

            {isAuthenticated ? (
              <div className="hidden md:flex items-center gap-2">
                <Link href="/dashboard">
                  <Button variant="ghost" size="sm">
                    Dashboard
                  </Button>
                </Link>
                <Link href="/watchlist">
                  <Button variant="ghost" size="sm">
                    Watchlist
                  </Button>
                </Link>
                <div className="flex items-center gap-2 ml-2 pl-2 border-l border-white/10">
                  <Link href="/profile">
                    <Button variant="ghost" size="sm" icon={<User className="h-4 w-4" />}>
                      {user?.username}
                    </Button>
                  </Link>
                  <Button
                    variant="ghost"
                    size="sm"
                    icon={<LogOut className="h-4 w-4" />}
                    onClick={() => logout()}
                  >
                    Logout
                  </Button>
                </div>
              </div>
            ) : (
              <div className="hidden md:flex items-center gap-2">
                <Link href="/login">
                  <Button variant="ghost" size="sm">
                    Login
                  </Button>
                </Link>
                <Link href="/register">
                  <Button variant="primary" size="sm">
                    Sign Up
                  </Button>
                </Link>
              </div>
            )}

            {/* Mobile Menu Button */}
            <Button
              variant="ghost"
              size="sm"
              icon={<Menu className="h-5 w-5" />}
              onClick={toggleMobileMenu}
              className="md:hidden"
            />
          </div>
        </div>
      </div>
    </header>
  );
}
