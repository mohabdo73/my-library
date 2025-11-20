from django.shortcuts import render, get_object_or_404
from .models import Book # استيراد نموذج الكتاب

# ==========================================================
# 1. تعديل دالة الصفحة الرئيسية (لعرض أحدث 4 كتب)
# ==========================================================
def home_view(request):
    # جلب أحدث 4 كتب مرتبة حسب تاريخ الإضافة
    latest_books = Book.objects.all().order_by('-date_added')[:4]
    context = {
        'latest_books': latest_books
    }
    return render(request, 'library/home.html', context)

# ==========================================================
# 2. دالة قائمة الكتب (لعرض جميع الكتب)
# ==========================================================
def book_list(request):
    # جلب جميع الكتب
    all_books = Book.objects.all().order_by('-date_added')
    context = {
        'books': all_books,
        'page_title': 'جميع الكتب المتاحة'
    }
    return render(request, 'library/book_list.html', context)

# ==========================================================
# 3. دالة تفاصيل الكتاب
# ==========================================================
def book_detail(request, pk):
    # جلب الكتاب حسب المفتاح الأساسي (pk)، وإظهار 404 إذا لم يتم العثور عليه
    book = get_object_or_404(Book, pk=pk)
    context = {
        'book': book
    }
    return render(request, 'library/book_detail.html', context)

# ==========================================================
# 4. دالة تفاصيل سلة التسوق
# ==========================================================
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book

# 1. دالة إضافة الكتاب للسلة
def add_to_cart(request, book_id):
    # جلب السلة الحالية من الجلسة أو إنشاء سلة فارغة
    cart = request.session.get('cart', {})
    
    # تحويل المعرف لنص لأن مفاتيح الجلسة تخزن كنصوص
    book_id = str(book_id)
    
    if book_id in cart:
        cart[book_id] += 1  # زيادة الكمية إذا كان موجوداً
    else:
        cart[book_id] = 1   # إضافته لأول مرة
        
    # حفظ السلة في الجلسة
    request.session['cart'] = cart
    
    # التوجيه لصفحة السلة لرؤية النتيجة
    return redirect('library:cart_detail')

# 2. دالة عرض السلة (تعديل الدالة الموجودة)
def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    grand_total = 0

    for book_id, quantity in cart.items():
        book = get_object_or_404(Book, id=book_id)
        total_price = book.price * quantity
        grand_total += total_price
        
        cart_items.append({
            'book': book,
            'quantity': quantity,
            'total_price': total_price
        })

    context = {
        'cart_items': cart_items,
        'grand_total': grand_total
    }
    return render(request, 'library/cart_detail.html', context)