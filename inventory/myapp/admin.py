from django.contrib import admin
from .models import User, Medicine, Inventory, MultipleUpload
# Register your models here.

class InventoryInline(admin.TabularInline):
    model = Inventory
    extra = 1

class ImageMedInline(admin.TabularInline):
    model = MultipleUpload
    extra = 1

# User
class UserAdmin(admin.ModelAdmin): 
     fieldsets = (
        (None, {'fields' : ('email', 'password', 'is_staff', 'is_active', 'is_superuser')}),
        ('Personal Info', {'fields' : ('first_name', 'last_name', 'image', 'public_id', 'original_name')}),
        ('Permissions', {'fields' : ('user_permissions',)}), 
    )
    
     add_fieldsets = (
        (None, {'fields' : ('email', 'password', 'is_staff', 'is_active', 'is_superuser')}),
        ('Personal Info', {'fields' : ('first_name', 'last_name', 'image', 'public_id', 'original_name')}),
        ('Permissions', {'fields' : ('user_permissions',)}), 
    )
    
     search_fields = ('email', 'first_name', 'last_name')
     ordering = ('email',)
     filter_horizontal = ()

# Medicine
class MedicineAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields' : ['medicine_name']}),
        (None, {'fields' : ['medicine_desc']}),
        (None, {'fields' : ['onActive']}),
        (None, {'fields' : ['created_at']}),
        (None, {'fields' : ['deleted_at']}),
    ]
    inlines = [InventoryInline, ImageMedInline]
    list_display = ('medicine_name', 'medicine_desc', 'onActive','created_at','deleted_at')
    
# Inventory    
class InventoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields' : ['medicine_id']}),
        (None, {'fields' : ['medicine_price']}),
        (None, {'fields' : ['quantity']}),
        (None, {'fields' : ['medicine_type']}),
        (None, {'fields' : ['medicine_measurement']}),
        (None, {'fields' : ['manufacturer']}),
        (None, {'fields' : ['expiration_date']}),
        (None, {'fields' : ['onActive']}),
        (None, {'fields' : ['created_at']}),
        (None, {'fields' : ['deleted_at']}),  
    ]
    list_display = ('medicine_id', 'medicine_price', 'quantity','medicine_type','medicine_measurement','manufacturer','expiration_date','onActive','created_at','deleted_at')

class MultipleUploadAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields' : ['item_id']}),
        (None, {'fields' : ['public_id']}),
        (None, {'fields' : ['original_name']}),
        (None, {'fields' : ['url']}),
        (None, {'fields' : ['created_at']}),
    ]
    list_display = ('item_id', 'public_id', 'original_name','url','created_at')


admin.site.register(User, UserAdmin)
admin.site.register(Medicine, MedicineAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(MultipleUpload, MultipleUploadAdmin)