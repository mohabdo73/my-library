# ==========================================================
# الموقع: my_library/library/admin.py
# ==========================================================
from django.contrib import admin
from .models import Book, Cart, CartItem, Order # استيراد النماذج الجديدة

# لتجميل عرض النموذج في لوحة الإدارة
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'stock_count', 'category', 'date_added')
    list_filter = ('category', 'author')
    search_fields = ('title', 'author', 'description')

# تسجيل النموذج الأساسي (الكتاب)
admin.site.register(Book, BookAdmin)

# تسجيل النماذج الجديدة
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)