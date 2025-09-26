import React, { useState, useEffect } from 'react';
import { Users, TrendingUp, MessageCircle, Calendar } from 'lucide-react';
import { Card, CardContent } from '../ui/card';

export const UserStatsCounter = () => {
  const [stats, setStats] = useState({
    total_users: 0,
    active_today: 0,
    total_messages: 0,
    loading: true
  });

  useEffect(() => {
    fetchStats();
    // تحديث الإحصائيات كل 30 ثانية
    const interval = setInterval(fetchStats, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchStats = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/stats/users`);
      if (response.ok) {
        const data = await response.json();
        setStats({
          total_users: data.total_users || 0,
          active_today: data.active_today || 0,
          total_messages: data.total_messages || 0,
          loading: false
        });
      }
    } catch (error) {
      console.error('خطأ في جلب الإحصائيات:', error);
      setStats(prev => ({ ...prev, loading: false }));
    }
  };

  if (stats.loading) {
    return (
      <div className="animate-pulse">
        <div className="h-20 bg-gray-200 rounded-lg"></div>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
      
      {/* إجمالي المستخدمين */}
      <Card className="bg-gradient-to-r from-blue-50 to-indigo-50 border-blue-200 hover:shadow-lg transition-all duration-200">
        <CardContent className="p-4">
          <div className="flex items-center justify-between">
            <div className="text-right">
              <p className="text-sm text-blue-600 font-medium">إجمالي المستخدمين</p>
              <p className="text-2xl font-bold text-blue-800">{stats.total_users.toLocaleString()}</p>
            </div>
            <div className="bg-blue-100 p-3 rounded-full">
              <Users className="h-6 w-6 text-blue-600" />
            </div>
          </div>
        </CardContent>
      </Card>

      {/* النشطون اليوم */}
      <Card className="bg-gradient-to-r from-green-50 to-emerald-50 border-green-200 hover:shadow-lg transition-all duration-200">
        <CardContent className="p-4">
          <div className="flex items-center justify-between">
            <div className="text-right">
              <p className="text-sm text-green-600 font-medium">نشطون اليوم</p>
              <p className="text-2xl font-bold text-green-800">{stats.active_today.toLocaleString()}</p>
            </div>
            <div className="bg-green-100 p-3 rounded-full">
              <TrendingUp className="h-6 w-6 text-green-600" />
            </div>
          </div>
        </CardContent>
      </Card>

      {/* إجمالي المحادثات */}
      <Card className="bg-gradient-to-r from-purple-50 to-pink-50 border-purple-200 hover:shadow-lg transition-all duration-200">
        <CardContent className="p-4">
          <div className="flex items-center justify-between">
            <div className="text-right">
              <p className="text-sm text-purple-600 font-medium">إجمالي الرسائل</p>
              <p className="text-2xl font-bold text-purple-800">{stats.total_messages.toLocaleString()}</p>
            </div>
            <div className="bg-purple-100 p-3 rounded-full">
              <MessageCircle className="h-6 w-6 text-purple-600" />
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};