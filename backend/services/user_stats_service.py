from motor.motor_asyncio import AsyncIOMotorCollection
from datetime import datetime, timedelta
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class UserStatsService:
    """خدمة إحصائيات المستخدمين"""
    
    def __init__(self, db):
        self.db = db
        self.user_sessions_collection: AsyncIOMotorCollection = db.user_sessions
        self.daily_stats_collection: AsyncIOMotorCollection = db.daily_stats
        
    async def track_user_session(self, session_id: str, user_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """تتبع جلسة مستخدم جديدة"""
        try:
            session_data = {
                'session_id': session_id,
                'start_time': datetime.utcnow(),
                'last_activity': datetime.utcnow(),
                'messages_count': 0,
                'user_info': user_info or {},
                'status': 'active'
            }
            
            # حفظ أو تحديث الجلسة
            await self.user_sessions_collection.update_one(
                {'session_id': session_id},
                {'$setOnInsert': session_data},
                upsert=True
            )
            
            # تحديث الإحصائيات اليومية
            await self._update_daily_stats()
            
            return session_data
            
        except Exception as e:
            logger.error(f"خطأ في تتبع المستخدم: {e}")
            return {}
    
    async def update_user_activity(self, session_id: str):
        """تحديث نشاط المستخدم"""
        try:
            await self.user_sessions_collection.update_one(
                {'session_id': session_id},
                {
                    '$set': {'last_activity': datetime.utcnow()},
                    '$inc': {'messages_count': 1}
                }
            )
        except Exception as e:
            logger.error(f"خطأ في تحديث نشاط المستخدم: {e}")
    
    async def get_user_statistics(self) -> Dict[str, Any]:
        """الحصول على إحصائيات المستخدمين الشاملة"""
        try:
            now = datetime.utcnow()
            today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            week_start = today_start - timedelta(days=7)
            month_start = today_start - timedelta(days=30)
            
            # إجمالي المستخدمين
            total_users = await self.user_sessions_collection.count_documents({})
            
            # المستخدمون النشطون اليوم
            active_today = await self.user_sessions_collection.count_documents({
                'last_activity': {'$gte': today_start}
            })
            
            # المستخدمون النشطون هذا الأسبوع
            active_week = await self.user_sessions_collection.count_documents({
                'last_activity': {'$gte': week_start}
            })
            
            # المستخدمون النشطون هذا الشهر
            active_month = await self.user_sessions_collection.count_documents({
                'last_activity': {'$gte': month_start}
            })
            
            # إجمالي الرسائل
            pipeline = [
                {'$group': {'_id': None, 'total_messages': {'$sum': '$messages_count'}}}
            ]
            
            messages_result = await self.user_sessions_collection.aggregate(pipeline).to_list(1)
            total_messages = messages_result[0]['total_messages'] if messages_result else 0
            
            # متوسط الرسائل لكل مستخدم
            avg_messages = round(total_messages / total_users, 1) if total_users > 0 else 0
            
            return {
                'total_users': total_users,
                'active_today': active_today,
                'active_week': active_week, 
                'active_month': active_month,
                'total_messages': total_messages,
                'avg_messages_per_user': avg_messages,
                'last_updated': now.isoformat(),
                'growth_stats': await self._calculate_growth_stats()
            }
            
        except Exception as e:
            logger.error(f"خطأ في جلب إحصائيات المستخدمين: {e}")
            return {
                'total_users': 0,
                'active_today': 0,
                'active_week': 0,
                'active_month': 0,
                'total_messages': 0,
                'avg_messages_per_user': 0,
                'error': str(e)
            }
    
    async def _update_daily_stats(self):
        """تحديث الإحصائيات اليومية"""
        try:
            today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            
            stats = await self.get_user_statistics()
            
            daily_record = {
                'date': today,
                'total_users': stats['total_users'],
                'active_users': stats['active_today'],
                'total_messages': stats['total_messages'],
                'timestamp': datetime.utcnow()
            }
            
            await self.daily_stats_collection.update_one(
                {'date': today},
                {'$set': daily_record},
                upsert=True
            )
            
        except Exception as e:
            logger.error(f"خطأ في تحديث الإحصائيات اليومية: {e}")
    
    async def _calculate_growth_stats(self) -> Dict[str, Any]:
        """حساب إحصائيات النمو"""
        try:
            # آخر 7 أيام
            last_week = datetime.utcnow() - timedelta(days=7)
            
            recent_stats = await self.daily_stats_collection.find(
                {'date': {'$gte': last_week}}
            ).sort('date', 1).to_list(7)
            
            if len(recent_stats) >= 2:
                growth_rate = ((recent_stats[-1]['total_users'] - recent_stats[0]['total_users']) / 
                              max(recent_stats[0]['total_users'], 1)) * 100
                
                return {
                    'weekly_growth_rate': round(growth_rate, 1),
                    'daily_average_new_users': round(
                        (recent_stats[-1]['total_users'] - recent_stats[0]['total_users']) / 7, 1
                    ),
                    'peak_activity_day': max(recent_stats, key=lambda x: x['active_users'])['date'].strftime('%Y-%m-%d')
                }
            
            return {'weekly_growth_rate': 0, 'daily_average_new_users': 0, 'peak_activity_day': 'غير متوفر'}
            
        except Exception as e:
            logger.error(f"خطأ في حساب إحصائيات النمو: {e}")
            return {'error': str(e)}

# إنشاء مثيل الخدمة
user_stats_service = None  # سيتم تهيئته في الخادم الرئيسي