from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from dairyapp.models import (
    Vendor, 
    MilkCategory, 
    vendorledger, 
    Profile, 
    CustomerMilkCategory, 
    Customerledger
)


#********************************************#
#       ||  Vendor Classes Started  ||       #
#********************************************#
@admin.register(Vendor)
class Vendor_Admin(admin.ModelAdmin):
    list_display = ['vendorname', 'managername', 'joiningdate', 'vendorcontact']
    search_fields = ['vendorname', 'managername', 'vendorcontact']
    list_filter = ['status', 'joiningdate']
    ordering = ['-joiningdate']


@admin.register(MilkCategory)
class MilkCategory_Admin(admin.ModelAdmin):
    list_display = ['animalname', 'milkprice', 'related_vendor']
    list_filter = ['animalname', 'milkprice']
    search_fields = ['animalname', 'related_vendor__vendorname']
    ordering = ['animalname']


@admin.register(vendorledger)
class vendorledger_Admin(admin.ModelAdmin):
    list_display = ['related_vendor', 'related_milkcategory', 'date', 'price', 'quantity', 'total']
    list_filter = ['related_vendor', 'related_milkcategory', 'date']
    search_fields = ['related_vendor__vendorname', 'related_milkcategory__animalname']
    ordering = ['-date']
    readonly_fields = ['total']  # Make total read-only as it's calculated
    fields = ['related_vendor', 'related_milkcategory', 'date', 'price', 'quantity', 'total']
    
    # Optional: Add calculated total if not stored in DB
    # def save_model(self, request, obj, form, change):
    #     obj.total = obj.price * obj.quantity
    #     super().save_model(request, obj, form, change)


#**********************************************#
#       ||  Customer Classes Started  ||       #
#**********************************************#
@admin.register(Profile)
class Profile_Admin(admin.ModelAdmin):
    list_display = ['__str__', 'user_type', 'contact_number', 'address']
    list_filter = ['user_type', 'joining_data']
    search_fields = ['user__username', 'user__email', 'contact_number']
    ordering = ['-joining_data']
    raw_id_fields = ['user']  # Better for large user tables


@admin.register(CustomerMilkCategory)
class CustomerMilkCategory_Admin(admin.ModelAdmin):
    list_display = ['fullname', 'animalname', 'milkprice']
    list_filter = ['animalname', 'milkprice']
    search_fields = ['related_customer__username', 'animalname']
    ordering = ['related_customer__username', 'animalname']
    
    def fullname(self, obj):
        """Get the full name of the customer."""
        return obj.related_customer.get_full_name() if obj.related_customer else "Unknown"
    fullname.short_description = "Customer Name"


@admin.register(Customerledger)
class Customerledger_Admin(admin.ModelAdmin):
    list_display = ['related_customer', 'date', 'quantity', 'price', 'total']
    list_filter = ['related_customer', 'date']
    search_fields = ['related_customer__username', 'related_customer__email']
    ordering = ['-date']
    readonly_fields = ['total']  # Make total read-only as it's calculated
    fields = ['related_customer', 'related_milk_category', 'date', 'price', 'quantity', 'total']
     