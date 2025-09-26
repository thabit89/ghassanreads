# نسخة مبسطة لخدمة الدردشة للنشر بدون قاعدة بيانات
import uuid
from datetime import datetime
from typing import Dict, Any

class SimpleChatService:
    """خدمة دردشة مبسطة للنشر بدون قاعدة بيانات"""
    
    def __init__(self):
        # ذاكرة مؤقتة للجلسات (ستفقد عند إعادة التشغيل)
        self.sessions = {}
        self.messages = {}
    
    async def create_new_session(self) -> str:
        """إنشاء جلسة جديدة"""
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            'created_at': datetime.utcnow(),
            'message_count': 0
        }
        self.messages[session_id] = []
        return session_id
    
    async def save_message(self, session_id: str, text: str, sender: str) -> Dict[str, Any]:
        """حفظ رسالة"""
        if session_id not in self.sessions:
            await self.create_new_session()
        
        message = {
            'id': str(uuid.uuid4()),
            'text': text,
            'sender': sender,
            'timestamp': datetime.utcnow(),
            'session_id': session_id
        }
        
        self.messages[session_id].append(message)
        self.sessions[session_id]['message_count'] += 1
        
        return message
    
    async def get_chat_history(self, session_id: str, limit: int = 50):
        """جلب تاريخ المحادثات"""
        if session_id not in self.messages:
            return []
        
        return self.messages[session_id][-limit:]
    
    def get_stats(self) -> Dict[str, Any]:
        """إحصائيات بسيطة"""
        total_sessions = len(self.sessions)
        total_messages = sum(session['message_count'] for session in self.sessions.values())
        
        return {
            'total_users': total_sessions,
            'active_today': total_sessions,
            'total_messages': total_messages,
            'active_week': total_sessions,
            'active_month': total_sessions
        }

# مثيل للاستخدام في النشر
simple_chat_service = SimpleChatService()