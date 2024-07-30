from django.contrib import admin
from .models import Category,Post,Order,OrderItem,Payment


admin.site.register(Category)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title","price","category","created")
    list_select_related = ("category",)
    search_fields = ("title","content","category")
    list_filter = ("created","category")


admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Payment)