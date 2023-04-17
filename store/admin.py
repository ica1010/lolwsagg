from django.contrib import admin
from .models import Banner, Feature, Product, ProductGallery, PromotionBanner, ReviewRating, Variation
import admin_thumbnails

@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display =('Product_name','price','stock','category','modified_date','is_available','is_bestseller','is_otherproduct')
    list_editable = ('is_bestseller',)
    list_editable = ('is_otherproduct',)
    prepopulated_fields={'slug':('Product_name',)}
    inlines = [ProductGalleryInline]
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value','is_active' )
    list_editable = ('is_active',)
    list_filter= ('product', 'variation_category', 'variation_value')


class BannerAdmin(admin.ModelAdmin):
    list_display = ('banner_name','images', 'modified_date', 'created_date' )
    list_filter= ('modified_date', 'created_date')
class FeatureAdmin(admin.ModelAdmin):
    list_display = ( 'feature_name','images','modified_date', 'created_date' )
    list_filter= ('modified_date', 'created_date')

class PromotionBannerAdmin(admin.ModelAdmin):
    list_display = ('promotion_name','promotion','images', 'modified_date', 'created_date')
    list_filter= ('modified_date', 'created_date')

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)


admin.site.register(Banner,BannerAdmin)
admin.site.register(PromotionBanner,PromotionBannerAdmin)
admin.site.register(Feature,FeatureAdmin)
admin.site.register(ProductGallery)
