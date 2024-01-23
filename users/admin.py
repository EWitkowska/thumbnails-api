from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from .forms import UserAdminChangeForm, UserAdminCreationForm
from .models import Account

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (
            None,
            {"fields": ("email", "password", "account_type")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["email", "account_type", "is_superuser", "is_staff", "is_active"]
    search_fields = ["email", "account_type__name"]
    ordering = ["id"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "account_type",
                ),
            },
        ),
    )


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_filter = ("can_retrieve_original_image", "can_generate_expiring_link")
    list_display = [
        "name",
        "can_retrieve_original_image",
        "can_generate_expiring_link",
        "thumbnail_dimensions_list",
    ]
    search_fields = ["name"]
    ordering = ["id"]
    filter_horizontal = ("thumbnail_dimensions",)

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "name",
                    "can_retrieve_original_image",
                    "can_generate_expiring_link",
                    "thumbnail_dimensions",
                ),
            },
        ),
    )

    def thumbnail_dimensions_list(self, obj):
        return ", ".join(
            [str(dimension) for dimension in obj.thumbnail_dimensions.all()]
        )

    thumbnail_dimensions_list.short_description = "Thumbnail Dimensions"
