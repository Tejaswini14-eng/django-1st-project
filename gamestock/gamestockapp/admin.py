from django.contrib import admin
from gamestockapp.models import product, cart, Review,orders
# Register your models here.

class productAdmin(admin.ModelAdmin):
    list_display = ['id','prod_name','price','category']
    list_filter= ['category']

admin.site.register(product, productAdmin)
admin.site.register(cart)
admin.site.register(orders)
admin.site.register(Review)
