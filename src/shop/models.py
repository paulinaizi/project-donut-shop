from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

class CustomUserManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
    
    def normalize_email(self, email):
        email = super().normalize_email(email)
        return email.lower() if email else email

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager() 

    def __str__(self):
        return self.email   

    class Meta:
        verbose_name = "Użytkownik"
        verbose_name_plural = "Użytkownicy"
    
class Donut(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(default=0.00, max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='uploads/donuts/')
    is_custom_base = models.BooleanField(default=False)
    coating = models.ForeignKey('Coating', null=True, blank=True, on_delete=models.CASCADE)
    sprinkle = models.ForeignKey('Sprinkle', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Donuty'

class Sprinkle(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(default=0.00, max_digits=4, decimal_places=2)
    image = models.ImageField(upload_to='uploads/sprinkles/')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Posypka'
        verbose_name_plural = 'Posypki'

class Coating(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(default=0.00, max_digits=4, decimal_places=2)
    image = models.ImageField(upload_to='uploads/coatings/')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Polewa'
        verbose_name_plural = 'Polewy'