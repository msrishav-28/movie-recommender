'use client';

import { useState, type ReactNode } from 'react';
import { cn } from '@/lib/utils';

export interface Tab {
  id: string;
  label: string;
  icon?: ReactNode;
  content: ReactNode;
  disabled?: boolean;
}

export interface TabsProps {
  tabs: Tab[];
  defaultTab?: string;
  onChange?: (tabId: string) => void;
  variant?: 'default' | 'pills';
}

export function Tabs({ tabs, defaultTab, onChange, variant = 'default' }: TabsProps) {
  const [activeTab, setActiveTab] = useState(defaultTab || tabs[0]?.id);

  const handleTabChange = (tabId: string) => {
    setActiveTab(tabId);
    onChange?.(tabId);
  };

  const activeTabContent = tabs.find((tab) => tab.id === activeTab)?.content;

  return (
    <div className="w-full">
      {/* Tab List */}
      <div
        className={cn(
          'flex items-center gap-1',
          variant === 'default' && 'border-b border-border',
          variant === 'pills' && 'glass-light rounded-lg p-1'
        )}
      >
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => !tab.disabled && handleTabChange(tab.id)}
            disabled={tab.disabled}
            className={cn(
              'flex items-center gap-2 px-4 py-2.5 font-medium transition-all',
              'disabled:opacity-50 disabled:cursor-not-allowed',
              variant === 'default' && [
                'border-b-2 -mb-px',
                activeTab === tab.id
                  ? 'border-brand-primary text-brand-primary'
                  : 'border-transparent text-text-secondary hover:text-text-primary',
              ],
              variant === 'pills' && [
                'rounded-md',
                activeTab === tab.id
                  ? 'bg-brand-primary text-white shadow-md'
                  : 'text-text-secondary hover:bg-glass-medium',
              ]
            )}
          >
            {tab.icon}
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="mt-6 animate-fade-in">{activeTabContent}</div>
    </div>
  );
}
