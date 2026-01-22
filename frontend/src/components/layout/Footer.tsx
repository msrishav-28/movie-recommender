import Link from 'next/link';
import { Film, Github, Twitter, Instagram } from 'lucide-react';

export function Footer() {
  const currentYear = new Date().getFullYear();

  const footerLinks = {
    Product: [
      { label: 'Browse Movies', href: '/browse' },
      { label: 'Aesthetic Search', href: '/aesthetic' },
      { label: 'Trending', href: '/trending' },
      { label: 'Top Rated', href: '/top-rated' },
    ],
    Company: [
      { label: 'About', href: '/about' },
      { label: 'Blog', href: '/blog' },
      { label: 'Careers', href: '/careers' },
      { label: 'Contact', href: '/contact' },
    ],
    Support: [
      { label: 'Help Center', href: '/help' },
      { label: 'Terms of Service', href: '/terms' },
      { label: 'Privacy Policy', href: '/privacy' },
      { label: 'Cookie Policy', href: '/cookies' },
    ],
    Connect: [
      { label: 'Twitter', href: '#', icon: Twitter },
      { label: 'Instagram', href: '#', icon: Instagram },
      { label: 'GitHub', href: '#', icon: Github },
    ],
  };

  return (
    <footer className="border-t border-white/10 bg-void-deep mt-auto">
      <div className="container-padding py-12 lg:py-16">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 lg:gap-12">
          {/* Logo & Description */}
          <div className="col-span-2 md:col-span-1">
            <Link href="/" className="flex items-center gap-2 mb-4">
              <Film className="h-8 w-8 text-klein-blue" />
              <span className="font-cinematic text-xl tracking-wider">CINEAESTHETE</span>
            </Link>
            <p className="text-sm text-white/40 max-w-xs">
              Discover movies through aesthetic vibes and visual atmosphere. The world&apos;s first
              AI-powered aesthetic search.
            </p>
          </div>

          {/* Links */}
          {Object.entries(footerLinks).map(([category, links]) => (
            <div key={category}>
              <h3 className="font-semibold text-text-primary mb-4">{category}</h3>
              <ul className="space-y-3">
                {links.map((link) => (
                  <li key={link.label}>
                    <Link
                      href={link.href}
                      className="text-sm text-white/40 hover:text-text-primary transition-colors inline-flex items-center gap-2"
                    >
                      {'icon' in link && link.icon && <link.icon className="h-4 w-4" />}
                      {link.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* Bottom Bar */}
        <div className="mt-12 pt-8 border-t border-white/10 flex flex-col sm:flex-row justify-between items-center gap-4">
          <p className="text-sm text-white/40">
            © {currentYear} CineAesthete. All rights reserved.
          </p>
          <div className="flex items-center gap-6">
            <Link href="/terms" className="text-sm text-white/40 hover:text-text-primary transition-colors">
              Terms
            </Link>
            <Link href="/privacy" className="text-sm text-white/40 hover:text-text-primary transition-colors">
              Privacy
            </Link>
            <Link href="/cookies" className="text-sm text-white/40 hover:text-text-primary transition-colors">
              Cookies
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
