from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('register', views.index),
    # html page
    path('mechanicclick', views.mechanicclick_view, name='mechanicclick'),
    path('userclick', views.userclick_view, name='userclick'),
    path('adminclick', views.adminclick_view, name='adminclick'),
    # mechanicclick_register
    path('mechanicregister/', views.mechanicregister_view, name='mechanicregister'),
    path('mechaniclogin/', views.mechaniclogin_view, name='mechaniclogin'),
    path('mechanicdashboard/', views.mechanicdashboard_view, name='mechanicdashboard'),
    # userclick_register
    path('userregister/', views.userregister_view, name='userregister'),
    path('userlogin/', views.userlogin_view, name='userlogin'),
    path('userdashboard/', views.userdashboard_view, name='userdashboard'),

    path('admindashboard', views.admindashboard_view, name='admindashboard'),
    path('admin-home', views.adminlogin, name='admin-home'),
    # admin_login_page
    path('emergency_requests/', views.emergency_requests_view, name='emergency_requests'),  # Fixed the name here
    path('admin_feedback/',views.admin_feedback_view,name='admin_feedback'),
    path('admin/mechanics/', views.adminmechanics_view, name='admindashboard_mechanics'),
    path('mechanicdlt/<int:id>', views.delete_mechanic_from_event_view, name='delete-mechanic'),
    path('update_mechanic/<int:id>/', views.update_mechanic, name='update_mechanic'),
    path('user/', views.user_view, name='user'),
    path('update_user/<int:id>/', views.update_user, name='update_user'),
    path('delete_user/<int:id>/', views.delete_user, name='delete-user'),
    path('log/',views.log_out,name='logout'),
    # user login page
    path('userdashboard', views.userdashboard_view, name='userdashboard'),
    # mechanic dashboard page
    path('assigned_requests/', views.assigned_requests, name='assigned_requests'),
    path('mechprofile/', views.mechanic_profile, name='mechanic_profile'),
    path('logt/', views.log_out, name='logout'),
    # user dashboard page
    path('user/mechanics/', views.usermechanics_view, name='userdashboard_mechanics'),
    path('my_req/', views.my_requests_view, name='my_requests'),
    path('user/profile/', views.user_profile, name='user_profile'),
    path('user/feedback/', views.user_feedback_view, name='user_feedback'),
    path('logt/', views.log_out, name='logout'),

    path('feedback/', views.submit_feedback, name='user_feedback'),
    path('admin/feedback/', views.feedback_list, name='admin_feedback'),
    path('feedback/thank-you/', views.feedback_thank_you, name='feedback_thank_you'),

    path('mechanic/profile/', views.mechanic_profile, name='mechanic_profile'),
    path('mechanic/profile/update/', views.update_mechanic_profile, name='update_mechanic_profile'),
    path('user/profile/', views.user_profile, name='user_profile'),
    path('user/profile/update/', views.update_user_profile, name='update_user_profile'),

    path('mechanic_feedback/<int:mechanic_id>/', views.view_mechanic_feedbacks, name='mechanic_feedback'),
    path('make_request/<int:mechanic_id>/', views.make_request, name='make_request'),
    path('update_request_status/<int:request_id>/', views.update_request_status, name='update_request_status'),
    path('map/', views.map, name='map'),
    path('chatbot/', views.chatbot, name='chatbot'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)