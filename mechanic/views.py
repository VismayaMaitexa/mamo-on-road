from django.http import HttpResponseRedirect , HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import  authenticate,login
from django.shortcuts import render,redirect,reverse
from .import forms,models
from django.contrib.auth.models import Group
from . import forms  # Import your forms from the appropriate module
from django.shortcuts import get_object_or_404
from .models import Mechanic
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import Customer

# Create your views here.
def index(request):
    return render(request,'index.html')
def mechanicclick_view(request):
    return render(request,'mechanicclick.html')
def userclick_view(request):
    return render(request,'userclick.html')
    



def adminclick_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == 'Admin' and password == '12345':
            user = User.objects.filter(username=username).first()

            if user is None:
                # Create a new user if one does not exist
                user = User.objects.create_user(username=username, password=password)
                
            # Log in the user after creation or if they already existed
            login(request, user)
            return redirect('admin-home')
        else:
            # Invalid credentials
            return render(request, "adminclick.html", {'error_message': 'Invalid username or password'})

    return render(request, 'adminclick.html')


from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from . import forms  # Assuming your forms are in the same directory
from .models import Mechanic  # Assuming you have a Mechanic model

def mechanicregister_view(request):
    userForm = forms.MechanicUserForm()
    mechanicForm = forms.MechanicForm()

    if request.method == 'POST':
        userForm = forms.MechanicUserForm(request.POST)
        mechanicForm = forms.MechanicForm(request.POST, request.FILES)

        if userForm.is_valid() and mechanicForm.is_valid():
            try:
                # Save the user (hash the password)
                user = userForm.save(commit=False)
                user.set_password(user.password)
                user.save()

                # Save the mechanic data
                mechanic = mechanicForm.save(commit=False)
                mechanic.user = user

                # Retrieve the latitude and longitude from the form data
                latitude = request.POST.get('latitude')
                longitude = request.POST.get('longitude')

                # Ensure latitude and longitude are properly handled (e.g., convert to float)
                if latitude and longitude:
                    mechanic.latitude = float(latitude)
                    mechanic.longitude = float(longitude)

                mechanic.save()

                # Add the user to the 'MECHANIC' group
                my_mechanic_group, created = Group.objects.get_or_create(name='MECHANIC')
                my_mechanic_group.user_set.add(user)

                return redirect('mechaniclogin')  # Redirect the user to the mechanic login page

            except Exception as e:
                print("Error:", e)  # Print the error to the console or log it

        else:
            print("Form errors:", userForm.errors, mechanicForm.errors)  # Check for any form errors

    return render(request, 'mechanicregister.html', {'userForm': userForm, 'mechanicForm': mechanicForm})

def mechaniclogin_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('mechanicdashboard')  # Redirect to dashboard after successful login
        else:
            return render(request, 'mechaniclogin.html', {'error': 'Invalid credentials'})

    return render(request, 'mechaniclogin.html')

def userregister_view(request):
    userForm = forms.CustomerUserForm()
    customerForm = forms.CustomerForm()

    if request.method == 'POST':
        userForm = forms.CustomerUserForm(request.POST)
        customerForm = forms.CustomerForm(request.POST, request.FILES)

        if userForm.is_valid() and customerForm.is_valid():
            # Debug print statements
            print("Forms are valid, saving user and customer")

            # Save the user (hash the password)
            user = userForm.save(commit=False)
            user.set_password(user.password)
            user.save()

            # Save the mechanic data
            customer = customerForm.save(commit=False)
            customer.user = user
            customer.save()

            # Add the user to the 'MECHANIC' group
            my_customer_group, created = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group.user_set.add(user)

            # After successful registration, redirect to the mechanic login page
            return redirect('userlogin')  # This will redirect the user to the mechanic login page
        else:
            # Print form errors for debugging
            print("Form errors:", userForm.errors, customerForm.errors)

    return render(request, 'userregister.html', {'userForm': userForm, 'customerForm': customerForm})

#edit user

def adminlogin(request):
    return render(request,'admindashboard.html')

def userlogin_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('userdashboard')  # Redirect to dashboard after successful login
        else:
            return render(request, 'userlogin.html', {'error': 'Invalid credentials'})

    return render(request, 'userlogin.html')

#userdashboard page
def userdashboard_view(request):
    if request.user.is_authenticated:
        # Render the user's dashboard
        return render(request, 'userdashboard.html')
    else:
        # Redirect to login if the user is not authenticated
        return redirect('userlogin')

from django.shortcuts import render, get_object_or_404
from .models import Mechanic

def mechanicdashboard_view(request):
    # Retrieve the mechanic object associated with the logged-in user
    mechanic = get_object_or_404(Mechanic, user=request.user)
    
    # Pass the mechanic object to the template context
    return render(request, 'mechanicdashboard.html', {'mechanic': mechanic})

def admindashboard_view(request):
    return render(request,'admindashboard.html')


#mechanic_dashboard_page
from django.shortcuts import render
from .models import Request

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Request

@login_required
def assigned_requests(request):
    # Fetch only the requests assigned to the logged-in mechanic
    mechanic = get_object_or_404(Mechanic, user=request.user)
    
    # Pass the requests to the template
    return render(request, 'assigned_requests.html', {'mechanic': mechanic})

@login_required
def update_request_status(request, request_id):
    # Get the request object
    req = get_object_or_404(Request, id=request_id)

    # Check if the logged-in user is the assigned mechanic for this request
    if req.mechanic.user != request.user:
        messages.error(request, "You don't have permission to handle this request.")
        return redirect('assigned_requests')

    # Handle the form action (either accept or reject the request)
    action = request.POST.get('action')

    if action == 'accept':
        req.status = 'Accepted'
        messages.success(request, "Request has been accepted.")
    elif action == 'reject':
        req.status = 'Rejected'
        messages.success(request, "Request has been rejected.")
    
    req.save()

    return redirect('assigned_requests')

def mechanic_profile(request):
    return render(request,'mechanic_profile.html')
def log_out(request):
    return render(request,'index.html')

#user_dashboard_page
from geopy.distance import geodesic
from django.shortcuts import render
from . import models


def usermechanics_view(request):
    mechanics = models.Mechanic.objects.all()

    if request.method == 'POST':
        lat = float(request.POST.get('lat'))
        long = float(request.POST.get('long'))
        print(lat,long)

        nearby_mechanics = []
        max_distance_km = 10  

        for mechanic in mechanics:
            mechanic_lat = mechanic.lat
            mechanic_lon = mechanic.long

            user_location = (lat, long)
            mechanic_location = (mechanic_lat, mechanic_lon)

            distance = geodesic(user_location, mechanic_location).km

            if distance <= max_distance_km:
                nearby_mechanics.append(mechanic)

        return render(request, 'userdashboard_mechanics.html', {'mechanics': nearby_mechanics})

    return render(request, 'userdashboard_mechanics.html', {'mechanics': mechanics})



from django.shortcuts import render, get_object_or_404
from .models import Mechanic, Request
from django.contrib.auth.decorators import login_required


@login_required
def my_requests_view(request):  # request here is an HttpRequest object
    # Retrieve all mechanics
    mechanics = Mechanic.objects.all()

    # Fetch requests for the current logged-in user
    user_requests = Request.objects.filter(user=request.user)

    # Add the request status information to each mechanic
    for mechanic in mechanics:
        # Check if the current user has requested this mechanic
        request_exists = user_requests.filter(mechanic=mechanic).exists()
        # Add the status of the request if it exists
        mechanic.user_request_status = None
        if request_exists:
            # Fetch the first request made by the user to this mechanic
            request_obj = user_requests.filter(mechanic=mechanic).first()
            mechanic.user_request_status = request_obj.status  # Store the request status

        # Attach a flag to indicate if a request has been made by the user
        mechanic.request_exists = request_exists

    # Pass mechanics along with request status to the template
    return render(request, 'my_requests.html', {'mechanics': mechanics})

def user_profile(request):
    return render(request,'user_profile.html')
def user_feedback_view(request):
    return render(request, 'user_feedback.html')
def log_out(request):
    return render(request,'index.html')


#admin_login_page(dashboard)
from django.shortcuts import render
from .models import Request  # Assuming Request model exists

def emergency_requests_view(request):
    # Fetch all requests (including status) associated with mechanics and users
    requests = Request.objects.all()

    # Pass the requests to the template
    return render(request, 'emergency_requests.html', {'requests': requests})

def admin_feedback_view(request):
    return render(request,'admin_feedback.html')
def adminmechanics_view(request):
    mechanics = models.Mechanic.objects.all()
    print(mechanics)
    return render(request,'admindashboard-mechanics.html', {'mechanics': mechanics})


from django.shortcuts import get_object_or_404, redirect
from .models import Mechanic  # Adjust this to match your model name

def delete_mechanic_from_event_view(request, id):
    mechanic = get_object_or_404(Mechanic, id=id)
    mechanic.delete()
    return redirect('admindashboard_mechanics')  # Replace with the actual URL name you want to redirect to

from django.urls import path
from . import views

# views.py
from django.shortcuts import get_object_or_404, redirect
from .models import Mechanic

def update_mechanic(request, id):
    mechanic = get_object_or_404(Mechanic, id=id)

    if request.method == "POST":
        # Update related user details
        user = mechanic.user
        user.first_name = request.POST.get("firstname")
        user.last_name = request.POST.get("lastname")
        user.save()

        # Update mechanic details
        mechanic.address = request.POST.get("address")
        mechanic.mobile = request.POST.get("mobile")
        
        # Handle profile picture update
        if 'profile_pic' in request.FILES:
            mechanic.profile_pic = request.FILES['profile_pic']
        
        mechanic.save()

        return redirect("admindashboard_mechanics")  # Replace 'mechanics' with the name of the mechanics list URL pattern

    return render(request, "update_mechanic.html", {"mechanic": mechanic})



def user_view(request):
    users=models.Customer.objects.all()
    print(users)
    return render(request,'admindashboard-user.html',{'users':users})
def delete_user(request,id):
    customer=models.Customer.objects.get(id=id)
    customer.delete()
    return redirect('user')

from django.shortcuts import render, get_object_or_404, redirect
from .models import Customer  # Assuming the customer model is linked to User
from .forms import UserForm  # Use a form for the user details update


def update_user(request, id):
    customer = get_object_or_404(Customer, id=id)

    if request.method == "POST":
        # Update related user details
        user = customer.user
        user.first_name = request.POST.get("firstname")
        user.last_name = request.POST.get("lastname")
        user.save()

        # Update mechanic details
        customer.address = request.POST.get("address")
        customer.mobile = request.POST.get("mobile")
        
        # Handle profile picture update
        if 'profile_pic' in request.FILES:
            customer.profile_pic = request.FILES['profile_pic']
        
        customer.save()

        return redirect("user")  # Replace 'mechanics' with the name of the mechanics list URL pattern

    return render(request, "update_user.html", {"mechanic": customer})

def log_out(request):
    return render(request,'index.html')

#admin feedback
# views.py
from django.shortcuts import render
from .models import Feedback

def feedback_list(request):
    # Get all feedback, ordered by newest
    feedbacks = Feedback.objects.all().order_by('-created_at')
    
    return render(request, 'admin_feedback.html', {'feedbacks': feedbacks})

#user feedback

from django.shortcuts import render, redirect
from .forms import FeedbackForm


def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # Add the current user as the feedback submitter
            feedback = form.save(commit=False)
            feedback.user = request.user  # Set the user submitting the feedback
            feedback.save()
            return redirect('feedback_thank_you')  # Redirect after submission
        else:
            # Print form errors for debugging (optional)
            print(form.errors)
    else:
        form = FeedbackForm()
    print(form.fields['mechanic'].queryset)
    return render(request, 'user_feedback.html', {'form': form})


def feedback_thank_you(request):
    return render(request, 'feedback_thank_you.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import MechanicProfileForm
from .models import Mechanic

@login_required
def mechanic_profile(request):
    try:
        mechanic = Mechanic.objects.get(user=request.user)
    except Mechanic.DoesNotExist:
        mechanic = None
    
    return render(request, 'mechanic_profile.html', {'mechanic': mechanic})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import MechanicProfileForm
from .models import Mechanic

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import MechanicProfileForm
from .models import Mechanic


@login_required
def update_mechanic_profile(request):
    try:
        mechanic = Mechanic.objects.get(user=request.user)
    except Mechanic.DoesNotExist:
        mechanic = None

    if request.method == 'POST':
        form = MechanicProfileForm(request.POST, request.FILES, instance=mechanic)
        if form.is_valid():
            form.save()  # Save both the user and mechanic profile
            return redirect('mechanic_profile')  # Redirect after saving
        else:
            print(form.errors)  # Print form errors for debugging
    else:
        form = MechanicProfileForm(instance=mechanic)

    return render(request, 'update_mechanic_profile.html', {'form': form})




from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomerProfileForm
from .models import Customer

@login_required
def user_profile(request):
    try:
        customer = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        customer = None
    
    return render(request, 'user_profile.html', {'customer': customer})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomerProfileForm
from .models import Customer

@login_required
def update_user_profile(request):
    try:
        customer = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        customer = None

    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()  # Ensure username is saved in the User model as well
            return redirect('user_profile')  # Redirect back to the profile page
    else:
        form = CustomerProfileForm(instance=customer)

    return render(request, 'update_user_profile.html', {'form': form})


from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from .models import Feedback, Mechanic

def view_mechanic_feedbacks(request, mechanic_id):
    mechanic = get_object_or_404(Mechanic, id=mechanic_id)
    
    # Check if the logged-in user is the mechanic
    if request.user != mechanic.user:
        return HttpResponseForbidden("You are not allowed to view this feedback.")
    
    feedbacks = Feedback.objects.filter(mechanic=mechanic)
    
    return render(request, 'mechanic_feedback.html', {
        'mechanic': mechanic,
        'feedbacks': feedbacks
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Mechanic, Request  # Make sure to import your models
from django.contrib import messages

@login_required

def make_request(request, mechanic_id):
    # Get the mechanic by ID
    mechanic = get_object_or_404(Mechanic, pk=mechanic_id)

    # Check if the user has already made a request to this mechanic (optional)
    existing_request = Request.objects.filter(user=request.user, mechanic=mechanic).first()
    if existing_request:
        messages.error(request, "You have already made a request to this mechanic.")
        return redirect('userdashboard_mechanics')

    # Create a new request
    if request.method == 'POST':
        # Capture form data (including time)
        date = request.POST['date']
        time = request.POST['time']
        place = request.POST['place']
        issue = request.POST['issue']
        vehicle_type = request.POST['vehicle_type']
        contact_number = request.POST['contact_number']
        
        # Combine date and time into a datetime object
        from datetime import datetime
        date_time_str = f"{date} {time}"
        date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')

        # Create a new request with all necessary data
        new_request = Request(
            user=request.user,
            mechanic=mechanic,
            date_requested=date_time_obj,  # Save both date and time as a datetime
            place=place,
            issue=issue,
            vehicle_type=vehicle_type,
            contact_number=contact_number,
            status='Pending',  # You can set the initial status as 'Pending' or whatever you prefer
        )
        new_request.save()

        # Send a success message and redirect to the user's request page
        messages.success(request, f"Request has been sent to {mechanic.user.first_name} {mechanic.user.last_name}.")
        return redirect('my_requests')  # Redirect to the user's request page

    # If it's a GET request, just render the confirmation page or process any additional logic
    return render(request, 'make_request_confirmation.html', {'mechanic': mechanic})



## location based

def map(request):
    return render(request,'map.html')

def chatbot(request):
    return render(request,'chatbot.html')