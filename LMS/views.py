from django.shortcuts import render
from django.urls import reverse_lazy
from .models import *
from django.shortcuts import get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from .forms import *
from django.utils import timezone
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.generic.edit import UpdateView


from django.shortcuts import render
from django.http import JsonResponse
import os
from .models import Course_Content

















def get_suggestions(request):
    input_text = request.GET.get('input', '')
    suggestions_file_path = os.path.join(os.path.dirname(__file__), 'states.txt')
   
    with open(suggestions_file_path, 'r') as f:
        suggestions = [line.strip() for line in f if line.strip().lower().startswith(input_text.lower())]

    return JsonResponse({'suggestions': suggestions})


from django.http import HttpResponse
import os
from django.conf import settings

def get_admin_suggestions(request):
    return render(request, 'suggestions/departments.txt')

# views.py


    # file_path = os.path.join(settings.BASE_DIR, 'templates', 'states.txt')
    # with open(file_path, 'r') as file:
    #     suggestions = file.read()
    # return HttpResponse(suggestions)




def states(request):
    return render(request, 'suggestions/states.txt')



def department(request):
    return render(request, 'suggestions/departments.txt')




def LGA(request):
    return render(request, 'suggestions/LGA.txt')



def institution(request):
    return render(request, 'suggestions/institution.txt')


def index(request):
    sponsors = SponsorProfile.objects.all()[0:15]
    courses = Course.objects.all()[0:6]
    context = {
        'sponsors': sponsors,
        'courses' : courses
    }
    return render(request, 'home/home.html', context)



@login_required(login_url="signin")
def grant(request, courses):
    profile = StudentProfile.objects.get(user = request.user)
    course = get_object_or_404(Course, title = courses)


    initial_data = {'student': profile.id, 'course_title': course}  

    if request.method == "POST":
        form = GrantForm(request.POST)
        if form.is_valid():
            student= profile
            date = form.cleaned_data.get("date")
            description = form.cleaned_data.get("description")
            course_title = course
            form.save()
            messages.success(request, 'Request for Grant sucessful')
   
    form = GrantForm(initial=initial_data)
    context = {
        "form" : form, 
        "profile" : profile, 

        } 
    return render(request, 'dashboard/grant.html', context)






@login_required(login_url="signin")
def sponsor_payment(request):
    
    profile = SponsorProfile.objects.get(user = request.user)
    base_url = request.build_absolute_uri('/')


    context = {
        'profile' : profile,
        'base_url' : base_url,
    }

    return render(request, 'dashboard/sponsor_payment.html', context)





@login_required(login_url="signin")
def courses(request):
    profile = StudentProfile.objects.get(user = request.user)
    free_courses = Course.objects.filter(course = profile.course)
    general_courses = Course.objects.filter(course = 'general')


    context = {
        "profile" : profile, 
        "courses" : free_courses,
        "general_courses" : general_courses,
        } 
    return render(request, 'dashboard/courses.html', context)




@login_required(login_url="signin")
def course_content(request, courses):
    # course = get_object_or_404(Course, title = courses)
    course_content = Course_Content.objects.get(title = courses)
    profile = StudentProfile.objects.get(user = request.user)
    courses = Course_Content.objects.filter(course = course_content.course)




  
    context = {
    "profile" : profile, 
    "course_content" : course_content,
    "courses" : courses,

    } 
    return render(request, 'dashboard/course_content.html', context)


    

    
@login_required(login_url="signin")
def course_video(request, courses):
    course = get_object_or_404(Course, title = courses)
    course = get_object_or_404(Course, title = courses)
    profile = StudentProfile.objects.get(user = request.user)
    print(course.title)



    grant = Grant.objects.filter(student = profile).filter(approved = True).filter(course_title = course.title)

    if grant:    
        student_profile, created = StudentProfile.objects.get_or_create(user = request.user)
            
        if course not in student_profile.purchased_courses.all():
            student_profile.purchased_courses.add(course)
            messages.success(request, 'grant Approved')


    if course.is_purchased(request.user) or course.paid == False:
        profile = StudentProfile.objects.get(user = request.user)
        course_video = Course.objects.get(title = courses)
        course_content = Course_Content.objects.filter(course = course)

        try:
            schedule = Course_Schedule.objects.get( course_title = course_video)

            context = {
                "profile" : profile, 
                "course_video" : course_video,
                "schedule" : schedule,
                "course_content" : course_content,
                } 
            return render(request, 'dashboard/course_video.html', context)
        except:
            context = {
            "profile" : profile, 
            "course_video" : course_video,
             "course_content" : course_content,

            } 
            return render(request, 'dashboard/course_video.html', context)

    else:
        return redirect('course_payment', courses = course.title)
    



@login_required(login_url="signin")

def confirm_course_payment(request, courses):
    course = get_object_or_404(Course, title = courses)
    student_profile, created = StudentProfile.objects.get_or_create(user = request.user)
        
    if course not in student_profile.purchased_courses.all():
        student_profile.purchased_courses.add(course)
        messages.success(request, 'Payment successful')
    else:
        messages.error(request, 'You have registered this course')

           
    return redirect('dashboard')




@login_required(login_url="signin")
def schedule_link(request, courses):
    course_content = Course_Content.objects.get(title = courses)
    schedule = Course_Schedule.objects.get(course_content = course_content)
    course = get_object_or_404(Course, title = schedule.course_title)
    if course.is_purchased(request.user) :
        profile = StudentProfile.objects.get(user = request.user)
        course_schedule = get_object_or_404(Course_Schedule, course_content = schedule.course_content)
        context = {
            "profile" : profile, 
            "course_schedule" : course_schedule, 
            } 
        
        return render(request, 'dashboard/schedule_link.html', context)
    

    elif schedule.paid == False:
        profile = StudentProfile.objects.get(user = request.user)
        course_schedule = get_object_or_404(Course_Schedule, course_content = schedule.course_content)
        context = {
            "profile" : profile, 
            "course_schedule" : course_schedule, 
            } 
        
        return render(request, 'dashboard/schedule_link.html', context)

    else:
        messages.error(request, 'Oops You have not registered for that course!')
        return redirect('com_schedule')


@login_required(login_url="signin")
def course_payment(request, courses):
    course = get_object_or_404(Course, title = courses)
    profile = StudentProfile.objects.get(user = request.user)
    print(course.title)



    grant = Grant.objects.filter(student = profile).filter(approved = True).filter(course_title = course.title)

    if grant:    
        student_profile, created = StudentProfile.objects.get_or_create(user = request.user)
            
        if course not in student_profile.purchased_courses.all():
            student_profile.purchased_courses.add(course)
            messages.success(request, 'grant Approved')



    base_url = request.build_absolute_uri('/')
    course = Course.objects.get(title = courses)
    try:
        schedule = get_object_or_404(Course_Schedule, course_title = course)
        context = {
            'profile' : profile,
            'base_url' : base_url,
            'course' : course,
            'schedule' : schedule
            # 'pk' : pk
        }

        return render(request, 'dashboard/course_payment.html', context)
    except:

        # print("00000000000000000 :", pk)

        context = {
            'profile' : profile,
            'base_url' : base_url,
            'course' : course,
            # 'pk' : pk
        }

        return render(request, 'dashboard/course_payment.html', context)






@login_required(login_url="signin")
def student_schedule(request):


    profile = StudentProfile.objects.get(user = request.user)
    base_url = request.build_absolute_uri('/')
    com_date = timezone.datetime.now()
    schedules = Course_Schedule.objects.filter(date__gt = com_date).filter(course_of_study = profile.course)
    general = Course_Schedule.objects.filter(date__gt = com_date).filter(course_of_study = 'general')

    context = {
        'schedules' : schedules,
        'general' : general,
        'profile' : profile,
    }

    return render(request, 'dashboard/schedule.html', context )











@login_required(login_url="signin")
def com_schedule(request):
    profile = StudentProfile.objects.get(user = request.user)
    base_url = request.build_absolute_uri('/')
    com_date = timezone.datetime.now()
    schedules = Course_Schedule.objects.filter(date__lt = com_date).filter(course_of_study =  profile.course) #created time is lesser than now, meaning the created time has passed
    general = Course_Schedule.objects.filter(date__lt = com_date).filter(course_of_study = 'general')

    context = {
        'schedules' : schedules,
        'general' : general,
        'profile' : profile,
    }

    return render(request, 'dashboard/com_schedule.html', context )













def get_filtered_course_content(request):
    course_title_id = request.GET.get('course_title_id')

    # Filter course content based on the selected course title ID
    if course_title_id:
        course_content = Course_Content.objects.filter(course=course_title_id)
        data = [{'id': content.id, 'name': content.title} for content in course_content]
    else:
        data = []

    return JsonResponse(data, safe=False)



def get_course_of_study(request):
    course_title_id = request.GET.get('course_title_id')
    course = Course.objects.filter(id=course_title_id).first()
    course_of_study = course.course if course else ''
    paid = course.paid if course else ''
    return JsonResponse({'course_of_study': course_of_study, 'paid':paid})









@login_required(login_url="signin")
def course_schedule(request):
    profile = FacilitatorProfile.objects.get(user = request.user)
    com_date = timezone.datetime.now()
    schedules = Course_Schedule.objects.filter(date__gt = com_date)
    
    
    initial_data = {'facilitator': profile.id}  

    if request.method == "POST":
        form = CourseScheduleForm(request.POST)
        if form.is_valid():
            course_title = form.cleaned_data.get("course_title")
            course_content = form.cleaned_data.get("course_content")
            date = form.cleaned_data.get("date")
            duration = form.cleaned_data.get("duration")
            course_of_study = form.cleaned_data.get("course_of_study")
            paid = form.cleaned_data.get("paid")
            form.save()
            messages.success(request, 'Course Schedule has been Added')



   
    form = CourseScheduleForm(initial=initial_data)

    context = {
        "form" : form, 
        "profile" : profile, 
        "schedules" : schedules, 
        "course_video" : course_video,
        } 
    return render(request, 'dashboard/course_schedule.html', context)




@login_required(login_url="signin")
def com_course_schedule(request):
    profile = FacilitatorProfile.objects.get(user = request.user)
    com_date = timezone.datetime.now()
    schedules = Course_Schedule.objects.filter(date__lt = com_date)
    
    
    initial_data = {'facilitator': profile.id}  

    if request.method == "POST":
        form = CourseScheduleForm(request.POST)
        if form.is_valid():
            course_title = form.cleaned_data.get("course_title")
            course_content = form.cleaned_data.get("course_content")
            date = form.cleaned_data.get("date")
            duration = form.cleaned_data.get("duration")
            course_of_study = form.cleaned_data.get("course_of_study")
            form.save()
            messages.success(request, 'Course Schedule has been Added')
   


    form = CourseScheduleForm(initial=initial_data)
    context = {
        "form" : form, 
        "profile" : profile, 
        "schedules" : schedules, 
        "course_video" : course_video,
        } 
    

    return render(request, 'dashboard/com_course_schedule.html', context)









class UpdateSchedule(UpdateView):
    model = Course_Schedule
    fields = ['link']
    template_name = 'dashboard/course_schedule_update.html'
    success_url = reverse_lazy('com_course_schedule')








@login_required(login_url="signin")
def dashboard(request):
    if request.user.is_student == True:
        profile = StudentProfile.objects.get(user = request.user)
        course = Course.objects.count
        return render(request, 'dashboard/index.html', context = {"profile" : profile, 'count': course})

    elif request.user.is_facilitator == True:
        profile = FacilitatorProfile.objects.get(user = request.user)
        return render(request, 'dashboard/index.html', context = {"profile" : profile})

    elif request.user.is_sponsor == True:
        profile = SponsorProfile.objects.get(user = request.user)
        return render(request, 'dashboard/index.html', context = {"profile" : profile})

        
        
    return render(request, 'dashboard/index.html')




@login_required(login_url="signin")
def sponsor(request):
    profile = SponsorProfile.objects.get(user = request.user)
    
    context = {
        "profile" : profile, 

        } 
    return render(request, 'dashboard/sponsor.html', context)





@login_required(login_url="signin")
def delete_course_schedule(request, pk):
    course_schedule = Course_Schedule.objects.get(id = pk)
    course_schedule.delete()
    messages.success(
        request, "Course Schedule has been Deleted !"
        )
    return redirect("course_schedule")














@login_required(login_url="signin")
def sponsor_update_profile(request):
    profile = get_object_or_404(SponsorProfile, user = request.user)

    if request.method == 'POST':
        profile_form = SponsorProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('sponsor_profile')
    else:
        profile_form = SponsorProfileForm(instance=profile)

        
            
    user_profile = SponsorProfile.objects.get(user = request.user)
    
    context = {
        'profile': user_profile,
        'form': profile_form
    }


    return render(request, "dashboard/sponsor_profile.html", context)


@login_required(login_url="signin")
def student_update_profile(request):
    profile = get_object_or_404(StudentProfile, user = request.user)

    if request.method == 'POST':
        profile_form = StudentProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('student_profile')
    else:
        profile_form = StudentProfileForm(instance=profile)

        
            
    user_profile = StudentProfile.objects.get(user = request.user)
    
    context = {
        'profile': user_profile,
        'form': profile_form
    }

    # return render(request, "profile.html", context)

    return render(request, "dashboard/student_profile.html", context)



@login_required(login_url="signin")
def facilitator_update_profile(request):
    profile = get_object_or_404(FacilitatorProfile, user = request.user)

    if request.method == 'POST':
        profile_form = FacilitatorProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('facilitator_profile')
    else:
        profile_form = FacilitatorProfileForm(instance=profile)

        
            
    user_profile = FacilitatorProfile.objects.get(user = request.user)
    
    context = {
        'profile': user_profile,
        'form': profile_form
    }

    # return render(request, "profile.html", context)

    return render(request, "dashboard/facilitator_profile.html", context)





class CustomResetPasswordView(PasswordResetView):
    template_name = 'password_reset_form.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'email_subject.txt'
    success_url = 'password_reset/done'
    form_class = CustomPasswordResetForm




def student_signup(request):
    if request.user.is_anonymous:
        now = datetime.now()
        month = now.month
        year = now.year
        day = now.day
        count = StudentProfile.objects.count()

        print('This====', str(year)  + str(month)+ str(day) + str(count) )
    
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            fname = request.POST['fname']
            lname = request.POST['lname']
            course = request.POST['course']
            gender = request.POST['gender']
            institution = request.POST['institution']
            location = request.POST['address']
            LGA = request.POST['LGA']
            state = request.POST['state']
            NIN = request.POST['NIN']
            id_number = str(year)  + str(month)+ str(day) + str(count) 
            
            phone_number = request.POST['phone_number']
            password = request.POST['password']

            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'Email Already Used ')
                return redirect('student-signup')
            elif CustomUser.objects.filter(username=username).exists():
                messages.error(request, "Username Already Used")
                return redirect('student-signup')
            else:
                user = CustomUser.objects.create_user(username=username, email=email, password=password)
                user.first_name = fname
                user.last_name = lname
                user.is_student = True
                user.save()
                
                
                subject = 'Welcome to InnovationbedAI Labs'
                email_from = settings.EMAIL_HOST_USER
                msg_html = render_to_string('email.html', {"username":username})
                message = f'''Hi {username}, thank you for registering On InnovationbedAI Labs. Your Account Has Been Successful Created. Please Do Not Share Your Details With Anyone'''
                send_mail( "InnovationbedAI Labs welcome message", message, email_from, [email], html_message=msg_html)
                
                
                student_profile = StudentProfile.objects.create(
                    full_name = str(fname) + ' ' + str(lname),
                    course = course,
                    institution = institution,
                    gender = gender,
                    state = state,
                    address = location,
                    LGA = LGA,
                    NIN = NIN,
                    phone_number = phone_number,
                    user= user,
                    email = email,
                    id_number = id_number

                
                    
                )
                        
                messages.success(request, 'Account Created successfully')
                return redirect('signin')

    else:
        return redirect( 'dashboard')
    return render(request, 'dashboard/student-signup.html')




def facilitator_signup(request):
    if request.user.is_anonymous:
    
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            fname = request.POST['fname']
            lname = request.POST['lname']
            password = request.POST['password']
            number = request.POST['number']
            address = request.POST['address']

            # if password == password2:
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'Email Already Used ')
                return redirect('facilitator-signup')
            elif CustomUser.objects.filter(username=username).exists():
                messages.error(request, "Username Already Used")
                return redirect('facilitator-signup')
            else:
                user = CustomUser.objects.create_user(username=username, email=email, password=password)
                user.first_name = fname
                user.last_name = lname
                user.is_facilitator = True
                user.save()
                
                
                subject = 'Welcome to InnovationbedAI Labs'
                email_from = settings.EMAIL_HOST_USER
                msg_html = render_to_string('email.html', {"username":username})
                message = f'''Hi {username}, thank you for registering On InnovationbedAI Labs. Your Account Has Been Successful Created. Please Do Not Share Your Details With Anyone'''
                send_mail( "InnovationbedAI Labs welcome message", message, email_from, [email], html_message=msg_html)
                
                
                facilitator_profile = FacilitatorProfile.objects.create(
                    full_name = str(fname) + " " + str(lname),
                    user = user,
                    phone_number = number,
                    email = email,
                    address = address,
                
                    
                )
                        
                messages.success(request, 'Account Created successfully')
                return redirect('signin')
            # else:
            #     messages.error(request, "Password Not Thesame")
            #     return redirect('/')
    else:
        return redirect( 'dashboard')
    return render(request, 'dashboard/facilitator-signup.html')


    

def sponsor_signup(request):
    if request.user.is_anonymous:
    
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            fname = request.POST['fname']
            lname = request.POST['lname']
            number = request.POST['number']
            password = request.POST['password']
            location = request.POST['address']

            # password2 = request.POST['password2']

            # if password == password2:
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'Email Already Used ')
                return redirect('sponsor-signup')
            elif CustomUser.objects.filter(username=username).exists():
                messages.error(request, "Username Already Used")
                return redirect('sponsor-signup')
            else:
                user = CustomUser.objects.create_user(username=username, email=email, password=password)
                user.first_name = fname
                user.last_name = lname
                user.is_sponsor = True
                user.save()
                
                subject = 'Welcome to InnovationbedAI Labs'
                email_from = settings.EMAIL_HOST_USER
                msg_html = render_to_string('email.html', {"username":username})
                message = f'''Hi {username}, thank you for registering On InnovationbedAI Labs. Your Account Has Been Successful Created. Please Do Not Share Your Details With Anyone'''
                send_mail( "InnovationbedAI Labs welcome message", message, email_from, [email], html_message=msg_html)
                
                
                
                sponsor_profile = SponsorProfile.objects.create(
                    full_name = str(fname) + " " + str(lname),
                    user = user,
                    phone_number = number,
                    email = email,
                    address = location,
                
                    
                )
                        
                messages.success(request, 'Account Created successfully')
                return redirect('signin')
            # else:
            #     messages.error(request, "Password Not Thesame")
            #     return redirect('/')
    else:
        return redirect('dashboard')
    return render(request, 'dashboard/sponsor-signup.html')









# def confirm_course_payment(request):
#     student_profile = StudentProfile.objects.get(user = request.user)
#     student_profile.paid = True
#     student_profile.save()
#     messages.success(request, 'Payment successful')
#     return redirect('dashboard')


@login_required(login_url="signin")
def confirm_course_sponsor(request):
    # student_profile = StudentProfile.objects.get(user = request.user)
    # student_profile.paid = True
    # student_profile.save()
    messages.success(request, 'Payment successful')
    return redirect('dashboard')

    



def register_option(request):
    if request.user.is_anonymous:
        return render(request, 'dashboard/option.html')
    else:
        return redirect('dashboard')

        
    



def signin(request):
    if request.user.is_anonymous:
        if request.method == "POST":
                username = request.POST["username"]
                password = request.POST["password"]
                user = authenticate(username = username, password = password)
                if user is not None:
                    login(request, user)
                    messages.success(request, "Logged in Successfully!")
                    return redirect("dashboard")
                else:
                    messages.error(request, "Incorrect Username or Password")
                    return redirect('signin')
    else:
        return redirect("dashboard")
    return render(request, 'dashboard/login.html')




@login_required(login_url='signin')
def signout(request):
    logout(request)
    messages.success(request, 'Logged out Successfully !')
    return redirect('signin')














# def User_Registration(request):
#     if request.user.is_authenticated:
#         return redirect('profile')


















#     if request.method=="POST":
#         uname=request.POST['full_name'] + str(uuid.uuid4())
#         # i think i need to remove the space character from the username :)
#         user=User.objects.create(
#             email=request.POST['email'],
#             username=uname,
#         )
#         user.set_password(request.POST['password'])
#         # user.is_active=False
#         # we can't log the user in from here if user.is_active is False
#         user.save()
#         login(request,user)
#         user_profile=UserProfile.objects.create(
#             gender=request.POST['gender'],
#             user=user,
#             full_name=request.POST['full_name']
#         )
#         user_profile.save()
#          # Generate a verification token
#         verification_token = str(uuid.uuid4())
#         user_profile.verification_token = verification_token
#         user_profile.save()
#         return redirect('update')
#     return render(request,'form.html')



# @login_required(login_url="signin")

# def Update_profile(request):
#     profile = get_object_or_404(Profile, username = request.user.username)

#     if request.method == 'POST':
#         # avatar = request.FILES['image']
#         # fname = request.POST['fname']
#         # lname = request.POST['lname']
#         # email = request.POST['email']
        
        
#         # profile = Profile.objects.get(username = request.user.username)
        
#         # profile.avatar = avatar,
#         # profile.first_name = fname,
#         # profile.last_name = lname,
#         # profile.email = email
        
#         # profile.save()
#         profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
#         if profile_form.is_valid():
#             profile_form.save()
#             messages.success(request, 'Your profile has been updated.')
#             return redirect('profile')
#     else:
#         profile_form = ProfileForm(instance=profile)

        
            
#     user_profile = Profile.objects.get(username = request.user.username)
    
#     context = {
#         'profile': user_profile,
#         'form': profile_form
#     }

#     return render(request, "profile.html", context)





    




# def sponsor_update_profile(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')  # Get the bio data from the POST request
#         full_name = request.POST.get('full_name')  # Get the bio data from the POST request
#         location = request.POST.get('location')  # Get the bio data from the POST request
#         phone_number = request.POST.get('phone_number')  # Get the bio data from the POST request
        
#          # Get the bio data from the POST request
        
#         if 'image'  in request.FILES:
#             image = request.FILES.get('image') 
#         else:
#             image = None    
    

#         # Update the profile model
#         sponsor_profile = SponsorProfile.objects.get(user=request.user)
#         sponsor_profile.email = email
#         sponsor_profile.full_name = full_name
#         sponsor_profile.location = location
#         sponsor_profile.phone_number = phone_number
#         sponsor_profile.image = image
        
#         sponsor_profile.save()

#         # Optionally, you can add a success message
#         messages.success(request, 'Your profile has been updated!')
        
#         # Redirect to the user's profile page
#         return redirect('profile')

#     sponsor_profile = SponsorProfile.objects.get(user=request.user)

    
#     context = {
#         'profile': sponsor_profile,
#     }

#     return render(request, "dashboard/profile.html", context)

