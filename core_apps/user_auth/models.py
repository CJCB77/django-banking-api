import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .emails import send_account_locked_email
from .managers import UserManager

class CustomUser(AbstractUser):
    class SecurityQuestions(models.TextChoices):
        MAIDEN_NAME = (
            "maiden_name",
            _("What is your mother's maiden name?"),
        )
        FAVORITE_COLOR = (
            "favorite_color",
            _("What is your favorite color?"),
        )
        BIRTH_CITY = (
            "birth_city",
            _("What city were you born in?"),
        )
        PET_NAME = (
            "pet_name",
            _("What is your first  pet's name?"),
        )
    
    class AccountStatus(models.TextChoices):
        ACTIVE = "active", _("Active")
        LOCKED = "locked", _("Locked")
    
    class RoleChoices(models.TextChoices):
        CUSTOMER = "customer", _("Customer")
        ACCOUNT_EXECUTIVE = "account_executive", _("Account Executive")
        TELLER = "teller", _("Teller")
        BRANCH_MANAGER = "branch_manager", _("Branch Manager")
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(_("Username"), max_length=12, unique=True)
    security_question = models.CharField(
        _("Security Question"),
        max_length=50,
        choices=SecurityQuestions.choices,
    )
    security_answer = models.CharField(_("Security Answer"), max_length=50)
    email = models.EmailField(_("Email"), unique=True, db_index=True)
    first_name = models.CharField(_("First name"), max_length=30)
    middle_name = models.CharField(_("Middle name"), max_length=30, blank=True, null=True)
    last_name = models.CharField(_("Last name"), max_length=30)
    id_no = models.CharField(_("ID Number"), max_length=10, unique=True)
    account_status = models.CharField(
        _("Account Status"),
        choices=AccountStatus.choices,
        default=AccountStatus.ACTIVE,
    )
    role = models.CharField(
        _("Role"),
        choices=RoleChoices.choices,
        default=RoleChoices.CUSTOMER,
    )
    failed_login_attempts = models.PositiveSmallIntegerField(default=0)
    last_failed_login = models.DateTimeField(null=True, blank=True)
    otp = models.CharField(_("OTP"),max_length=6, null=True, blank=True)
    otp_expiry_time = models.DateTimeField(_("OTP Expiry Time"), null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "id_no",
        "security_question",
        "security_answer",
    ]
    
    def set_otp(self, otp: str)-> None:
        self.otp = otp,
        self.otp_expiry_time = timezone.now() + settings.OTP_EXPIRATION
        self.save()
    
    def verify_otp(self, otp:str)-> bool:
        if self.otp == otp and self.otp_expiry_time > timezone.now():
            self.otp = ""
            self.otp_expiry_time = None
            self.save()
            return True
        
        return False

    def handle_failed_login_attempt(self) -> None:
        self.failed_login_attempts += 1
        self.last_failed_login = timezone.now()
        if self.failed_login_attempts >= settings.LOGIN_ATTEMPTS:
            self.account_status = self.AccountStatus.LOCKED
            self.save()
            send_account_locked_email(self)
        self.save()
    
    def reset_failed_login_attempts(self) -> None:
        self.failed_login_attempts = 0
        self.last_failed_login = None
        self.account_status = self.AccountStatus.ACTIVE
        self.save()

    def unlock_account(self) -> None:
        if self.is_locked:
            self.reset_failed_login_attempts()
    
    def unlock_if_expired(self) -> bool:
        if self.is_locked and self.last_failed_login:
            if (
                timezone.now() - self.last_failed_login
                > settings.LOCKOUT_DURATION
            ):
                self.unlock_account()
                return True
        return False

    @property
    def is_locked(self) -> bool:
        return self.account_status == self.AccountStatus.LOCKED

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name = _("User")    
        verbose_name_plural = _("Users")
        ordering = ["-date_joined"]
    
    def has_role(self, role_name:str) -> bool:
        return hasattr(self, "role") and self.role == role_name

    def __str__(self) -> str:
        return f"{self.full_name} - {self.get_role_display()}"