from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from . models import *
from . forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from payment.views import *
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver 
import random
from datetime import datetime,timedelta
from numpy import random
# Create your views here.

def index(request):
    return render(request,'index.html')

def register(request):
    reg=False
    if request.method=='POST':
        user_form=UserForm(data=request.POST)
        profile_form=ProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            user.save()
            profile=profile_form.save(commit=False)
            profile.user=user
            profile.save()

            reg=True
            return redirect('user_login')
        else:
            HttpResponse("invalid form")
    else:
         user_form=UserForm()
         profile_form=ProfileForm()
    return render(request,'register.html',{'register':reg,'user_form':user_form,'profile_form':profile_form}) 
     


def user_login(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('dashboard'))
            else:
                return HttpResponse("Not active")
        else:
            return HttpResponse("Invalid username or password")
    else:
        
        return render(request,'login.html')




def dashboard(request):
    try:

        profile=Register.objects.get(user=request.user)
        return render(request,'dashboard.html',{'profile':profile})
    except:
        return render(request,'dashboard.html')
    
    

@login_required
def user_logout(request):
    logout(request)
    return redirect('index')





def change_password(request):
    if request.method=="POST":
        form=PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user=form.save()
            update_session_auth_hash(request,user)
            messages.success(request,"YOUR PASSWORD SUCCESSFULLY UPDATED")
            return render(request,'change_password.html')
        else:
            messages.error(request,"PLEASE CORRECT ERROR")
    else:
        form=PasswordChangeForm(request.user)
    return render(request,'change_password.html',{"form":form})


def update_profile(request):
    if request.method=="POST":
        update_form=UpdateForm(request.POST,instance=request.user)
        update_profile_form=UpdateProfileForm(request.POST,instance=request.user)
        #print(request.user.register)
        if update_form.is_valid() and update_profile_form.is_valid():
            update_form.save()
            update_profile_form.save()
            messages.success(request,f'Your Account has been Updated')
            return redirect('dashboard')
    else:
        update_form=UpdateForm(instance=request.user)
        update_profile_form=UpdateProfileForm(instance=request.user)
    context={
        'update_form':update_form,
        'update_profile_form':update_profile_form
    }
    return render(request,'update_profile.html',context)


def complaint(request):
    if request.method=="POST":
        complaint_form=ComplaintForm(request.POST)
        if complaint_form.is_valid():
            cp=Complaints(user=request.user,content=complaint_form.cleaned_data['content'],reason=complaint_form.cleaned_data['reason'])
            cp.save()
            return render(request,'complaint.html',{'msg':'successfully added complaint'})
        else:
            return HttpResponse("Invalid form")
    complaint_form=ComplaintForm()
    return render(request,'complaint.html',{'form':complaint_form})


def feedback(request):
    if request.method=="POST":
        feedback_form=FeedbackForm(request.POST)
        if feedback_form.is_valid():
            cp=Feedback(user=request.user,content=feedback_form.cleaned_data['content'])
            cp.save()
            return render(request,'feedback.html',{'msg':'successfully added complaint'})
        else:
            return HttpResponse("Invalid form")
    feedback_form=FeedbackForm()
    return render(request,'feedback.html',{'feedbackform':feedback_form})


def requirement(request):
    staff=Register.objects.filter(user_type='staff')
    #Sprint(staff)
    a=[]
    for i in staff:
        allotted_requirement=Requiremt.objects.filter(staff=i,status='notfinished')
        for j in allotted_requirement:
            a.append(j.percentage)
    print(max(a))
    requirements=Requiremt.objects.filter(status='notfinished',percentage=max(a))
    staffs=[]
    for ij in requirements:
        #print(ij.staff)
        staffs.append(ij.staff)
    #print(staffs)
    random_staff = random.choice(staffs)
    print(random_staff)   
    if request.method=="POST":
        requirement_form=RequirementForm(request.POST)
        if requirement_form.is_valid():
            requirements=Requiremt(user=request.user,staff=random_staff,description=requirement_form.cleaned_data['description'],square_feet=requirement_form.cleaned_data['square_feet'])
            print(requirements.square_feet)
            j=requirements.square_feet
            price=PriceTable.objects.all()
            
            for i in price:
                if j>=i.base and j<=i.upper:
                    print(i.price)
                    break
            print(i)
            requirements.message=i
            requirements.save()
            return render(request,'requirement.html',{'msg':'Requirement added Successfully'})
        else:
            return HttpResponse("Invalid Form")
    requirement_form=RequirementForm()
    return render(request,'requirement.html',{'requirement_form':requirement_form})


def requirement_view(request):
    print(request.user)
    User_instance=request.user.id
    employee_work=Requiremt.objects.filter(staff__user__id=User_instance).order_by('-date')
    user_requirement=Requiremt.objects.filter(user=request.user).order_by('-date')
    print(user_requirement)
    print(employee_work)
    return render(request,'view_requirements.html',{'list':employee_work,'user_requirement':user_requirement})


def update_requirement(request,requirement_id):
    requirement=Requiremt.objects.get(id=requirement_id)
    print(requirement)
    update_requirement_form=UpdateRequirementForm(instance=requirement)
    if request.method=="POST":
        update_requirement_form=UpdateRequirementForm(request.POST,request.FILES,instance=requirement)
        update_requirement_form.save()
        return redirect('requirement_view')
    return render(request,'update_requirements.html',{'update_requirement_form':update_requirement_form})



def view_complaints(request):
    complaints=Complaints.objects.all().order_by('date')
    return render(request,'view_complaints.html',{'complaints':complaints})


def chat(request):
    staff_chat=Chat.objects.filter(user=request.user).order_by('date')
    print(staff_chat)
    if request.method=="POST":
        chat_form=ChatForm(request.POST)
        if chat_form.is_valid():
            cp=Chat(user=request.user,content=chat_form.cleaned_data['content'])
            cp.save()

            
            return render(request,'chat.html',{'msg':'successfully added complaint'})
        else:
            return HttpResponse("Invalid form")
    chat_form=ChatForm()
    return render(request,'chat.html',{'chat_form':chat_form,'staff_chat':staff_chat})


def admin_chat(request):
    print(request.user)
    User_instance=request.user.id
    admin_chat=Chat.objects.filter(staff__user__id=User_instance).order_by('date')
    
    print(admin_chat)
    
    return render(request,'chat_from_admin.html',{'admin_chat':admin_chat})



def leave(request):
    if request.method=="POST":
        leave_form=LeaveForm(request.POST)
        if leave_form.is_valid():
            lv=Leave(user=request.user,startdate=leave_form.cleaned_data['startdate'],days=leave_form.cleaned_data['days'],reason=leave_form.cleaned_data['reason'])
            lv.save()

            
            return render(request,'leave_form.html',{'msg':'successfully submitted leave'})
        else:
            return HttpResponse("Invalid form")
    leave_form=LeaveForm()
    return render(request,'leave_form.html',{'leave_form':leave_form})


def leave_list(request):
    view_leave=Leave.objects.filter(user=request.user)
    return render(request,'view_leave.html',{'view_leave':view_leave})



def previous_work(request):
    previous_work=Requiremt.objects.all().order_by('date')
    return render(request,'previous_work.html',{'previous_work':previous_work})

def profile(request):
    staff_list=Register.objects.filter(user_type='staff')
    print(staff_list)
    return render(request,'all_staff_view.html',{'staffs':staff_list})









           

