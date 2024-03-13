from django.contrib import admin

from ecommerce.models import Category, SubCategory, Product, Color, User, Role, Address, AddressType, State, Country, \
    Order, Rating, Cart, TransactionType, OrderProducts, ProductColors, CartProducts

# Register your models here.
admin.site.register(User)
admin.site.register(Role)
admin.site.register(Address)
admin.site.register(AddressType)
admin.site.register(State)
admin.site.register(Country)

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Color)

admin.site.register(Order)
admin.site.register(Rating)
admin.site.register(TransactionType)
admin.site.register(OrderProducts)
admin.site.register(CartProducts)


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_products')  # Add other fields if needed
    search_fields = ('user__username', 'user__email')  # Add other fields if needed

    def display_products(self, obj):
        return ", ".join([str(product) for product in obj.products.all()])

    display_products.short_description = 'Products'


admin.site.register(Cart, CartAdmin)


class ProductColorsInline(admin.TabularInline):
    model = ProductColors
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    filter_horizontal = ('tests',)
    inlines = [ProductColorsInline]

    def tests(self, obj):
        return ', '.join(color.name for color in obj.colors.all())


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductColors)
