'use client';

import { MotionValue, motion, useMotionValue, useSpring, useTransform } from 'framer-motion';
import { useRef } from 'react';
import { Home, Search, Heart, User, Sparkles, Film } from 'lucide-react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import { Tooltip } from '@/components/ui/Tooltip';

export function Dock() {
    const mouseX = useMotionValue(Infinity);

    return (
        <motion.div
            onMouseMove={(e) => mouseX.set(e.pageX)}
            onMouseLeave={() => mouseX.set(Infinity)}
            className="fixed bottom-8 left-1/2 z-50 flex h-16 -translate-x-1/2 items-end gap-4 rounded-2xl border border-white/10 glass-heavy px-4 pb-3"
        >
            <DockItem mouseX={mouseX} href="/" icon={<Home className="h-full w-full" />} label="Home" />
            <DockItem mouseX={mouseX} href="/browse" icon={<Film className="h-full w-full" />} label="Browse" />
            <DockItem mouseX={mouseX} href="/aesthetic" icon={<Search className="h-full w-full" />} label="Search" />
            <DockItem mouseX={mouseX} href="/trending" icon={<Sparkles className="h-full w-full" />} label="Trending" />
            <DockItem mouseX={mouseX} href="/watchlist" icon={<Heart className="h-full w-full" />} label="Watchlist" />
            <DockItem mouseX={mouseX} href="/profile" icon={<User className="h-full w-full" />} label="Profile" />
        </motion.div>
    );
}

function DockItem({
    mouseX,
    icon,
    href,
    label,
}: {
    mouseX: MotionValue;
    icon: React.ReactNode;
    href: string;
    label: string;
}) {
    const ref = useRef<HTMLDivElement>(null);
    const pathname = usePathname();
    const isActive = pathname === href;

    const distance = useTransform(mouseX, (val) => {
        const bounds = ref.current?.getBoundingClientRect() ?? { x: 0, width: 0 };
        return val - bounds.x - bounds.width / 2;
    });

    const widthSync = useTransform(distance, [-150, 0, 150], [40, 80, 40]);
    const width = useSpring(widthSync, { mass: 0.1, stiffness: 150, damping: 12 });

    return (
        <Link href={href}>
            <Tooltip content={label}>
                <motion.div
                    ref={ref}
                    style={{ width }}
                    className={cn(
                        "aspect-square rounded-full flex items-center justify-center relative",
                        isActive ? "bg-white/10 border border-white/20" : "hover:bg-white/5"
                    )}
                >
                    <span className={cn(
                        "flex items-center justify-center p-2 transition-colors duration-200",
                        isActive ? "text-klein-blue" : "text-white/60 hover:text-white"
                    )}>
                        {icon}
                    </span>
                    {isActive && (
                        <motion.div
                            layoutId="activeDockDot"
                            className="absolute -bottom-2 h-1 w-1 rounded-full bg-klein-blue"
                        />
                    )}
                </motion.div>
            </Tooltip>
        </Link>
    );
}
