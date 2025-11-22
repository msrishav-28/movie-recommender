'use client';

import { useState, useEffect } from 'react';
import { Plus, List, Loader, Trash2 } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Checkbox } from '@/components/ui/Checkbox';
import { Modal } from '@/components/ui/Modal';
import { listService, UserList } from '@/services/list.service';
import { formatDate } from '@/lib/utils';
import { toast } from 'sonner';

export default function MyListsPage() {
  const [lists, setLists] = useState<UserList[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newListName, setNewListName] = useState('');
  const [newListDesc, setNewListDesc] = useState('');
  const [isPublic, setIsPublic] = useState(true);
  const [isCreating, setIsCreating] = useState(false);

  useEffect(() => {
    loadLists();
  }, []);

  const loadLists = async () => {
    try {
      setIsLoading(true);
      const data = await listService.getMyLists();
      setLists(data);
    } catch (error) {
      toast.error('Failed to load lists');
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreateList = async () => {
    if (!newListName.trim()) {
      toast.error('List name is required');
      return;
    }

    try {
      setIsCreating(true);
      await listService.createList({
        name: newListName,
        description: newListDesc || undefined,
        is_public: isPublic,
      });
      toast.success('List created!');
      setShowCreateModal(false);
      setNewListName('');
      setNewListDesc('');
      setIsPublic(true);
      loadLists();
    } catch (error) {
      toast.error('Failed to create list');
      console.error(error);
    } finally {
      setIsCreating(false);
    }
  };

  const handleDeleteList = async (listId: number) => {
    if (!confirm('Are you sure you want to delete this list?')) return;

    try {
      await listService.deleteList(listId);
      toast.success('List deleted');
      loadLists();
    } catch (error) {
      toast.error('Failed to delete list');
      console.error(error);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader className="h-8 w-8 animate-spin text-brand-primary" />
      </div>
    );
  }

  return (
    <div className="min-h-screen section-spacing">
      <div className="container-padding">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-4xl font-bold mb-2">My Lists</h1>
            <p className="text-text-secondary">
              Organize movies into custom lists
            </p>
          </div>
          <Button
            variant="primary"
            icon={<Plus className="h-5 w-5" />}
            onClick={() => setShowCreateModal(true)}
            glow
          >
            Create List
          </Button>
        </div>

        {/* Lists Grid */}
        {lists.length === 0 ? (
          <Card variant="glass">
            <CardContent className="p-12 text-center">
              <List className="h-16 w-16 text-text-tertiary mx-auto mb-4" />
              <h3 className="text-xl font-semibold mb-2">No lists yet</h3>
              <p className="text-text-secondary mb-6">
                Create your first list to start organizing movies
              </p>
              <Button
                variant="primary"
                icon={<Plus className="h-5 w-5" />}
                onClick={() => setShowCreateModal(true)}
              >
                Create Your First List
              </Button>
            </CardContent>
          </Card>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {lists.map((list) => (
              <Card key={list.id} variant="glass">
                <CardContent className="p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex-1">
                      <h3 className="text-xl font-bold mb-1">{list.name}</h3>
                      {list.description && (
                        <p className="text-sm text-text-tertiary">{list.description}</p>
                      )}
                    </div>
                    <Button
                      variant="ghost"
                      size="sm"
                      icon={<Trash2 className="h-4 w-4" />}
                      onClick={() => handleDeleteList(list.id)}
                    />
                  </div>

                  <div className="flex items-center justify-between text-sm text-text-secondary">
                    <span>{list.is_public ? 'Public' : 'Private'}</span>
                    <span>{formatDate(list.created_at, 'short')}</span>
                  </div>

                  {list.likes_count > 0 && (
                    <p className="text-sm text-brand-primary mt-2">
                      {list.likes_count} likes
                    </p>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {/* Create List Modal */}
        <Modal
          isOpen={showCreateModal}
          onClose={() => setShowCreateModal(false)}
          title="Create New List"
        >
          <div className="space-y-4">
            <Input
              label="List Name"
              placeholder="e.g., Favorite Thrillers"
              value={newListName}
              onChange={(e) => setNewListName(e.target.value)}
              required
            />

            <div>
              <label className="block text-sm font-medium mb-2">
                Description (Optional)
              </label>
              <textarea
                className="w-full px-4 py-3 bg-surface/50 border border-white/10 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-primary/50 text-text-primary placeholder-text-tertiary min-h-[100px] resize-y"
                placeholder="Describe your list..."
                value={newListDesc}
                onChange={(e) => setNewListDesc(e.target.value)}
              />
            </div>

            <Checkbox
              label="Make this list public"
              checked={isPublic}
              onChange={setIsPublic}
            />

            <div className="flex justify-end gap-3 pt-4">
              <Button
                variant="ghost"
                onClick={() => setShowCreateModal(false)}
                disabled={isCreating}
              >
                Cancel
              </Button>
              <Button
                variant="primary"
                onClick={handleCreateList}
                loading={isCreating}
              >
                Create List
              </Button>
            </div>
          </div>
        </Modal>
      </div>
    </div>
  );
}
