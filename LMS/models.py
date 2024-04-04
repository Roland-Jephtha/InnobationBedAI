from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django.templatetags.static import static








class CustomUser(AbstractUser):
    # user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null = True)
    avatar = models.FileField(upload_to='profile-images', null=True)
    ref_id = models.CharField(max_length = 255, null = True)
    is_student = models.BooleanField(default=False)
    is_facilitator = models.BooleanField(default=False)
    is_sponsor = models.BooleanField(default=False)

    class Meta:
        ordering = ['last_name']

    def __str__(self):
        return f"{self.username}: {self.first_name} {self.last_name}"
    
    



class StudentProfile(models.Model):
    # gender_choice = (
    #     ("Male", "Male"),
    #     ("Female", "Female"),
    #     ("Custom", "Custom"),
    # )
    # institution_choice = (
    #     ("University", "University"),
    #     ("Polytechnic", "Polytechnic"),
    #     ("College of Education", "College of Education"),
    # )
    # course_choice = (
    #     ("Computer Science", "Computer Science"),
    #     ("Electrical Engineering", "Electrical Engineering"),
    #     ("Mechanical Engineering", "Mechanical Engineering"),
    #     ("Petroleum Engineering", "Petroleum Engineering"),
    #     ("Medicine", "Medicine"),
    #     ("Argriculture", "Agriculture"),
    #     ("Others", "Others"),
    # )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="user_profile")
    full_name = models.CharField(max_length=500)
    email = models.EmailField(max_length=500)
    gender = models.CharField(max_length=255, null = True)
    institution  = models.CharField(max_length = 255, null = True, blank = True)
    image = models.ImageField(null=True, blank=True, upload_to="profiles/")
    address = models.CharField(null=True, blank=True, max_length=1000)
    course  = models.CharField( max_length = 255, null = True, blank = True)
    LGA  = models.CharField(max_length = 255, null = True, blank = True)
    state  = models.CharField(max_length = 255, null = True, blank = True)
    phone_number  = models.CharField(max_length = 255, null = True, blank = True)
    NIN  = models.CharField(max_length = 255, null = True, blank = True)
    id_number  = models.CharField(max_length = 255, null = True, blank = True)
    skillsets = models.TextField(null = True, blank=True)
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null  = True)
    purchased_courses = models.ManyToManyField('Course', blank=True)
    course_schedule = models.ManyToManyField('Course_Schedule', blank=True)

    def __str__(self):
        return self.full_name  # this function was missing self parameter, so i corrected it

    class Meta:
        ordering = ['-created']
        
        
        

    
    
class FacilitatorProfile(models.Model):
    gender_choice = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Custom", "Custom"),
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="facilitator_profile")
    full_name = models.CharField(max_length=500)
    email = models.EmailField(max_length=500)
    gender = models.CharField(choices=gender_choice, max_length=50)
    image = models.ImageField(null=True, blank=True, upload_to="profiles/")
    address = models.CharField(null=True, blank=True, max_length=1000)
    course  = models.CharField(max_length = 255, null = True, blank = True)
    phone_number  = models.CharField(max_length = 255, null = True, blank = True)
    skillsets = models.TextField(null = True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null  = True)

    def __str__(self):
        return self.full_name  # this function was missing self parameter, so i corrected it
    class Meta:
            ordering = ['-created']
   
    
class SponsorProfile(models.Model):
   
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="sponsor_profile")
    full_name = models.CharField(max_length=500)
    email = models.EmailField(max_length=500)
    image = models.ImageField(null=True, blank=True, upload_to="profiles/")
    address = models.CharField(null=True, blank=True, max_length=1000)
    phone_number  = models.CharField(max_length = 255, null = True, blank = True)
    bio = models.TextField(null = True)
    created = models.DateTimeField(auto_now_add=True, null  = True)

    def __str__(self):
        return self.full_name  # this function was missing self parameter, so i corrected it
    
    class Meta:
        ordering = ['-created']



class Course(models.Model):
    title = models.CharField(max_length = 255, null = True, unique = True)
    image = models.ImageField(null=True,  upload_to="course/")
    link = models.URLField(max_length = 255, null = True, )
    description = models.TextField(null = True, )
    course = models.CharField(max_length = 255, null = True, default = "general")
    price = models.IntegerField(max_length = 255, null = True, blank = True)
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null  = True)

    def is_purchased(self, user):
        student_profile, created = StudentProfile.objects.get_or_create(user = user)
        return self in student_profile.purchased_courses.all()
    
    def __str__(self):
        return self.title # this function was missing self parameter, so i corrected it
    class Meta:
        ordering = ['-created']



class Course_Content(models.Model):
    course = models.ForeignKey(Course, on_delete = models.CASCADE, null = True, )
    title = models.CharField(max_length = 255, null = True,)
    contents = models.TextField(null=True)
    link = models.URLField(blank=True, null= True)
    def __str__(self):
        return self.title
    
    


    
    
class Course_Schedule(models.Model):
    facilitator = models.ForeignKey(FacilitatorProfile, on_delete=models.CASCADE, null = True )
    course_title = models.ForeignKey(Course, on_delete = models.CASCADE, null = True, )
    duration = models.IntegerField(max_length = 255, null = True)
    link = models.URLField(max_length = 255, null = True)
    course_of_study = models.CharField(max_length = 255, null = True)
    date = models.DateTimeField( null = True)
    created = models.DateTimeField(auto_now_add=True, null  = True)


    def is_purchased(self, user):
        student_profile, created = StudentProfile.objects.get_or_create(user = user)
        return self in student_profile.course_schedule.all()
    
    
    def __str__(self):
        return str(self.course_title)
    
    class Meta:
        ordering = ['-created']



class Grant(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, null = True )
    course_title = models.CharField(max_length = 255, null = True)
    description = models.TextField(null = True)
    date = models.DateTimeField( null = True)
    created = models.DateTimeField(auto_now_add=True, null  = True)
    approved = models.BooleanField(default=False)
    
    
    def __str__(self):
        return str(self.student) + ' request a grant'
    
    class Meta:
        ordering = ['-created']


# class Sponsor_Payment(models.model):
#     sponsor = models.ForeignKey(SponsorProfile, on_delete=models.CASCADE, null = True )
#     amount = models.charField(max_length = 255, null = True, blank = True)
#     time = models.DateTimeField(auto_now_add=True, null  = True, blank = True)
    
    
#     def __str__(self):
#             return str(self.sponsor) + " Made a Sponsored of " + str(self.sponsor)
    
#     class Meta:
#         ordering = ['-time']
        
        
# class Course_Payment(models.model):
#     sponsor = models.ForeignKey(SponsorProfile, on_delete=models.CASCADE, null = True )
#     amount = models.charField(max_length = 255, null = True)
#     time = models.DateTimeField(auto_now_add=True, null  = True)
    
    
    
#     def __str__(self):
#             return str(self.sponsor) + " Sponsored a Course"
    
#     class Meta:
#         ordering = ['-time']

    
    

    