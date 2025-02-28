from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# mechanic/models.py
from django.contrib.auth.models import User
from django.db import models


class Mechanic(models.Model):
    VEHICLE_TYPE_CHOICES = [
        ('two wheeler', 'Two Wheeler'),
        ('three wheeler', 'Three Wheeler'),
        ('four wheeler', 'Four Wheeler'),
        ('other', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    address = models.CharField(max_length=255)
    mobile = models.CharField(max_length=15)
    
    # Add default value to working_time_from
    working_time_from = models.TimeField(default="09:00")  # Default value for working_time_from
    working_time_to = models.TimeField(default="18:00")
    
    # Adding vehicle_type field
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE_CHOICES, default='other')
    verification_document = models.FileField(upload_to='verification_documents/', blank=True, null=True)
    lat = models.FloatField(null=True,blank=True)
    long = models.FloatField(null=True,blank=True)
    
    def __str__(self):
        return self.user.username


class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic=models.ImageField(upload_to='profile_pic/CustomerProfilePic/',null=True,blank=True)
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE,null=True)  # This creates a relation to Mechanic
    address=models.CharField(max_length=40)
    mobile=models.CharField(max_length=20,null=False)


from django.db import models
from django.contrib.auth.models import User

class MechanicProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    mobile = models.CharField(max_length=20)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    verification_document = models.FileField(upload_to='verification_docs/', blank=True, null=True)
    working_time_from = models.TimeField(blank=True, null=True)
    working_time_to = models.TimeField(blank=True, null=True)
    vehicle_type = models.CharField(max_length=50, choices=[
        ('two wheeler', 'Two wheeler'),
        ('three wheeler', 'Three wheeler'),
        ('four wheeler', 'Four wheeler'),
        ('other', 'Other')
    ], blank=True, null=True)

    def __str__(self):
        return self.user.username


    
    # models.py
from django.db import models
from django.contrib.auth.models import User

class Feedback(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]  # 1 to 5 star rating
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who gave the feedback
    mechanic = models.ForeignKey(Mechanic, null=True, blank=True, on_delete=models.SET_NULL)  # Mechanic receiving feedback
    feedback_text = models.TextField()  # Feedback content
    rating = models.IntegerField()  # Rating from 1 to 5 (or any range)
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the feedback was created

    def __str__(self):
        return f"Feedback from {self.user.username} for {self.mechanic.user.username}"


# mechanic/models.py

from django.db import models
from django.contrib.auth.models import User

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    mobile = models.CharField(max_length=20)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username

from django.db import models
from django.contrib.auth.models import User
from .models import Mechanic

class Request(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE)
    date_requested = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    place = models.CharField(max_length=255)
    issue = models.CharField(max_length=255)
    vehicle_type = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return f"Request from {self.user.username} to {self.mechanic.user.username} - Status: {self.status}"
