from django.db import models
import random
import string
# Create your models here.

def generate_random_string(length=20):
    characters = string.ascii_letters + string.digits 
    return ''.join(random.choice(characters) for _ in range(length))

class User(models.Model): 
    id = models.CharField(primary_key=True, default=generate_random_string, editable=False, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    image = models.CharField(max_length=10000, null=True, blank=True)
    public_id = models.CharField(max_length=3000, null=True, blank=True)
    original_name = models.CharField(max_length=3000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Medicine(models.Model): 
    id = models.CharField(primary_key=True, default=generate_random_string, editable=False, unique=True)
    medicine_name = models.CharField(max_length = 100)
    medicine_desc = models.CharField(max_length = 1000)
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

class ImageMultiple(models.Model):
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