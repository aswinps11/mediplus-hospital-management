from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name='index'),
    path('contact/',views.contact,name='contact'),
    path('blogs/',views.blogs,name='blogs'),
    path('doctors/',views.doctors_list,name='doctors_list'),
    path('details/<int:id>/',views.doctors_details,name='doctors_details'),
    path('contact-submission/',views.contact_submission,name='contact'),
    # path('appointment/',views.book_appointment,name='appointment'),
    path('services/',views.services,name='services'),
    path('about/',views.about,name='about'),
    path('newsletter/',views.newsletter_subscribe,name='newsletter_subscribe'),
    path('appointment/',views.appointment,name='appointment'),
]