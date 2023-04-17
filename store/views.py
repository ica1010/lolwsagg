from django.http import HttpResponse
from django.shortcuts import redirect, render
from accounts.models import UserProfile
from carts.models import Cartitems
from carts.views import _cart_id
from orders.models import OrderProduct
from store.form import ReviewForm
from store.models import Product, ProductGallery, ReviewRating
from django.db.models import Q
from django.shortcuts import get_object_or_404
from category.models import category
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.contrib import messages
# Create your views here.
def store(request, category_slug=None):
    categories=None
    products=None

    if category_slug !=None:
        categories=get_object_or_404(category, slug=category_slug )
        products=Product.objects.filter(category=categories, is_available=True)
        paginator= Paginator(products,12)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products=Product.objects.all().filter(is_available=True).order_by('id')
        paginator= Paginator(products,12)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    context={
        'products':paged_products ,
        'product_count':product_count,
    }
    return render(request,'store/store.html',context) 

def product_detail(request, category_slug, product_slug):    
    try:
        products=Product.objects.all().filter(is_bestseller=True)
        otherproduct=Product.objects.all().filter(is_otherproduct=True)
        single_product=Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = Cartitems.objects.filter(Cart__Cart_id=_cart_id(request), product= single_product).exists()
    except Exception as e:
        raise e
    
    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)

    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

    context={
        'product_gallery': product_gallery,
        'orderproduct': orderproduct,
        'reviews': reviews,
        'single_product':single_product,
        'in_cart':in_cart,
        'products':products,
        'otherproduct':otherproduct,
    }
    return render(request,'store/product_detail.html', context)

def search(request, product_count=0):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products= Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword)| Q(Product_name__icontains=keyword))
            product_count = products.count()
        if keyword  == '':
           products= Product.objects.order_by('-created_date')
        else:
            pass
    context = {
        'products':products,
        'product_count':product_count,
    }
    return render(request,'store/store.html',context) 
def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)