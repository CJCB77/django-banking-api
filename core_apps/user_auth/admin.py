from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser as User
from .forms import UserChangeForm, UserCreationForm


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    form = UserChangeForm
    add_for = UserCreationForm
    model = User

    list_display = [
        "email",
        "username",
        "first_name",
        "last_name",
        "role",
        "account_status",
        "is_staff",
        "is_active",
    ]

    list_filter = ["email", "is_staff", "role", "is_active"]
    fieldsets = (
        (_("User Credentials"), {"fields": ("username","email", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "middle_name",
                    "last_name",
                    "id_no",
                )
            },
        ),
        (
            _("Account Status"),
            {
                "fields": (
                    "account_status",
                    "failed_login_attempts",
                    "last_failed_login",
                    "otp",
                    "otp_expiry_time",
                )
            },
        ),
        (
            _("Security"),
            {
                "fields":(
                    "security_question",
                    "security_answer",
                )
            }
        ),
        (
            _("Permissions and Groups"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            _("Important dates"),
            {
                "fields": (
                    "last_login",
                    "date_joined",
                )
            },
        )
    )

    search_fields = ["email", "first_name", "last_name", "username"]
    ordering = ["email"]