from django.urls import path
from . import views  

app_name = 'library' 

urlpatterns = [
    # رابط الصفحة الرئيسية
    path('', views.home_view, name='home'), 
    
    # 1. رابط قائمة الكتب
    path('books/', views.book_list, name='book_list'), 
    
    # 2. رابط تفاصيل كتاب محدد (باستخدام المفتاح الأساسي pk)
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    # هذا هو المسار الجديد لإضافة الكتاب
    path('add-to-cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),

    path('cart/', views.cart_detail, name='cart_detail'),

]