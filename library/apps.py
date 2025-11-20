from django.apps import AppConfig


class LibraryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'library'
    # التعديل المطلوب: إضافة الاسم المعروض
    verbose_name = 'تطبيق المكتبة'