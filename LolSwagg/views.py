
from django.shortcuts import render
from store.models import Banner, Feature, Product, PromotionBanner, ReviewRating

def home(request):
    products=Product.objects.all().filter(is_bestseller=True)
    otherproduct=Product.objects.all().filter(is_otherproduct=True)
    banners = Banner.objects.all()
    PromotionBanners = PromotionBanner.objects.all()
    features = Feature.objects.all()
    reviews = None
    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

    context={
        'reviews': reviews,
        'features':features,
        'banners':banners,
        'products':products,
        'otherproduct':otherproduct,
        'PromotionBanners':PromotionBanners,
        }
    return render(request,'home.html', context)

