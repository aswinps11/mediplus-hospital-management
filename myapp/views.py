from django.shortcuts import render,redirect
from .models import UserData,Doctor
from django.contrib import messages
from django.core.paginator import Paginator
from frontend.models import ContactMessage,Newsletter,Appointment
from django.http import HttpResponse
import csv
from openpyxl import Workbook 
from django.db.models import Q

# Create your views here.


# Register
def register(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        
        if UserData.objects.filter(name=name).exists():
            return render(request,'register.html',{'error':'Username already exists.'})
        
        if UserData.objects.filter(email=email).exists():
            return render(request,'register.html',{'error':'email already exists.'})
        
        user=UserData(name=name,email=email,password=password)
        user.save()
        
        return render(request,'login.html',{'msg':'User successfully registered.'})
    
    return render(request,'register.html')


# Login
def login(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        
        try:
            user=UserData.objects.get(email=email,password=password)
            request.session['user_id']=user.id
            request.session['user_name']=user.name
            request.session['user_email']=user.email
            return redirect('dashboard')
        
        except UserData.DoesNotExist:
            return render(request,'login.html',{'error':'Invalid email or password.'})
    
    return render(request,'login.html')


def dashboard(request):
    if request.method == 'POST':
        query=request.GET.get('search','')
    
        doctor_list=Doctor.objects.filter(
            Q(name__icontains=query) | Q(specialization__icontains=query)).order_by('-id')
        
        paginator=Paginator(doctor_list,4)
        page=request.GET.get('page')
        doc=paginator.get_page(page)
        return render(request,'doctor_list.html',{'doc':doc,'search':query})

    if 'user_id' not in request.session:
        return redirect('login')
    
    name=request.session.get('user_name')
    return render(request,'dashboard.html',{'name':name})

    
        

def logout(request):
    request.session.flush()
    return render(request,'login.html',{'msg':'You have been logged out successfully.'})



# doctors

# create
def add_doctor(request):
    if request.method=='POST':
        name=request.POST.get('name')
        specialization=request.POST.get('specialization')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        address=request.POST.get('address')
        image=request.FILES.get('image')
        available_daysandtime=request.POST.get('available_daysandtime')
        biography=request.POST.get('biography')
        education=request.POST.get('education')
        
        
        Doctor.objects.create(name=name,specialization=specialization,image=image,available_daysandtime=available_daysandtime,email=email,phone=phone,address=address,biography=biography,education=education)
        
        messages.success(request,'Added Successfully')
        return redirect('doctors_list')
    return render(request,'add_doctor.html')
        
# Edit
def edit_list(request,id):
    doc=Doctor.objects.get(id=id)
    if request.method=='POST':
        doc.name=request.POST.get('name')
        doc.specialization=request.POST.get('specialization')
        doc.image=request.FILES.get('image')
        doc.available_days=request.POST.get('available_days')
        doc.available_time=request.POST.get('available_time')
        
        doc.save()
        
        messages.success(request,'Edited Successfully')
        return redirect('doctors_list')
    
    return render(request,'edit_doctor.html',{'doc':doc})


# View
# def doctors_list(request):
#     doc=Doctor.objects.all()
#     return render(request,'doctors_list.html',{'doc':doc})

def doctor_list(request):
    t_search=request.GET.get('t_search','')
    d_search=request.GET.get('d_search','')
    
    query=t_search or d_search
    
    doctor_list=Doctor.objects.filter(
        Q(name__icontains=query) | Q(specialization__icontains=query)).order_by('-id')
    
    paginator=Paginator(doctor_list,4)
    page=request.GET.get('page')
    doc=paginator.get_page(page)
    return render(request,'doctor_list.html',{'doc':doc,'d_search':d_search,'t_search':t_search})
    

# delete
def delete_doctor(request,id):
    doc=Doctor.objects.get(id=id)
    doc.delete()
    
    return redirect('doctors_list')
    

# details
def doctor_details(request,id):
    doc=Doctor.objects.get(id=id)
    return render(request,'doctor_details.html',{'doc':doc})


# contact us- frontend
def contact_message_list(request):
    message_list=ContactMessage.objects.all().order_by('-created_at')
    return render(request,'contact_list.html',{'message':message_list})
    
    
# newsletter
def  newsletters(request):
    subscribers=Newsletter.objects.all().order_by('-subscribed_at')
    return render(request,'newsletter.html',{'subscribers':subscribers})
    
    
# newsletter export
def export_newsletter(request):
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment:filename="newsletter.csv"'
    
    writer=csv.writer(response)
    writer.writerow(['Email','Subscribed Date'])
    
    for n in Newsletter.objects.all():
        writer.writerow([n.email,n.subscribed_at])
        
    return response


#  contact export
def export_contact(request):
    wb=Workbook()
    ws=wb.active
    ws.title="Contact Messages"

    ws.append(['Name','Email','Phone','Message','Created At'])

    for m in ContactMessage.objects.all():
        ws.append([
            m.name,
            m.email,
            m.phone,
            m.message,
            m.created_at.strftime("%Y-%m-%d %H:%M")
        ])  

    response=HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response['Content-Disposition']='attachment; filename="contact_message.xlsx"'

    wb.save(response)
    return response

# appointment list
def appointment_list(request):
    appointment_list=Appointment.objects.all().order_by('-created_at')
    return render(request,'appointment_list.html',{'appointment':appointment_list})