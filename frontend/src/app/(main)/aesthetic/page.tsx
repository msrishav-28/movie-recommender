'use client';

import { useState } from 'react';
import { Search, Sparkles, Palette, Image as ImageIcon, Tag } from 'lucide-react';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { Tabs } from '@/components/ui/Tabs';
import { MasonryGrid } from '@/components/ui/MasonryGrid';
import { aestheticService } from '@/services/aesthetic.service';
import { useDebounce } from '@/hooks/useDebounce';
import { VISUAL_TAGS, MOOD_TAGS } from '@/config/constants';
import { useQuery } from '@tanstack/react-query';

const COLOR_PALETTE = [
  '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8',
  '#F7DC6F', '#BB8FCE', '#85C1E2', '#F8B195', '#C06C84',
  '#6C5CE7', '#00B894', '#FDCB6E', '#E17055', '#74B9FF',
];

export default function AestheticSearchPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedColors, setSelectedColors] = useState<string[]>([]);
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [uploadedImage, setUploadedImage] = useState<File | null>(null);
  const [activeTab, setActiveTab] = useState('query');

  const debouncedQuery = useDebounce(searchQuery, 500);

  // Search by natural language query
  const { data: queryResults, isLoading: queryLoading } = useQuery({
    queryKey: ['aesthetic-search', 'query', debouncedQuery],
    queryFn: () => aestheticService.searchByQuery(debouncedQuery),
    enabled: debouncedQuery.length > 2,
  });

  // Search by color palette
  const { data: colorResults, isLoading: colorLoading } = useQuery({
    queryKey: ['aesthetic-search', 'colors', selectedColors],
    queryFn: () => aestheticService.searchByColor(selectedColors),
    enabled: selectedColors.length > 0,
  });

  // Search by visual tags
  const { data: tagResults, isLoading: tagLoading } = useQuery({
    queryKey: ['aesthetic-search', 'tags', selectedTags],
    queryFn: () => aestheticService.searchByTags(selectedTags),
    enabled: selectedTags.length > 0,
  });

  // Trending searches
  const { data: trendingSearches } = useQuery({
    queryKey: ['aesthetic-search', 'trending'],
    queryFn: () => aestheticService.getTrendingSearches(),
  });

  const handleColorSelect = (color: string) => {
    setSelectedColors((prev) =>
      prev.includes(color) ? prev.filter((c) => c !== color) : [...prev, color]
    );
  };

  const handleTagSelect = (tag: string) => {
    setSelectedTags((prev) =>
      prev.includes(tag) ? prev.filter((t) => t !== tag) : [...prev, tag]
    );
  };

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setUploadedImage(file);
      // TODO: Implement image upload to backend
    }
  };

  const getResults = () => {
    if (activeTab === 'query' && queryResults) return queryResults;
    if (activeTab === 'colors' && colorResults) return colorResults;
    if (activeTab === 'tags' && tagResults) return tagResults;
    return [];
  };

  const isLoading = queryLoading || colorLoading || tagLoading;
  const results = getResults();

  return (
    <div className="min-h-screen bg-void">
      {/* Hero Section */}
      <section className="relative py-20 overflow-hidden">
        {/* Cinematic Background Elements */}
        <div className="absolute inset-0 bg-void/50 backdrop-blur-3xl z-0" />
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-4xl h-64 bg-klein-blue/20 blur-[100px] rounded-full opacity-50 pointer-events-none" />

        <div className="container-padding relative z-10">
          <div className="max-w-4xl mx-auto text-center space-y-8">
            <div className="inline-flex items-center gap-2 px-6 py-2 rounded-full border border-white/10 bg-white/5 backdrop-blur-md shadow-glow animate-fade-in">
              <Sparkles className="h-4 w-4 text-klein-blue" />
              <span className="text-sm font-medium font-mono text-klein-blue tracking-wide uppercase">AI-Powered Discovery</span>
            </div>

            <h1 className="text-5xl md:text-7xl font-bold font-headline leading-tight animate-in fade-in slide-in-from-bottom-4 duration-700 delay-100">
              Find Movies by <span className="text-transparent bg-clip-text bg-gradient-to-r from-klein-blue to-electric-teal">Visual Vibe</span>
            </h1>

            <p className="text-xl text-text-secondary font-light max-w-2xl mx-auto animate-in fade-in slide-in-from-bottom-4 duration-700 delay-200">
              Search for films using natural language, colors, or visual tags. Discover movies that match your aesthetic.
            </p>
          </div>
        </div>
      </section>

      {/* Search Interface */}
      <section className="section-spacing">
        <div className="container-padding">
          <Tabs
            tabs={[
              {
                id: 'query',
                label: 'Natural Language',
                icon: <Search className="h-5 w-5" />,
                content: (
                  <div className="space-y-6">
                    <Input
                      type="search"
                      placeholder="e.g., 'rain with neon lights', 'cozy autumn vibes', 'cyberpunk cityscape'..."
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      prefix={<Search className="h-5 w-5" />}
                      showClearButton
                      onClear={() => setSearchQuery('')}
                      className="text-lg"
                    />

                    {trendingSearches && trendingSearches.length > 0 && (
                      <div>
                        <p className="text-sm font-medium mb-3">Trending Searches:</p>
                        <div className="flex flex-wrap gap-2">
                          {trendingSearches.slice(0, 10).map((search: string, index: number) => (
                            <button
                              key={index}
                              onClick={() => setSearchQuery(search)}
                              className="px-4 py-2 rounded-full glass-light hover:glass-medium transition-all text-sm"
                            >
                              {search}
                            </button>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                ),
              },
              {
                id: 'colors',
                label: 'Color Palette',
                icon: <Palette className="h-5 w-5" />,
                content: (
                  <div className="space-y-6">
                    <div>
                      <p className="text-sm font-medium mb-3">Select colors that match your mood:</p>
                      <div className="grid grid-cols-5 sm:grid-cols-10 gap-3">
                        {COLOR_PALETTE.map((color) => (
                          <button
                            key={color}
                            onClick={() => handleColorSelect(color)}
                            className={`w-full aspect-square rounded-lg transition-all hover:scale-110 ${selectedColors.includes(color)
                              ? 'ring-4 ring-klein-blue ring-offset-2 ring-offset-background'
                              : ''
                              }`}
                            style={{ backgroundColor: color }}
                          />
                        ))}
                      </div>
                    </div>

                    {selectedColors.length > 0 && (
                      <div>
                        <p className="text-sm font-medium mb-3">Selected Colors:</p>
                        <div className="flex flex-wrap gap-2">
                          {selectedColors.map((color) => (
                            <div
                              key={color}
                              className="flex items-center gap-2 px-3 py-1.5 rounded-full glass-light"
                            >
                              <div
                                className="w-4 h-4 rounded-full"
                                style={{ backgroundColor: color }}
                              />
                              <button
                                onClick={() => handleColorSelect(color)}
                                className="text-xs hover:text-signal-red"
                              >
                                ×
                              </button>
                            </div>
                          ))}
                          <Button
                            size="sm"
                            variant="ghost"
                            onClick={() => setSelectedColors([])}
                          >
                            Clear All
                          </Button>
                        </div>
                      </div>
                    )}
                  </div>
                ),
              },
              {
                id: 'image',
                label: 'Reference Image',
                icon: <ImageIcon className="h-5 w-5" />,
                content: (
                  <div className="space-y-6">
                    <div className="border-2 border-dashed border-white/10 rounded-lg p-12 text-center hover:border-klein-blue transition-colors">
                      <input
                        type="file"
                        accept="image/*"
                        onChange={handleImageUpload}
                        className="hidden"
                        id="image-upload"
                      />
                      <label htmlFor="image-upload" className="cursor-pointer">
                        <ImageIcon className="h-12 w-12 mx-auto mb-4 text-white/40" />
                        <p className="text-lg font-medium mb-2">Upload a Reference Image</p>
                        <p className="text-sm text-text-secondary">
                          Upload a screenshot or image to find visually similar movies
                        </p>
                        <div className="mt-4 bg-klein-blue text-white hover:bg-klein-blue-hover active:bg-klein-blue-active shadow-md hover:shadow-lg h-10 px-6 text-base inline-flex items-center justify-center gap-2 rounded-md font-medium transition-all duration-200">
                          Choose Image
                        </div>
                      </label>
                    </div>

                    {uploadedImage && (
                      <div className="glass-medium rounded-lg p-4">
                        <p className="text-sm font-medium mb-2">Uploaded Image:</p>
                        <p className="text-sm text-text-secondary">{uploadedImage.name}</p>
                      </div>
                    )}
                  </div>
                ),
              },
              {
                id: 'tags',
                label: 'Visual Tags',
                icon: <Tag className="h-5 w-5" />,
                content: (
                  <div className="space-y-6">
                    <div>
                      <p className="text-sm font-medium mb-3">Select visual characteristics:</p>
                      <div className="flex flex-wrap gap-2">
                        {VISUAL_TAGS.map((tag) => (
                          <button
                            key={tag}
                            onClick={() => handleTagSelect(tag)}
                            className={`px-4 py-2 rounded-full transition-all ${selectedTags.includes(tag)
                              ? 'bg-klein-blue text-white'
                              : 'glass-light hover:glass-medium'
                              }`}
                          >
                            {tag}
                          </button>
                        ))}
                      </div>
                    </div>

                    <div>
                      <p className="text-sm font-medium mb-3">Select mood & atmosphere:</p>
                      <div className="flex flex-wrap gap-2">
                        {MOOD_TAGS.map((tag) => (
                          <button
                            key={tag}
                            onClick={() => handleTagSelect(tag)}
                            className={`px-4 py-2 rounded-full transition-all ${selectedTags.includes(tag)
                              ? 'bg-klein-blue text-white'
                              : 'glass-light hover:glass-medium'
                              }`}
                          >
                            {tag}
                          </button>
                        ))}
                      </div>
                    </div>

                    {selectedTags.length > 0 && (
                      <div className="flex items-center gap-2">
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => setSelectedTags([])}
                        >
                          Clear All Tags
                        </Button>
                        <span className="text-sm text-text-secondary">
                          {selectedTags.length} tag{selectedTags.length !== 1 ? 's' : ''} selected
                        </span>
                      </div>
                    )}
                  </div>
                ),
              },
            ]}
            defaultTab="query"
            onChange={setActiveTab}
            variant="pills"
          />
        </div>
      </section>

      {/* Results Section */}
      <section className="section-spacing bg-void-deep/50">
        <div className="container-padding">
          {results.length > 0 ? (
            <>
              <div className="mb-8">
                <h2 className="text-3xl font-bold mb-2">Results</h2>
                <p className="text-text-secondary">
                  Found {results.length} movies matching your aesthetic
                </p>
              </div>
              <MasonryGrid items={results} />
            </>
          ) : !isLoading && (
            <div className="text-center py-20">
              <Sparkles className="h-16 w-16 mx-auto mb-4 text-white/40" />
              <h3 className="text-2xl font-bold mb-2">Start Your Aesthetic Search</h3>
              <p className="text-text-secondary">
                Use any of the search methods above to discover movies by their visual style
              </p>
            </div>
          )}
        </div>
      </section>
    </div>
  );
}
