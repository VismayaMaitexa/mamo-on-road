from django import forms
from django.contrib.auth.models import User
from . import models

class CustomerUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets={
            'password': forms.PasswordInput()
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model=models.Customer
        fields=['address','mobile','profile_pic']        
        

class MechanicUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets={
            'password': forms.PasswordInput()
        }

from django import forms
from .models import Mechanic


class MechanicForm(forms.ModelForm):
    class Meta:
        model = Mechanic
        fields = ['address', 'mobile', 'profile_pic', 'working_time_from', 'working_time_to', 'vehicle_type', 'verification_document','lat','long']
    
    # Add hidden input fields for latitude and longitude
    # lat = forms.FloatField(widget=forms.HiddenInput(), required=False)
    # long = forms.FloatField(widget=forms.HiddenInput(), required=False)

from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

        
from django import forms
from .models import Feedback, MechanicProfile
from django import forms
from .models import Feedback, MechanicProfile

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['mechanic', 'feedback_text', 'rating']  # Include mechanic field
        widgets = {
            'feedback_text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter your feedback here...'}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }
    
    mechanic = forms.ModelChoiceField(
        queryset=models.Mechanic.objects.all(),
        empty_label="Select Mechanic",
        widget=forms.Select(attrs={'class': 'mechanic-select'})
    )
    

from django import forms
from .models import MechanicProfile

class MechanicProfileForm(forms.ModelForm):
    class Meta:
        model = MechanicProfile
        fields = ['username', 'address', 'mobile', 'profile_pic', 'verification_document', 
                  'working_time_from', 'working_time_to', 'vehicle_type']

    username = forms.CharField(max_length=150, required=True)

    def save(self, commit=True):
        # Get the associated mechanic profile (not committing yet)
        mechanic_profile = super().save(commit=False)
        
        # Get the associated User object
        user = mechanic_profile.user
        
        # If the username is being updated, assign the new value to the User model
        if 'username' in self.cleaned_data:
            user.username = self.cleaned_data['username']
        
        if commit:
            user.save()  # Save the updated User model (username)
            mechanic_profile.save()  # Save the MechanicProfile model with updated data
        return mechanic_profile


from django import forms
from .models import Customer
from django.contrib.auth.models import User

class CustomerProfileForm(forms.ModelForm):
    # Add a username field for editing
    username = forms.CharField(max_length=150, required=True)

    class Meta:
        model = Customer
        fields = ['username', 'address', 'mobile', 'profile_pic']  # Include username here

    def save(self, commit=True):
        # Get the associated user model from the customer instance
        customer = super().save(commit=False)
        user = customer.user  # Get the associated User object

        # If the username is being updated, assign the new value to the User model
        if 'username' in self.cleaned_data:
            user.username = self.cleaned_data['username']
        
        if commit:
            user.save()  # Save the updated user model
            customer.save()  # Save the customer profile with updated data
        return customer


