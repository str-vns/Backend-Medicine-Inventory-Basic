from django.db import models
import random
import string
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.

def generate_random_string(length=20):
    characters = string.ascii_letters + string.digits 
    return ''.join(random.choice(characters) for _ in range(length))
class UserManager(BaseUserManager):
     
    def _create_user(self, email, password=None, first_name=None, last_name=None, **extra_fields):
        values = [email, first_name, last_name, password]
        field_values = dict(zip(self.model.REQUIRED_FIELDS, values))
        for field, value in field_values.items():
            if not value:
                raise ValueError(f"The {field} field must be set.")
            
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, name, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, name, phone, password, **extra_fields)
    
    def create_superuser(self, email, password=None, first_name=None, last_name=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, first_name, last_name, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(primary_key=True, default=generate_random_string, editable=False, unique=True)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    image = models.CharField(max_length=10000, null=True, blank=True)
    public_id = models.CharField(max_length=3000, null=True, blank=True)
    original_name = models.CharField(max_length=3000, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name','password']
    
    def __str__(self):
        return self.email
    def get_first_name(self):
        return self.first_name if self.first_name else "No First Name"
    def get_last_name(self):
        return self.last_name if self.last_name else "No Last Name"
    def masked_password(self, obj):
        return '*' * 8  
    masked_password.short_description = 'Password'


class Medicine(models.Model):
    id = models.CharField(primary_key=True, default=generate_random_string, editable=False, unique=True)
    medicine_name = models.CharField(max_length=100)
    medicine_desc = models.CharField(max_length=1000)
    onActive = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.medicine_name

class Inventory(models.Model):
    
    MEDICINE_TYPE = [
        ('tablet', 'Tablet'),
        ('capsule', 'Capsule'),
        ('liquid', 'Liquid'),
        ('suppositories', 'Suppositories'),
        ('drops', 'Drops'),
        ('inhalers', 'Inhalers'),
        ('injections', 'Injections'),
        ('implants', 'Implants'),
        ('creams', 'Creams'),
        ('patches', 'Patches'),
    ]
    
    id = models.CharField(primary_key=True, default=generate_random_string, editable=False, unique=True)
    medicine_id = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    medicine_price = models.FloatField()
    quantity = models.IntegerField()
    medicine_type = models.CharField(max_length=50, choices=MEDICINE_TYPE)
    medicine_measurement = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=100)
    onActive = models.BooleanField(default=True)
    expiration_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

class MultipleUpload(models.Model):
    id = models.CharField(primary_key=True, default=generate_random_string, editable=False, unique=True)  
    item_id = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    public_id = models.CharField(max_length=3000, null=True, blank=True)
    original_name = models.CharField(max_length=3000, null=True, blank=True)
    url = models.CharField(max_length=10000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True) 

def clean(self):
    super().clean()
    valid_keys = [key for key, _ in self.MEDICINE_TYPE]
    if self.medicine_type not in valid_keys:
        raise ValueError(f"Invalid medicine type. Choose from {valid_keys}")
    
    def __str__(self):
        return self.medicine_id