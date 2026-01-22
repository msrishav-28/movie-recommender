'use client';

import { User, Lock, Bell } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Toggle } from '@/components/ui/Toggle';
import { Tabs } from '@/components/ui/Tabs';
import { useAuth } from '@/hooks/useAuth';

export default function SettingsPage() {
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-void">
      <section className="bg-void/80 border-b border-white/5 backdrop-blur-md sticky top-[64px] z-30 shadow-lg">
        <div className="container-padding py-6">
          <h1 className="text-3xl md:text-4xl font-bold mb-2 font-headline leading-none">Settings</h1>
          <p className="text-text-secondary font-mono text-sm">Manage your account and preferences</p>
        </div>
      </section>

      <section className="section-spacing">
        <div className="container-padding max-w-4xl mx-auto">

          <Tabs
            tabs={[
              {
                id: 'account',
                label: 'Account',
                icon: <User className="h-5 w-5" />,
                content: (
                  <Card variant="glass">
                    <CardHeader>
                      <CardTitle>Profile Information</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      <Input label="Username" value={user?.username} />
                      <Input label="Email" value={user?.email} />
                      <Button variant="primary">Save Changes</Button>
                    </CardContent>
                  </Card>
                ),
              },
              {
                id: 'password',
                label: 'Password',
                icon: <Lock className="h-5 w-5" />,
                content: (
                  <Card variant="glass">
                    <CardHeader>
                      <CardTitle>Change Password</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      <Input label="Current Password" type="password" />
                      <Input label="New Password" type="password" />
                      <Button variant="primary">Update Password</Button>
                    </CardContent>
                  </Card>
                ),
              },
              {
                id: 'notifications',
                label: 'Notifications',
                icon: <Bell className="h-5 w-5" />,
                content: (
                  <Card variant="glass">
                    <CardContent className="space-y-4 pt-6">
                      <Toggle label="Email Notifications" checked={true} />
                      <Toggle label="Push Notifications" checked={false} />
                      <Toggle label="Weekly Digest" checked={true} />
                    </CardContent>
                  </Card>
                ),
              },
            ]}
            variant="pills"
          />
        </div>
      </section>
    </div>
  );
}
