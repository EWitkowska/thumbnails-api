from django.contrib import admin

from .models import ThumbnailDimension, Image, ExpiringLink


@admin.register(ThumbnailDimension)
class ThumbnailDimensionAdmin(admin.ModelAdmin):
    list_filter = ("width", "height")
    list_display = ("dimensions",)
    search_fields = ("width", "height")
    ordering = ("width", "height")

    def dimensions(self, obj):
        return f"{obj.width}x{obj.height}"

    dimensions.admin_order_field = "width"
    dimensions.short_description = "Dimensions (Width x Height)"

    def get_search_results(self, request, queryset, search_term):
        if "x" in search_term:
            width, height = search_term.split("x")
            queryset = queryset.filter(width=width, height=height)
            return queryset, False
        return super().get_search_results(request, queryset, search_term)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_filter = ("user__email",)
    list_display = (
        "user",
        "image",
        "thumbnails",
    )
    search_fields = ("user__email", "image", "thumbnails")
    ordering = ("user", "image", "thumbnails")

    def has_add_permission(self, request):
        return False


@admin.register(ExpiringLink)
class ExpiringLinkAdmin(admin.ModelAdmin):
    list_filter = ("image__user__email",)
    list_display = (
        "image",
        "temporary_link",
        "created_at",
        "expires_in",
    )
    search_fields = ("image__user__email", "temporary_link", "created_at", "expires_in")
    ordering = ("image", "temporary_link", "created_at", "expires_in")

    def has_add_permission(self, request):
        return False
