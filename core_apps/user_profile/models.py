from typing import Any
from decimal import Decimal
from cloudinary.models import CloudinaryField
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from core_apps.common.models import TimeStampedModel

User = get_user_model()

class Profile(TimeStampedModel):
    """
    Class for storing KYC information
    (Know your customer)
    """
    class Salutation(models.TextChoices):
        MR = "mr", _("Mr.")
        MRS = "mrs", _("Mrs.")
        MISS = "miss", _("Miss")
    
    class Gender(models.TextChoices):
        MALE = "male", _("Male")
        FEMALE = "female", _("Female")
    
    class MaritalStatus(models.TextChoices):
        SINGLE = "single", _("Single")
        MARRIED = "married", _("Married")
        WIDOWED = "widowed", _("Widowed")
        DIVORCED = "divorced", _("Divorced")
    
    class IdentificationMeans(models.TextChoices):
        PASSPORT = "passport", _("Passport")
        DRIVER_LICENSE = "driver_license", _("Driver License")
        NATIONAL_ID = "national_id", _("National ID")

    class EmploymentStatus(models.TextChoices):
        SELF_EMPLOYED = "self_employed", _("Self Employed")
        EMPLOYED = "employed", _("Employed")
        UNEMPLOYED = "unemployed", _("Unemployed")
        RETIRED = "retired", _("Retired")
        STUDENT = "student", _("Student")
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    title = models.CharField(
        _("Salutation"), max_length=10, choices=Salutation.choices, default=Salutation.MR
    )
    gender = models.CharField(max_length=10, choices=Gender.choices, default=Gender.MALE)
    date_of_birth = models.DateField(
        _("Date of Birth"), default=settings.DEFAULT_BIRTH_DATE
    )
    country_of_birth = CountryField(
        _("Country of Birth"), default=settings.DEFAULT_COUNTRY
    )
    place_of_birth = models.CharField(
        _("Place of Birth"), max_length=50, default="Unknown"
    )
    marital_status = models.CharField(
        _("Marital Status"), max_length=20, choices=MaritalStatus.choices
    )
    identification_means = models.CharField(
        _("Means of Identification"),
        max_length=20,
        choices=IdentificationMeans.choices,
        default=IdentificationMeans.NATIONAL_ID,
    )
    id_issue_date = models.DateField(
        _("Date of Issue"), default=settings.DEFAULT_DATE
    )
    id_expiry_date = models.DateField(
        _("Expiry Date"), default=settings.DEFAULT_EXPIRY_DATE
    )
    nationality = models.CharField(
        _("Nationality"), max_length=50, default="Unknown"
    )
    phone_number = PhoneNumberField(
        _("Phone Number"), default="Unknown"
    )
    address = models.CharField(
        _("Address"), max_length=100, default="Unknown"
    )
    city = models.CharField(
        _("City"), max_length=50, default="Unknown"
    )
    country = CountryField(
        _("Country"), default=settings.DEFAULT_COUNTRY
    )
    postal_code = models.CharField(
        _("Postal Code"), max_length=10, default="Unknown"
    )
    employment_status = models.CharField(
        _("Employment Status"), 
        max_length=20, 
        choices=EmploymentStatus.choices,
        default=EmploymentStatus.EMPLOYED
    )
    employer_name = models.CharField(
        _("Employer Name"), 
        max_length=50, 
        null=True,
        blank=True,
    )
    annual_income = models.DecimalField(
        _("Annual Income"), 
        max_digits=12, 
        decimal_places=2,
        default=Decimal(0.00),
    )
    employer_address = models.CharField(
        _("Employer Address"), 
        max_length=100, 
        null=True,
        blank=True,
    )
    employer_city = models.CharField(
        _("Employer City"), 
        max_length=50, 
        null=True,
        blank=True,
    )
    employer_state = models.CharField(
        _("Employer State"),
        max_length=50, 
        null=True,
        blank=True,
    )
    photo = CloudinaryField(
        _("Photo"),
        blank=True,
        null=True
    )
    photo_url = models.URLField(
        _("Photo URL"),
        blank=True,
        null=True,
    )
    id_photo = CloudinaryField(
        _("ID Photo"),
        blank=True,
        null=True
    )
    id_photo_url = models.URLField(
        _("ID Photo URL"),
        blank=True,
        null=True,
    )
    signature_photo = CloudinaryField(
        _("Signature Photo"),
        blank=True,
        null=True
    )
    signature_photo_url = models.URLField(
        _("Signature Photo URL"),
        blank=True,
        null=True,
    )

    def clean(self) -> None:
        super().clean()
        if self.id_expiry_date and self.id_issue_date:
            if self.id_expiry_date < self.id_issue_date:
                raise ValidationError(_("ID Expiry Date cannot be before ID Issue Date"))

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def is_complete_with_next_of_kin(self):
        required_fields = [
            self.title,
            self.gender,
            self.date_of_birth,
            self.country_of_birth,
            self.place_of_birth,
            self.marital_status,
            self.identification_means,
            self.id_issue_date,
            self.id_expiry_date,
            self.nationality,
            self.phone_number,
            self.address,
            self.city,
            self.country,
            self.employment_status,
            self.photo,
            self.id_photo,
            self.signature_photo
        ]

        return all(required_fields) and self.next_of_kin.exists()
    
    def __str__(self):
        return f"{self.title} {self.user.first_name} {self.user.last_name}"

class NextOfKin(TimeStampedModel):
    class Gender(models.TextChoices):
        MALE = "male", _("Male")
        FEMALE = "female", _("Female")
    
    class Salutation(models.TextChoices):
        MR = "mr", _("Mr.")
        MRS = "mrs", _("Mrs.")
        MISS = "miss", _("Miss")

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="next_of_kin")
    title = models.CharField(_("Title"), max_length=20, choices=Salutation.choices)
    first_name = models.CharField(_("First Name"), max_length=50)
    last_name = models.CharField(_("Last Name"), max_length=50)
    gender = models.CharField(_("Gender"), max_length=10, choices=Gender.choices)
    date_of_birth = models.DateField(_("Date of Birth"))
    relationship = models.CharField(_("Relationship"), max_length=50)
    email = models.EmailField(_("Email"),db_index=True)
    phone_number = PhoneNumberField(_("Phone Number")) 
    address = models.CharField(_("Address"), max_length=100)
    city = models.CharField(_("City"), max_length=50)
    country = CountryField(_("Country"))   
    is_primary = models.BooleanField(_("Is Primary"), default=False)

    def clean(self) -> None:
        super().clean()
        if self.is_primary:
            primary_kin = NextOfKin.objects.filter(
                profile= self.profile,
                is_primary=True
            ).exclude(pk=self.pk)
            if primary_kin.exists():
                raise ValidationError(_("Only one primary next of kin is allowed"))
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} {self.first_name} {self.last_name}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["profile", "is_primary"],
                # Enforce the unique constraint only for records
                # where is_primary is True
                condition=models.Q(is_primary=True),
                name="unique_primary_next_of_kin",
            )
        ]
   