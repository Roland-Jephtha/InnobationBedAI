from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from .forms import CustomSetPasswordForm, CustomPasswordResetForm


urlpatterns = [
    path('get_suggestions', get_admin_suggestions, name='get_suggestions'),
    path('suggestions', get_suggestions, name='suggestions'),
    path('', index, name='index'),
    path('sponsor_payment', sponsor_payment, name='sponsor_payment'),
    path('course_payment/<courses>', course_payment, name='course_payment'),
    path('course_content/<str:pk>', course_content, name='course_content'),
    path('states', states, name='states'),
    path('LGA', LGA, name='LGA'),
    path('institution', institution, name='institution'),
    path('department', department, name='department'),
    path('dashboard', dashboard, name='dashboard'),

    path('course_video/<courses>', course_video, name='course-video'),
    path('schedule_link/<courses>', schedule_link, name='schedule_link'),
    path('course_schedule', course_schedule, name='course_schedule'),
    path('com_course_schedule', com_course_schedule, name='com_course_schedule'),
    path('delete_course_schedule/<str:pk>', delete_course_schedule, name='delete_course_schedule'),
    path('confirm_course_payment/<courses>', confirm_course_payment, name='confirm_course_payment'),
    path('confirm_course_sponsor', confirm_course_sponsor, name='confirm_course_sponsor'),
    path('schedule', student_schedule, name='schedule'),
    path('com_schedule', com_schedule, name='com_schedule'),
    path('on_schedule', on_schedule, name='on_schedule'),
    path('grant/<courses>', grant, name='grant'),
    path('update_schedule/<str:pk>', UpdateSchedule.as_view(), name = 'update_schedule'),

    












    path('student-signup', student_signup, name='student-signup'),
    path('sponsor-signup', sponsor_signup, name='sponsor-signup'),
    path('facilitator-signup', facilitator_signup, name='facilitator-signup'),
    path('register-option', register_option, name='register-option'),
    path('courses', courses, name='courses'),
    path('sponsor_profile', sponsor_update_profile, name='sponsor_profile'),
    path('sponsor', sponsor, name='sponsor'),
    path('facilitator_profile', facilitator_update_profile, name='facilitator_profile'),
    path('student_profile', student_update_profile, name='student_profile'),

    path('login/', signin, name='signin'),
    path('signout', signout, name='signout'),
    
    path('password-reset/', auth_views.PasswordResetView.as_view(form_class=CustomPasswordResetForm,
        template_name='password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(form_class=CustomSetPasswordForm,
        template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete')

    
]