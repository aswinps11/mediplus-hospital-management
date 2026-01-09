from django.urls import path
from . import views

urlpatterns=[
    
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('logout/',views.logout,name='logout'),
    path('add/',views.add_doctor,name='add_doctor'),
    path('edit/<int:id>/',views.edit_list,name='edit_list'),
    path('list/',views.doctor_list,name='doctor_list'),
    path('delete/<int:id>/',views.delete_doctor,name='delete_doctor'),
    path('doctor/<int:id>/',views.doctor_details,name='doctor_details'),
    path('contact-messages/',views.contact_message_list,name='contact_list'),
    path('newsletter/',views.newsletters,name='newsletters'),
    path('newsletter_export',views.export_newsletter,name='export_newsletter'),
    path('contact__export',views.export_contact,name='export_contact'),
    path('appointments/',views.appointment_list,name='appointment_list'),
    
] 