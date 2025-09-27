import os
from typing import List, Dict, Any, Optional
# from emergentintegrations.llm.chat import LimChat, UserMessage # مُعطَّل بسبب الملفات المفقودة
from dotenv import load_dotenv
import logging
import uuid

# تحميل متغيرات البيئة
load_dotenv()

logger = logging.getLogger(__name__)

class GhassanLLMService:
    def __init__(self):
        # استخدام مفتاح Claude الخاص للتحليل الأدبي المتقدم
        self.anthropic_key = os.environ.get('ANTHROPIC_API_KEY')
        self.emergent_key = os.environ.get('EMERGENT_LLM_KEY')
        
        if not self.anthropic_key:
            logger.warning("ANTHROPIC_API_KEY not found, using EMERGENT_LLM_KEY")
        if not self.emergent_key:
            raise ValueError("EMERGENT_LLM_KEY not found in environment variables")
        
        # رسالة النظام المحدثة - غسان المبادر والمساعد الفعال
        self.system_message = """أنت غسان، المساعد الأدبي العُماني المبادر والمفيد.

🌟 **شخصيتك المبادرة:**
• مساعد استباقي يقترح الحلول والأفكار قبل أن يُطلب منك
• مبدع في تصميم الجداول المقارنة والخطط التعليمية
• متحمس لمساعدة الطلاب في مشاريعهم الأدبية
• محفز للقراءة والمذاكرة بطرق إبداعية ومشوقة
• لطيف ومهذب في التعامل مع جميع الأعمار

💡 **أساليبك المبادرة:**
• "يمكنني عمل جدول مقارنة لك بين..." 
• "دعني أقترح عليك خطة دراسية لـ..."
• "ما رأيك أن نصمم مشروع حول...؟"
• "لدي فكرة مبتكرة قد تساعدك..."
• "هل تريد أن أقترح كتب للقراءة عن...؟"

🎓 **مساعدتك التعليمية الشاملة:**
• صمم جداول مقارنة للكتاب والأعمال
• اقترح مشاريع إبداعية متعلقة بالأدب العُماني
• ضع خطط قراءة مخصصة لكل مرحلة دراسية
• اقترح طرق مذاكرة فعالة ومتنوعة
• ابتكر أنشطة تفاعلية للتعلم

🚨 **مع الحفاظ على الدقة المطلقة:**
• لا تختلق معلومات مطلقاً
• استخدم فقط المعلومات المؤكدة من المصادر
• اعترف بعدم المعرفة عند الحاجة
• قدم البدائل والاقتراحات العملية

💬 **أسلوبك المتوازن:**
• متحمس ومشجع دون مبالغة
• مبادر ومفيد دون تطفل
• مهذب ولطيف مع الجميع
• محترم لجميع الأعمار والمراحل

تذكر: أنت مساعد مبادر ومبدع، لكن دقيق وصادق!"""

    async def generate_response_with_search(
        self, 
        user_message: str, 
        search_results: List[Dict[str, Any]] = None,
        session_id: str = None,
        use_claude: bool = False,
        conversation_context: str = ""
    ) -> Dict[str, Any]:
        """توليد رد مع نتائج البحث (تم تعطيله مؤقتاً بسبب ملفات الدردشة المفقودة)"""
        
        # 🚨🚨🚨 كود الدردشة مُعطَّل مؤقتاً لضمان نجاح النشر 🚨🚨🚨

        # تعويض آمن لضمان أن الوظيفة ترجع قيمة صالحة دون الاعتماد على كود الدردشة المفقود
        
        # إنشاء session_id إذا لم يكن موجوداً
        if not session_id:
            session_id = str(uuid.uuid4())
            
        # إضافة التعويض النهائي (سيعمل هذا الآن لأنه خارج try/except ومع مسافة بادئة صحيحة)
        return {
            'text': 'عذراً، وظيفة الدردشة مُعطَّلة مؤقتاً. يرجى استعادة ملفات الكود المصدر المفقودة (مثل LimChat) لإعادة تفعيلها.',
            'session_id': session_id,
            'model_used': 'disabled_placeholder',
            'has_search_results': False,
            'search_results_count': 0,
            'error': 'Missing core chat functionality'
        }

        # 🚨🚨🚨 هنا كان يوجد كود الدردشة و try/except الذي تم تعطيله 🚨🚨🚨
        
    def _prepare_message_with_search(
        self, 
        user_message: str, 
        search_results: List[Dict[str, Any]] = None
    ) -> str:
        """إعداد الرسالة مع دمج نتائج البحث والتحقق من الموثوقية"""
        if not search_results:
            return user_message + "\n\n" + self._add_analytical_framework(user_message)
        
        # تجهيز المعلومات من البحث مع تقييم الموثوقية
        search_context = "\n--- معلومات من مصادر موثوقة ---\n"
        
        for i, result in enumerate(search_results, 1):
            reliability_note = ""
            if result.get('reliability_warning'):
                reliability_note = f" (تنبيه: {result['reliability_warning']})"
            
            search_context += f"""
{i}. {result.get('title', 'بلا عنوان')}{reliability_note}
المصدر: {result.get('source', 'غير محدد')} - نوع: {result.get('type', 'عام')}
المحتوى: {result.get('content', '')[:200]}...
درجة الموثوقية: {result.get('final_score', 0.5):.1f}/1.0
"""
        
        search_context += "\n--- نهاية المعلومات ---\n"
        
        # إضافة التوجيهات النقدية والنحوية
        analytical_framework = self._add_analytical_framework(user_message)
        
        # دمج الرسالة مع السياق
        enhanced_message = f"""السؤال: {user_message}

{search_context}

{analytical_framework}

تعليمات مهمة:
- استخدم هذه المعلومات بحذر شديد
- **لا تذكر أي عناوين كتب محددة من نتائج البحث إلا إذا كانت من مصادر موثوقة 100%**
- إذا تضاربت المصادر أو كانت غير مؤكدة، اعترف بذلك صراحة  
- **قل "لا أملك معلومات مؤكدة عن مؤلفاته المحددة" بدلاً من ذكر عناوين مشكوك فيها**
- ركز على التحليل الأدبي والنحوي العميق
- استخدم النظريات النقدية المناسبة
- اعتمد على الحقائق المؤكدة فقط

🚨 **تحذير نهائي:** إذا لم تكن متأكداً من عنوان كتاب أو تاريخ أو معلومة محددة، لا تذكرها أبداً. قل "أحتاج للتحقق من مصادر إضافية" """
        
        return enhanced_message
    
    def _add_conversation_context(self, message: str, conversation_context: str) -> str:
        """إضافة سياق المحادثة للرسالة"""
        if not conversation_context:
            return message
        
        return f"{conversation_context}\n\nالسؤال الحالي: {message}"
    
    def _add_educational_context(self, message: str, curriculum_context: str) -> str:
        """إضافة السياق التعليمي للرسالة"""
        if not curriculum_context:
            return message
        
        return f"{message}\n\n{curriculum_context}"
    
    def _add_analytical_framework(self, user_message: str) -> str:
        """إضافة إطار تحليلي بسيط وآمن"""
        
        # تحليل بسيط ومباشر فقط
        if any(word in user_message for word in ['تحليل', 'نقد', 'إعراب']):
            return """
📝 **إطار تحليلي بسيط:**
• حلل النص المُعطى فقط (لا تختلق نصوص)
• استخدم المصطلحات النحوية والبلاغية الصحيحة
• اذكر فقط ما هو واضح في النص
• لا تفترض معلومات غير مذكورة
"""
        
        elif any(word in user_message for word in ['أعرب', 'نحو', 'إعراب']):
            return """
✏️ **تحليل نحوي مطلوب:**
• أعرب الكلمات الموجودة في النص فقط
• اشرح القواعد النحوية بدقة
• لا تضيف أمثلة من عندك
• التزم بالنص المُعطى فقط
"""
        
        return ""  # لا إضافات معقدة
    
    def _should_use_claude(self, user_message: str) -> bool:
        """تحديد متى نستخدم Claude بدلاً من GPT للحصول على تحليل أكثر دقة"""
        # استخدم Claude للتحليل الإبداعي والنقدي والنحوي
        claude_keywords = [
            'تحليل', 'نقد', 'إبداع', 'شاعرية', 'جمالية', 
            'أسلوب', 'بلاغة', 'صورة شعرية', 'رمزية',
            'نحو', 'إعراب', 'قواعد', 'بنية', 'تركيب',
            'نظرية', 'منهج', 'مدرسة أدبية', 'تيار'
        ]
        
        return any(keyword in user_message for keyword in claude_keywords)
    
    def _add_advanced_instructions(self, message: str) -> str:
        """إضافة تعليمات الدقة الصارمة مع السياق التعليمي"""
        safe_instructions = """
        
🚨 **تعليمات الدقة المطلقة:**

❌ **لا تفعل هذا أبداً:**
- لا تختلق أو تتخيل أي معلومات
- لا تقل "يبدو أن" أو "ربما" أو "أعتقد"  
- لا تذكر عناوين كتب لم تُذكر في المصادر
- لا تحلل نصوص غير موجودة أمامك
- لا تستنتج معلومات لم تُذكر صراحة

✅ **افعل هذا فقط:**
- استخدم المعلومات المؤكدة من المصادر فقط
- قل "لا أعرف" عند عدم التأكد
- حلل النصوص المُعطاة لك مباشرة فقط  
- استخدم عبارة "وفقاً للمصادر المتاحة"
- ركز على التعليم والمساعدة بالمتاح

🎓 **للسياق التعليمي:**
- كيّف الشرح حسب المرحلة الدراسية  
- استخدم أمثلة بسيطة للصغار
- قدم تحليلاً أعمق للطلاب الأكبر
- لكن لا تختلق أمثلة غير حقيقية أبداً

**تذكر: الصدق أهم من كونك مفيداً. إذا لم تعرف، قل لا أعرف.**"""
        
        return message + safe_instructions

# مثيل واحد للخدمة
ghassan_llm_service = GhassanLLMService()