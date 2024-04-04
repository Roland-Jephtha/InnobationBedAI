from django import forms
from . models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm 
from django.contrib.auth.forms import SetPasswordForm
from .widgets import SuggestionInput


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomSetPasswordForm, self).__init__(*args, **kwargs)
        # Customize form fields if needed
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'New Password'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})






class CustomPasswordResetForm(PasswordResetForm):
        #Add css class
    def __init__(self, *args, **kwargs):
        super(CustomPasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})




# class CustomPasswordResetForm(PasswordResetForm):
#         #Add css class
#     def __init__(self, *args, **kwargs):
#         super(CustomPasswordResetForm, self).__init__(*args, **kwargs)
#         self.fields['email'].widget.attrs.update({'class': 'pl-5 form-control'})
        


# class UserForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'first_name', 'last_name', 'email',]

    
#     def __init__(self, *args, **kwargs):
#         super(UserForm, self).__init__(*args, **kwargs)
#         self.fields['username'].help_text = ''
#         # self.fields['password'].widget = forms.PasswordInput(attrs={'placeholder': ''})
    
    
class CourseScheduleForm(forms.ModelForm):
    class Meta:
        course_of_study = forms.CharField(widget=SuggestionInput)

        model = Course_Schedule
        fields  = ['course_title','date', 'duration','link', 'course_of_study', 'facilitator']
        
        
        widgets = {
            'date' : forms.DateTimeInput(attrs={'type' : 'datetime-local'}),
        }
        
        
    #Add css class
    def __init__(self, *args, **kwargs):
        super(CourseScheduleForm, self).__init__(*args, **kwargs)
        self.fields['course_title'].widget.attrs.update({'class': 'form-control'})
        self.fields['course_of_study'].widget.attrs.update({'class': 'form-control'})
        self.fields['date'].widget.attrs.update({'class': 'form-control'})
        self.fields['duration'].widget.attrs.update({'class': 'form-control'})
        self.fields['link'].widget.attrs.update({'class': 'form-control'})
        self.fields['facilitator'].widget.attrs.update({'class': 'hidden',})

    
    def clean_course_title(self):
        course_title = self.cleaned_data['course_title']
        if Course_Schedule.objects.filter(course_title=course_title).exists():
            raise forms.ValidationError("A course with this title already exists.")
        return course_title

        
        
class GrantForm(forms.ModelForm):
    class Meta:
        model = Grant
        fields  = [ 'course_title', 'description', 'student','date']
        
        
        widgets = {
            'date' : forms.DateTimeInput(attrs={'type' : 'datetime-local'}),
        }
        
        
    #Add css class
    def __init__(self, *args, **kwargs):
        super(GrantForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['course_title'].widget.attrs.update({'class': 'form-control'})
        self.fields['student'].widget.attrs.update({'class': 'hidden',})


 
       
        
        
        
class SponsorProfileForm(forms.ModelForm):
    class Meta:
        model = SponsorProfile
        fields  = ['image','full_name', 'address', 'email', 'phone_number', 'bio']
        
        
    #Add css class
    def __init__(self, *args, **kwargs):
        super(SponsorProfileForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'class': 'form-control', 'id': 'upload'})
        self.fields['full_name'].widget.attrs.update({'class': 'form-control', 'id': 'upload'})
        self.fields['address'].widget.attrs.update({'class': 'form-control', 'id': 'upload'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', })
        self.fields['email'].widget.attrs['readonly'] = True
        
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control', 'id': 'upload'})
        self.fields['bio'].widget.attrs.update({'class': 'form-control', 'id': 'upload'})




class FacilitatorProfileForm(forms.ModelForm):
    class Meta:
        model = FacilitatorProfile
        fields  = ['image','full_name', 'address', 'email', 'phone_number', 'course', 'skillsets']
        
        
    #Add css class
    def __init__(self, *args, **kwargs):
        super(FacilitatorProfileForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'class': 'form-control', 'id': 'upload'})
        self.fields['full_name'].widget.attrs.update({'class': 'form-control', 'id': 'upload'})
        self.fields['address'].widget.attrs.update({'class': 'form-control', 'id': 'upload'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs['readonly'] = True

        self.fields['phone_number'].widget.attrs.update({'class': 'form-control', 'id': 'upload'})
        self.fields['course'].widget.attrs.update({'class': 'form-control', 'id': 'upload'})
        # self.fields['skillsets'].widget.attrs.update({'class': 'form-control'})
        self.fields['skillsets'].widget = forms.Textarea(attrs={'placeholder': 'Add Skills', 'class': 'form-control', 'id': 'upload'})
        # self.fields['passw'].widget = forms.PasswordInput(attrs={'placeholder': ''})


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields  = ['image', 'id_number', 'full_name', 'state', 'address', 'email', 'phone_number',
                    'course', 'LGA', 'institution', 'gender', 'NIN', 'skillsets']
        
        
    #Add css class
    def __init__(self, *args, **kwargs):
        super(StudentProfileForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'class': 'form-control', 'id': 'upload'})
        self.fields['full_name'].widget.attrs.update({'class': 'form-control','id': 'upload'})
        self.fields['address'].widget.attrs.update({'class': 'form-control','id': 'upload'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})

        self.fields['phone_number'].widget.attrs.update({'class': 'form-control', 'id': 'upload'})
        self.fields['course'].widget.attrs.update({'class': 'form-control'})
        self.fields['institution'].widget.attrs.update({'class': 'form-control'})
        self.fields['gender'].widget.attrs.update({'class': 'form-control'})
        self.fields['state'].widget.attrs.update({'class': 'form-control'})
        self.fields['id_number'].widget.attrs.update({'class': 'form-control'})
        self.fields['NIN'].widget.attrs.update({'class': 'form-control'})


        self.fields['LGA'].widget.attrs.update({'class': 'form-control'})
        # self.fields['skillsets'].widget.attrs.update({'class': 'form-control'})
        self.fields['skillsets'].widget = forms.Textarea(attrs={'placeholder': 'Add Skills', 'class': 'form-control', 'id': 'upload'})
        # self.fields['passw'].widget = forms.PasswordInput(attrs={'placeholder': ''})
        
        
        # Non Editable fields
        
        self.fields['NIN'].widget.attrs['readonly'] = True
        self.fields['id_number'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['state'].widget.attrs['readonly'] = True
        self.fields['course'].widget.attrs['readonly'] = True
        self.fields['LGA'].widget.attrs['readonly'] = True
        self.fields['gender'].widget.attrs['readonly'] = True
        self.fields['institution'].widget.attrs['readonly'] = True
        
        
# class DepositForm(forms.ModelForm):
#     class Meta:
#         model = Deposit
#         fields  = ['currency', 'amount', 'payment_slip',   ]
        
        
#     #Add css class
#     def __init__(self, *args, **kwargs):
#         super(DepositForm, self).__init__(*args, **kwargs)
#         self.fields['currency'].widget.attrs.update({'class': 'deposit-form'})
#         self.fields['amount'].widget.attrs.update({'class': 'deposit-form'})
#         self.fields['payment_slip'].widget.attrs.update({'class': 'deposit-form'})
        
        

        
