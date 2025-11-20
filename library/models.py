# ==========================================================
# الموقع: my_library/library/models.py
# ==========================================================

from django.db import models
from django.contrib.auth.models import User # لاستخدام نموذج المستخدم

# ----------------------------------------------
# 1. نموذج الكتاب (Book) - المخزون الأساسي
# ----------------------------------------------
class Book(models.Model):
    # بيانات الكتاب
    title = models.CharField(max_length=200, verbose_name="العنوان")
    author = models.CharField(max_length=150, verbose_name="المؤلف")
    description = models.TextField(verbose_name="الوصف")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="السعر")
    
    # الصورة والمخزون
    cover_image = models.ImageField(upload_to='book_covers/', verbose_name="صورة الغلاف", blank=True, null=True) 
    stock_count = models.IntegerField(default=0, verbose_name="المخزون المتوفر")

    # التصنيف
    CATEGORY_CHOICES = [
        ('FICTION', 'خيال'),
        ('SCIENCE', 'علوم'),
        ('HISTORY', 'تاريخ'),
        ('BUSINESS', 'أعمال'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='FICTION', verbose_name="التصنيف")
    
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإضافة")

    class Meta:
        verbose_name = "كتاب"
        verbose_name_plural = "الكتب"
        ordering = ['-date_added']

    def __str__(self):
        return self.title


# ----------------------------------------------
# 2. نموذج عربة التسوق (Cart)
# ----------------------------------------------
class Cart(models.Model):
    # يربط السلة بمستخدم واحد.
    # on_delete=models.CASCADE يعني إذا حُذف المستخدم، تُحذف سلة التسوق الخاصة به.
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="المستخدم")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")

    class Meta:
        verbose_name = "عربة التسوق"
        verbose_name_plural = "عربات التسوق"
        
    def __str__(self):
        return f"سلة المستخدم {self.user.username}"


# ----------------------------------------------
# 3. نموذج عنصر السلة (CartItem)
# ----------------------------------------------
class CartItem(models.Model):
    # يربط عنصر السلة بسلة محددة
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name="عربة التسوق")
    # يربط عنصر السلة بكتاب محدد
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="الكتاب")
    quantity = models.IntegerField(default=1, verbose_name="الكمية")

    class Meta:
        verbose_name = "عنصر السلة"
        verbose_name_plural = "عناصر السلة"
        # يضمن عدم تكرار نفس الكتاب في نفس السلة مرتين (لتحديث الكمية بدلاً من الإضافة)
        unique_together = ('cart', 'book') 

    def __str__(self):
        return f"{self.quantity} x {self.book.title} في سلة {self.cart.user.username}"

    @property
    def get_total_price(self):
        # خاصية لحساب سعر الكمية
        return self.book.price * self.quantity


# ----------------------------------------------
# 4. نموذج الطلب (Order)
# ----------------------------------------------
class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'قيد المعالجة'),
        ('SHIPPED', 'تم الشحن'),
        ('DELIVERED', 'تم التوصيل'),
        ('CANCELLED', 'ملغى'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="المستخدم")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الطلب")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="الإجمالي")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name="حالة الطلب")
    
    # تفاصيل الشحن
    shipping_address = models.TextField(verbose_name="عنوان الشحن")
    payment_method = models.CharField(max_length=50, verbose_name="طريقة الدفع")
    
    class Meta:
        verbose_name = "طلب شراء"
        verbose_name_plural = "طلبات الشراء"
        ordering = ['-created_at']

    def __str__(self):
        return f"طلب رقم {self.id} للمستخدم {self.user.username}"