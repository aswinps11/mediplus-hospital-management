from django.shortcuts import render,redirect
from myapp.models import Doctor
from django.core.paginator import Paginator
from django.contrib import messages
from .models import ContactMessage,Newsletter,Appointment
from datetime import datetime

# Create your views here.
def index(request):
    return render(request,'frontend/index.html')

def contact(request):
    return render(request,'frontend/contact.html')

def blogs(request):
    return render(request,'frontend/blog-single.html')

def doctors_list(request):
    doc=Doctor.objects.all()
    return render(request,'frontend/doctors_list.html',{'doc':doc})
# def doctors_list(request):
#     doctors_list=Doctor.objects.all().order_by('-id')
#     paginator=Paginator(doctors_list,4)
    
#     page=request.GET.get('page')
#     doc=paginator.get_page(page)
#     return render(request,'frontend/doctors_list.html',{'doc':doc})

def doctors_details(request,id):
    doc=Doctor.objects.get(id=id)
    return render(request,'frontend/doctors_details.html',{'doc':doc})

def contact_submission(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        subject=request.POST.get('subject')
        message_text=request.POST.get('message')
        
        if not name or not email or not phone or not subject or not message_text:
            return render(request,'frontend/contact.html',{'error':'All fields are required'})
            # messages.error(request,'All fields are required')
            # return render(request,'frontend/contact.html')
        
        ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message_text,
        )
        return render(request,'frontend/contact.html',{'msg':'Your message has been sent successfully.'})
        
        # messages.success(request,"Your message has been sent successfully.")
        
        # return redirect('contact')
 
    return render(request,'frontend/contact.html')

        
# appoinment
# def book_appointment(request):
#     return render(request,'frontend/appointment.html')

# services
def services(request):
    return render(request,'frontend/services.html')

# about
def about(request):
    return render(request,'frontend/about.html')

# newsletter
def newsletter_subscribe(request):
    if request.method == 'POST':
        email=request.POST.get('email')

        if Newsletter.objects.filter(email=email).exists():
            messages.error(request,"Email already subscribed.")

        else:
            Newsletter.objects.create(email=email)
            messages.success(request,"Subscribed successfully.")

    return redirect(request.META.get("HTTP_REFERER"))

# for appoinment
def appointment(request):

    specializations = Doctor.objects.values_list("specialization", flat=True).distinct()

    name = email = phone = message = date = ""
    selected_specialization = None
    selected_doctor = None
    doctors = Doctor.objects.none()

    if request.method == "POST":

        # Get all form fields
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        date = request.POST.get("date")

        selected_specialization = request.POST.get("specialization")
        

        # Load doctors when department selected
        if selected_specialization:
            doctors = Doctor.objects.filter(specialization=selected_specialization)
        
        selected_doctor = request.POST.get("doctor")

       
        if selected_doctor and date:
            Appointment.objects.create(
                name=name,
                email=email,
                phone=phone,
                doctor=Doctor.objects.get(id=selected_doctor),
                date=datetime.strptime(date, "%m/%d/%Y").date(),
                message=message
            )
            messages.success(request, "Appointment booked successfully!")
            return redirect("appointment")

    context = {
        "specializations": specializations,
        "selected_specialization": selected_specialization,
        "doctors": doctors,
        "selected_doctor": selected_doctor,


        "name": name,
        "email": email,
        "phone": phone,
        "message": message,
        "date": date,
    }

    return render(request, "frontend/appointment.html", context)