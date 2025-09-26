# main.py

from netlify_functions import handler

# هذا هو المسار الذي يجب أن يعمل الآن بعد إضافة included_files
from backend.server import app 

def netlify_handler(event, context):
    return handler(event, context, app=app)