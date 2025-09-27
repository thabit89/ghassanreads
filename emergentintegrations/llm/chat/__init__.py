# في ملف emergentintegrations/llm/chat/__init__.py
from .chat import LimChat  # (بدلاً من from .LimChat import LimChat)
from .chat import UserMessage # (أضف هذا السطر لضمان استيراد UserMessage أيضًا)