from django.contrib import admin
# التعديل المطلوب: استيراد include
from django.urls import path, include 

# استيراد الإعدادات (settings) ووحدة static لملفات الميديا
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # التعديل المطلوب: ربط مسارات تطبيق library بالمسار الرئيسي للموقع ('')
    path('', include('library.urls')), 
]

# إعداد لخدمة ملفات الميديا في وضع التطوير (DEBUG)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)