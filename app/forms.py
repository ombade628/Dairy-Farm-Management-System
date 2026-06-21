from django import forms
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from dairyapp.models import Vendor, MilkCategory, Profile, CustomerMilkCategory, Customerledger
import datetime
import re


class ContactForm(forms.Form):
    """Contact form for user inquiries."""
    name = forms.CharField(
        required=True, 
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'})
    )
    subject = forms.CharField(
        required=True, 
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com'})
    )
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control', 'cols': 20, 'rows': 3, 'placeholder': 'Your message...'})
    )


class SignUpForm(UserCreationForm):
    """User registration form with additional fields."""
    first_name = forms.CharField(
        max_length=30, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=30, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    email = forms.EmailField(
        max_length=254, 
        required=True,
        help_text='Required. Inform a valid email address.',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com'})
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        }

    def clean_email(self):
        """Validate that email is unique."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('A user with this email already exists.')
        return email

    def clean_username(self):
        """Validate username format."""
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValidationError('Username can only contain letters, numbers, and underscores.')
        return username


#*******************************************#
#       ||  Vendors Forms Started  ||       #
#*******************************************#

class AddVendorForm(forms.Form):
    """Form for adding a new vendor."""
    ANIMAL_CHOICES = (
        ('Cow', 'Cow'),
        ('Buffaloe', 'Buffalo'),
        ('Others', 'Others'),
    )
    
    Manager_Name = forms.CharField(
        required=True, 
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Manager Name'})
    )
    Vendor_Name = forms.CharField(
        required=True, 
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Vendor Name'})
    )
    joining_date = forms.DateField(
        initial=datetime.date.today,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    Address = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Address'})
    )
    Vendor_Contact = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Number'})
    )
    Status = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    def clean_Vendor_Contact(self):
        """Validate contact number format."""
        contact = self.cleaned_data.get('Vendor_Contact')
        if not re.match(r'^[0-9]{10,15}$', contact):
            raise ValidationError('Contact number must be 10-15 digits.')
        return contact


class MilkCategoryForm(forms.ModelForm):
    """Form for milk category."""
    class Meta:
        model = MilkCategory
        fields = ('animalname', 'milkprice', 'related_vendor')
        widgets = {
            'animalname': forms.Select(attrs={'class': 'form-control'}),
            'milkprice': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'related_vendor': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'animalname': 'Animal Name',
            'milkprice': 'Milk Price (per liter)',
            'related_vendor': 'Vendor',
        }

    def clean_milkprice(self):
        """Validate milk price is positive."""
        price = self.cleaned_data.get('milkprice')
        if price <= 0:
            raise ValidationError('Milk price must be greater than 0.')
        return price


class VendorLedgerForm(forms.Form):
    """Form for vendor ledger entries."""
    ANIMAL_CHOICES = (
        ('Cow', 'Cow'),
        ('Buffaloe', 'Buffalo'),
        ('Others', 'Others'),
    )
    DAY_CHOICES = (
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    )
    
    Milk_Category = forms.ChoiceField(
        label='Milk Category',
        choices=ANIMAL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    Day = forms.ChoiceField(
        label='Day',
        choices=DAY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    Quantity = forms.DecimalField(
        label='Quantity (liters)',
        required=False,
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'})
    )

    def clean_Quantity(self):
        """Validate quantity is positive."""
        quantity = self.cleaned_data.get('Quantity')
        if quantity and quantity <= 0:
            raise ValidationError('Quantity must be greater than 0.')
        return quantity


#***************************************************#
#       ||  Customer Forms (User) Started  ||       #
#***************************************************#

class ProfileForm(forms.ModelForm):
    """Form for user profile."""
    USER_TYPE_CHOICES = (
        ('Admin', 'Admin'),
        ('Customer', 'Customer'),
        ('Manager', 'Manager'),
    )
    
    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    joining_data = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    contact_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Number'})
    )
    address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Address'})
    )

    class Meta:
        model = Profile
        fields = ('user', 'user_type', 'contact_number', 'joining_data', 'address')
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'user': 'User',
            'joining_data': 'Joining Date',
        }

    def clean_contact_number(self):
        """Validate contact number format."""
        contact = self.cleaned_data.get('contact_number')
        if contact and not re.match(r'^[0-9]{10,15}$', contact):
            raise ValidationError('Contact number must be 10-15 digits.')
        return contact


class CustomerMilkCategoryForm(forms.ModelForm):
    """Form for customer milk category."""
    class Meta:
        model = CustomerMilkCategory
        fields = ('animalname', 'milkprice', 'related_customer')
        widgets = {
            'animalname': forms.Select(attrs={'class': 'form-control'}),
            'milkprice': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'related_customer': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'animalname': 'Animal Name',
            'milkprice': 'Milk Price (per liter)',
            'related_customer': 'Customer',
        }

    def clean_milkprice(self):
        """Validate milk price is positive."""
        price = self.cleaned_data.get('milkprice')
        if price <= 0:
            raise ValidationError('Milk price must be greater than 0.')
        return price


class CustomerLedgerForm(forms.ModelForm):
    """Form for customer ledger entries."""
    class Meta:
        model = Customerledger
        fields = ('related_customer', 'related_milk_category', 'date', 'price', 'quantity', 'total')
        widgets = {
            'related_customer': forms.Select(attrs={'class': 'form-control'}),
            'related_milk_category': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'readonly': 'readonly'}),
        }

    def clean(self):
        """Perform cross-field validation."""
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        quantity = cleaned_data.get('quantity')
        
        if price is not None and quantity is not None:
            cleaned_data['total'] = price * quantity
        
        return cleaned_data

    def clean_price(self):
        """Validate price is positive."""
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise ValidationError('Price must be greater than 0.')
        return price

    def clean_quantity(self):
        """Validate quantity is positive."""
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise ValidationError('Quantity must be greater than 0.')
        return quantity