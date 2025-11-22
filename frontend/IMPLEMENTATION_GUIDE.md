# CineAesthete Frontend - Complete Implementation Guide

> **Comprehensive guide for building the complete production-ready frontend**

---

## 📋 Project Status

### ✅ COMPLETED (Foundation Layer)

#### 1. Project Configuration
- [x] `package.json` - All dependencies configured
- [x] `tsconfig.json` - TypeScript with strict mode + path aliases
- [x] `next.config.js` - Next.js 14 with image optimization
- [x] `tailwind.config.ts` - Complete design system tokens
- [x] `postcss.config.js` - Tailwind + Autoprefixer
- [x] `.eslintrc.json` - ESLint with TypeScript rules
- [x] `.prettierrc` - Code formatting configuration
- [x] `.env.example` - Environment variables template
- [x] `.gitignore` - Git ignore patterns

#### 2. Core Infrastructure
- [x] `src/app/layout.tsx` - Root layout with fonts & providers
- [x] `src/app/globals.css` - Global styles + Tailwind layers
- [x] `src/types/index.ts` - Complete TypeScript type definitions
- [x] `src/config/constants.ts` - App constants & configuration
- [x] `src/lib/utils.ts` - Utility functions (50+ helpers)

#### 3. API Integration Layer
- [x] `src/services/api.client.ts` - Axios client with interceptors
- [x] `src/services/auth.service.ts` - Authentication service
- [x] `src/services/movie.service.ts` - Movie CRUD operations
- [x] `src/services/recommendation.service.ts` - Recommendations API
- [x] `src/services/aesthetic.service.ts` - Aesthetic search API

#### 4. Documentation
- [x] `README.md` - Comprehensive setup & usage guide
- [x] `IMPLEMENTATION_GUIDE.md` - This file

---

## 🚧 TO BE IMPLEMENTED

### Phase 1: State Management & Providers (Priority: HIGH)

#### 1.1 Zustand Stores
```
src/store/
├── authStore.ts          # User authentication state
├── uiStore.ts            # UI state (modals, sidebar, theme)
├── movieStore.ts         # Movie data cache
└── searchStore.ts        # Search history & filters
```

**authStore.ts** - User authentication
```typescript
interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
}
```

**uiStore.ts** - UI state
```typescript
interface UIState {
  theme: 'light' | 'dark' | 'system';
  sidebarOpen: boolean;
  modalStack: string[];
  setTheme: (theme: ThemeMode) => void;
  toggleSidebar: () => void;
  openModal: (id: string) => void;
  closeModal: () => void;
}
```

#### 1.2 React Query Setup
```
src/components/providers.tsx  # Wrap app with all providers
```

**Required Providers**:
- `QueryClientProvider` - React Query
- `ThemeProvider` - next-themes
- `AuthProvider` - Custom auth context
- `ToastProvider` - Sonner

---

### Phase 2: UI Component Library (Priority: HIGH)

Build all components from frontend plan spec:

#### 2.1 Base Components (`src/components/ui/`)

**Button.tsx** - 9 variants, 5 sizes
```typescript
variants: primary | secondary | tertiary | ghost | glass | outline | text | gradient | danger
sizes: xs | sm | md | lg | xl
features: icon support, loading state, ripple effect, glow effect
```

**Input.tsx** - Complete form input
```typescript
types: text | email | password | search | number
features: label, helper text, error state, prefix/suffix icons, character counter
```

**Card.tsx** - Container component
```typescript
variants: default | glass | elevated
features: header, footer, hover effects, loading state
```

**Modal.tsx** - Dialog system
```typescript
types: center | fullscreen | drawer | bottom-sheet
features: backdrop, animation, focus trap, scroll lock
```

**Dropdown.tsx** - Select component
```typescript
features: single/multi-select, search, virtualized, keyboard navigation
```

**Tooltip.tsx** - Hover information
```typescript
positions: top | bottom | left | right | auto
triggers: hover | focus | click
```

**Toast** - Already using Sonner ✅

#### 2.2 Movie Components (`src/components/movie/`)

**MovieCard.tsx** - THE MOST IMPORTANT COMPONENT
```typescript
Features:
- 2:3 aspect ratio poster
- 3D tilt effect on hover (perspective: 1000px, rotate ±7deg)
- Glassmorphic overlay with quick actions
- Match score badge (for aesthetic search)
- Genre chips (max 2)
- Rating display with star icon
- Responsive sizes: large (280px) | medium (220px) | small (160px)
- Entrance animation (staggered fade-in-up)
- Loading skeleton variant
```

**MovieDetail.tsx** - Full movie information panel
```typescript
Sections:
- Hero section with backdrop parallax
- Poster with 3D float animation
- Info panel (title, tagline, metadata)
- Overall + multi-dimensional ratings
- Action buttons row
- Sentiment analysis dashboard
- Synopsis with expand/collapse
- Aesthetic frames gallery
- Cast & crew carousel
- Videos (trailers/teasers)
- Reviews section
- Similar movies
- Technical details accordion
```

**MovieGrid.tsx** - Responsive grid layout
```typescript
Columns by breakpoint:
- 3xl (1920px+): 6 columns
- xl (1280px+): 5 columns
- lg (1024px): 4 columns
- md (768px): 3 columns
- sm (640px): 2 columns
Gap: 24px
```

**MovieCarousel.tsx** - Horizontal scroll
```typescript
Features:
- Momentum physics (friction: 0.92)
- Snap to center
- Gradient fade edges (120px width)
- Arrow navigation
- Touch/swipe support
```

#### 2.3 Layout Components (`src/components/layout/`)

**Header.tsx** - Navigation bar
```typescript
Elements:
- Logo (left)
- Search bar (center, expandable)
- Navigation links
- User menu (right)
- Mobile: Hamburger menu
Features:
- Sticky on scroll
- Glass effect
- Backdrop blur
- Search suggestions dropdown
```

**Footer.tsx** - Site footer
```typescript
Sections:
- Logo & tagline
- Quick links (4 columns)
- Social media icons
- Copyright & legal links
```

**Sidebar.tsx** - Filter sidebar (optional)
```typescript
Used in:
- Browse page
- Search results
Features:
- Collapsible sections
- Mobile: drawer modal
```

#### 2.4 Search Components (`src/components/search/`)

**AestheticSearchBar.tsx** - Main search interface
```typescript
Features:
- Large glass container (800px wide)
- AI indicator icon with pulse
- Example query bubbles (floating animation)
- Voice search support (optional)
- Search history dropdown
```

**SearchFilters.tsx** - Advanced filtering
```typescript
Filters:
- Genre (multi-select chips)
- Year range (dual-handle slider)
- Rating (minimum stars)
- Runtime (range slider)
- Language (dropdown)
- Streaming services (checkbox grid)
- Mood tags (chips)
```

---

### Phase 3: Pages & Routes (Priority: HIGH)

#### 3.1 App Router Structure
```
src/app/
├── layout.tsx                      # ✅ Root layout (DONE)
├── page.tsx                        # Homepage
├── globals.css                     # ✅ Global styles (DONE)
│
├── (auth)/                         # Auth routes group
│   ├── layout.tsx                  # Auth layout (no header/footer)
│   ├── login/
│   │   └── page.tsx               # Login page
│   ├── register/
│   │   └── page.tsx               # Register page
│   └── forgot-password/
│       └── page.tsx               # Password reset
│
├── (main)/                         # Main app routes
│   ├── browse/
│   │   └── page.tsx               # Browse/Explore page
│   ├── search/
│   │   └── page.tsx               # Search results
│   ├── aesthetic/
│   │   └── page.tsx               # Aesthetic search
│   ├── movie/
│   │   └── [id]/
│   │       └── page.tsx           # Movie detail page
│   ├── dashboard/
│   │   └── page.tsx               # User dashboard
│   ├── profile/
│   │   └── [username]/
│   │       └── page.tsx           # User profile
│   ├── watchlist/
│   │   └── page.tsx               # Watchlist page
│   └── settings/
│       └── page.tsx               # Settings page
│
└── not-found.tsx                   # 404 page
```

#### 3.2 Homepage (`src/app/page.tsx`)

**Required Sections**:
1. **Hero Section** (full viewport height)
   - Parallax background (3 layers)
   - Featured movie backdrop
   - Gradient overlays
   - Title with cinematic font
   - Action buttons (Watch Trailer, Add to Watchlist)
   - Scroll indicator (bouncing chevron)

2. **Value Proposition** (3-column grid)
   - Feature cards with icons
   - Animated on scroll (stagger)
   - Hover lift effect

3. **Aesthetic Search Showcase**
   - Gradient mesh background
   - Large search bar (800px)
   - Floating example bubbles (15-20)
   - "Describe your perfect movie vibe" heading

4. **Trending Movies** (horizontal carousel)
   - MovieCard components
   - Momentum scroll
   - Gradient fade edges

5. **How It Works** (3-step timeline)
   - Numbered badges
   - Icons
   - Connector lines with animation

6. **Social Proof** (statistics + testimonials)
   - Count-up animations
   - Testimonial carousel

7. **Final CTA**
   - Primary gradient background
   - Large heading
   - CTA button
   - Trust badges

#### 3.3 Browse Page (`src/app/(main)/browse/page.tsx`)

**Layout**: Filter sidebar + Movie grid

**Features**:
- Server-side filtering with URL params
- Infinite scroll (load more on scroll)
- Sort options dropdown
- View toggle (grid/list)
- Active filter chips
- Empty state handling

#### 3.4 Movie Detail Page (`src/app/(main)/movie/[id]/page.tsx`)

**Fetch Movie Data**:
```typescript
// Server component - fetch on server
async function MovieDetailPage({ params }: { params: { id: string } }) {
  const movie = await movieService.getMovieById(Number(params.id));
  
  return (
    <>
      <MovieHeroSection movie={movie} />
      <MovieDetailContent movie={movie} />
    </>
  );
}
```

**Sections** (from frontend plan):
- Hero with backdrop parallax
- Information panel
- Sentiment analysis dashboard
- Synopsis
- Aesthetic frames gallery
- Cast & crew
- Videos
- Reviews
- Similar movies
- Technical details
- Floating action bar (sticky)

#### 3.5 Aesthetic Search Page (`src/app/(main)/aesthetic/page.tsx`)

**Features**:
- Large search interface
- Example queries
- Visual tag selection
- Color palette picker
- Image upload for reference
- Results grid with match scores

---

### Phase 4: Custom Hooks (Priority: MEDIUM)

#### 4.1 Authentication Hooks
```typescript
// src/hooks/useAuth.ts
export function useAuth() {
  const login = async (email: string, password: string) => { ... }
  const logout = async () => { ... }
  const register = async (data: RegisterData) => { ... }
  
  return { user, isAuthenticated, login, logout, register, isLoading }
}
```

#### 4.2 Data Fetching Hooks
```typescript
// src/hooks/useMovies.ts
export function useMovies(filters: SearchFilters) {
  return useQuery({
    queryKey: ['movies', filters],
    queryFn: () => movieService.searchMovies(filters),
  });
}

// src/hooks/useInfiniteMovies.ts
export function useInfiniteMovies(filters: SearchFilters) {
  return useInfiniteQuery({
    queryKey: ['movies', 'infinite', filters],
    queryFn: ({ pageParam = 1 }) => 
      movieService.searchMovies(filters, pageParam),
    getNextPageParam: (lastPage) => lastPage.page + 1,
  });
}

// src/hooks/useMovie.ts
export function useMovie(id: number) {
  return useQuery({
    queryKey: ['movie', id],
    queryFn: () => movieService.getMovieById(id),
  });
}

// src/hooks/useRecommendations.ts
export function useRecommendations() {
  return useQuery({
    queryKey: ['recommendations'],
    queryFn: () => recommendationService.getRecommendations(),
  });
}
```

#### 4.3 UI Hooks
```typescript
// src/hooks/useInfiniteScroll.ts
export function useInfiniteScroll(callback: () => void) {
  // Intersection Observer implementation
}

// src/hooks/useMediaQuery.ts
export function useMediaQuery(query: string): boolean {
  // Match media query
}

// src/hooks/useDebounce.ts
export function useDebounce<T>(value: T, delay: number): T {
  // Debounce value changes
}

// src/hooks/useLocalStorage.ts
export function useLocalStorage<T>(key: string, initialValue: T) {
  // Sync state with localStorage
}

// src/hooks/useOnScreen.ts
export function useOnScreen(ref: RefObject<Element>): boolean {
  // Check if element is visible
}
```

---

### Phase 5: Additional Services (Priority: MEDIUM)

#### 5.1 Remaining Service Files
```
src/services/
├── api.client.ts            # ✅ DONE
├── auth.service.ts          # ✅ DONE
├── movie.service.ts         # ✅ DONE
├── recommendation.service.ts # ✅ DONE
├── aesthetic.service.ts     # ✅ DONE
├── user.service.ts          # TODO
├── rating.service.ts        # TODO
├── review.service.ts        # TODO
├── watchlist.service.ts     # TODO
└── social.service.ts        # TODO (if social features enabled)
```

#### 5.2 User Service
```typescript
// src/services/user.service.ts
export const userService = {
  getProfile: (username: string) => Promise<UserProfile>
  updateProfile: (data: Partial<User>) => Promise<User>
  updatePreferences: (prefs: UserPreferences) => Promise<void>
  uploadAvatar: (file: File) => Promise<string>
  getFollowers: (userId: string) => Promise<User[]>
  getFollowing: (userId: string) => Promise<User[]>
  followUser: (userId: string) => Promise<void>
  unfollowUser: (userId: string) => Promise<void>
}
```

#### 5.3 Rating & Review Service
```typescript
// src/services/rating.service.ts
export const ratingService = {
  rateMovie: (movieId: number, ratings: RatingData) => Promise<Rating>
  updateRating: (ratingId: string, ratings: RatingData) => Promise<Rating>
  deleteRating: (ratingId: string) => Promise<void>
  getUserRating: (movieId: number) => Promise<Rating | null>
}

// src/services/review.service.ts
export const reviewService = {
  getMovieReviews: (movieId: number, page: number) => Promise<PaginatedResponse<Review>>
  createReview: (movieId: number, content: string, rating: Rating) => Promise<Review>
  updateReview: (reviewId: string, content: string) => Promise<Review>
  deleteReview: (reviewId: string) => Promise<void>
  likeReview: (reviewId: string) => Promise<void>
  unlikeReview: (reviewId: string) => Promise<void>
}
```

#### 5.4 Watchlist Service
```typescript
// src/services/watchlist.service.ts
export const watchlistService = {
  getWatchlist: () => Promise<WatchlistItem[]>
  addToWatchlist: (movieId: number, priority: Priority) => Promise<WatchlistItem>
  removeFromWatchlist: (itemId: string) => Promise<void>
  updatePriority: (itemId: string, priority: Priority) => Promise<WatchlistItem>
  checkInWatchlist: (movieId: number) => Promise<boolean>
}
```

---

### Phase 6: Animations & Interactions (Priority: MEDIUM)

#### 6.1 Framer Motion Integration

**Page Transitions**:
```typescript
// src/components/PageTransition.tsx
export function PageTransition({ children }: { children: ReactNode }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.3 }}
    >
      {children}
    </motion.div>
  );
}
```

**Scroll Animations**:
```typescript
// src/components/ScrollReveal.tsx
export function ScrollReveal({ children, delay = 0 }: Props) {
  const controls = useAnimation();
  const [ref, inView] = useInView({ threshold: 0.2, triggerOnce: true });
  
  useEffect(() => {
    if (inView) {
      controls.start({ opacity: 1, y: 0 });
    }
  }, [controls, inView]);
  
  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 20 }}
      animate={controls}
      transition={{ duration: 0.4, delay }}
    >
      {children}
    </motion.div>
  );
}
```

**3D Tilt Effect** (for MovieCard):
```typescript
// src/hooks/useTilt.ts
export function useTilt(ref: RefObject<HTMLElement>) {
  const handleMouseMove = (e: MouseEvent) => {
    const rect = ref.current?.getBoundingClientRect();
    const x = (e.clientY - rect.top) / rect.height - 0.5;
    const y = (e.clientX - rect.left) / rect.width - 0.5;
    
    ref.current.style.transform = `
      perspective(1000px) 
      rotateX(${x * -7}deg) 
      rotateY(${y * 7}deg)
    `;
  };
  
  // ... add/remove event listeners
}
```

---

### Phase 7: Testing (Priority: LOW)

#### 7.1 Unit Tests (Jest + React Testing Library)
```
src/__tests__/
├── components/
│   ├── Button.test.tsx
│   ├── MovieCard.test.tsx
│   └── ...
├── hooks/
│   ├── useAuth.test.ts
│   └── ...
└── services/
    ├── auth.service.test.ts
    └── ...
```

#### 7.2 E2E Tests (Playwright)
```
e2e/
├── auth.spec.ts          # Login/register flows
├── movie-browse.spec.ts  # Browse & search
├── movie-detail.spec.ts  # Movie detail page
└── watchlist.spec.ts     # Watchlist operations
```

---

## 🚀 Implementation Order

### Week 1: Foundation (CRITICAL)
1. ✅ Project setup (DONE)
2. State management stores (authStore, uiStore)
3. Providers component
4. Base UI components (Button, Input, Card)
5. Header & Footer layout components

### Week 2: Core Features
6. Homepage with all sections
7. MovieCard component (MOST IMPORTANT)
8. Movie detail page
9. Browse/Search page
10. Authentication pages (login/register)

### Week 3: Advanced Features
11. Aesthetic search page
12. User dashboard
13. Watchlist page
14. Rating & review system
15. Remaining service integrations

### Week 4: Polish & Optimization
16. Animations & transitions
17. Error boundaries
18. Loading states & skeletons
19. Accessibility audit & fixes
20. Performance optimization
21. Responsive design refinement

---

## 📦 Installation Steps

```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install all dependencies (this will fix ALL TypeScript errors)
npm install

# 3. Create .env file
cp .env.example .env

# 4. Update .env with backend URL
# NEXT_PUBLIC_API_URL=http://localhost:8000

# 5. Verify installation
npm run type-check

# 6. Start development server
npm run dev

# Server will start on http://localhost:3000
```

---

## 🎯 Quick Wins (Get Something Running Fast)

### Minimum Viable Frontend (1-2 days)

**Goal**: Get a basic working app to see data from backend

1. **Install dependencies**: `npm install`
2. **Create simple Homepage**: Just show logo + "Coming soon"
3. **Create MovieCard**: Basic version without 3D effects
4. **Create Browse page**: Fetch & display movies in grid
5. **Add basic routing**: Homepage → Browse

**Files needed**:
- `src/app/page.tsx` - Simple homepage
- `src/components/movie/MovieCard.tsx` - Basic card
- `src/app/(main)/browse/page.tsx` - Movie grid
- `src/store/authStore.ts` - Basic auth state

This will let you see movies from the backend immediately!

---

## 📚 Key Dependencies to Learn

1. **Next.js 14** - App Router, Server Components
2. **React Query** - Data fetching & caching
3. **Zustand** - Simple state management
4. **Framer Motion** - Animations
5. **Radix UI** - Accessible components
6. **React Hook Form** - Forms
7. **Tailwind CSS** - Styling

---

## 🐛 Expected Issues & Solutions

### Issue: TypeScript errors everywhere
**Solution**: Run `npm install` - all errors will disappear

### Issue: Module not found errors
**Solution**: Check tsconfig.json paths are correct, restart TS server

### Issue: Tailwind classes not working
**Solution**: Ensure content paths in tailwind.config.ts include all files

### Issue: Can't connect to backend
**Solution**: Ensure backend running on port 8000, check CORS settings

### Issue: Images not loading
**Solution**: Check TMDb image URL configuration in .env

---

## 📞 Need Help?

1. Check the comprehensive [README.md](./README.md)
2. Review backend [API documentation](../backend/README.md)
3. Check [frontend plan](../frontend%20plan.md) for design specs
4. TypeScript errors? Run `npm install` first!

---

## ✅ Definition of Done

Before considering the frontend "complete", ensure:

- [ ] All pages render correctly
- [ ] Authentication flow works end-to-end
- [ ] Movies display from backend API
- [ ] Search & filtering functional
- [ ] Aesthetic search integrated
- [ ] Responsive on mobile/tablet/desktop
- [ ] All animations smooth (60fps+)
- [ ] Accessibility: keyboard navigation works
- [ ] Loading states for all async operations
- [ ] Error handling for API failures
- [ ] SEO meta tags on all pages
- [ ] Performance: Lighthouse score > 90
- [ ] No console errors in production build

---

**Ready to build? Start with `npm install` then follow Week 1 tasks!** 🚀

---

**Version**: 1.0.0  
**Last Updated**: November 16, 2025  
**Author**: CineAesthete Team
