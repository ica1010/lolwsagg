from django.db import models
from django.urls import reverse, reverse_lazy
from accounts.models import Account, UserProfile
from category.models import category
from django.db.models import Avg, Count
# Create your models here.

class Product(models.Model):
    Product_name=models.CharField(max_length=50 ,unique=True )
    slug=models.SlugField(max_length=50 ,unique=True )
    description=models.TextField(max_length=500 ,blank=True )
    price=models.IntegerField()
    images= models.ImageField(upload_to='photo/product')
    stock=models.IntegerField()
    is_available=models.BooleanField(default=True)
    is_bestseller=models.BooleanField(default=False)
    is_otherproduct=models.BooleanField(default=False)
    category= models.ForeignKey(category, on_delete=models.CASCADE)
    created_date= models.DateTimeField(auto_now_add=True)
    modified_date= models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
    
    def __str__(self):
        return self.Product_name
    
    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count
    
class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)
    

variation_category_choice= {
    ('color', 'color'),
    ('size', 'size'),
}

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=50, choices=variation_category_choice)
    variation_value = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_date= models.DateTimeField(auto_now_add=True)

    objects = VariationManager()

    def __str__(self):

        return self.variation_value
    
class Feature(models.Model):
    feature_name = models.CharField(max_length=50)
    images= models.ImageField(upload_to='photo/feature')
    created_date= models.DateTimeField(auto_now_add=True)
    modified_date= models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.feature_name
    
class Banner(models.Model):
    banner_name = models.CharField(max_length=50)
    banner_text = models.TextField()
    images= models.ImageField(upload_to='photo/banner')
    created_date= models.DateTimeField(auto_now_add=True)
    modified_date= models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.banner_name

class PromotionBanner(models.Model):
    promotion_name = models.CharField(max_length=50)
    promotion = models.CharField(max_length=100)
    images= models.ImageField(upload_to='photo/PromotionBanner')
    created_date= models.DateTimeField(auto_now_add=True)
    modified_date= models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.promotion_name
    
class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/products', max_length=255)

    def __str__(self):
        return self.product.Product_name

    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery'
