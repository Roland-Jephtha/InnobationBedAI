from django.contrib import admin
from .models import *
from django import forms
from django.contrib import admin
import os


from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.contrib import admin
from django import forms

class GrantAdminForm(forms.ModelForm):
    class Meta:
        model = Grant
        fields = '__all__'

    # Override the course_title field to use TextInput with list of suggestions
    course_title = forms.CharField(widget=forms.TextInput(attrs={'list': 'course_titles_list'}))




class GrantAdmin(admin.ModelAdmin):
    list_display = ('student', 'course_title', 'approved')


class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'price')

admin.site.register(Grant, GrantAdmin)
admin.site.register(CustomUser)
admin.site.register(StudentProfile)
admin.site.register(SponsorProfile)
admin.site.register(FacilitatorProfile)
admin.site.register(Course, CourseAdmin)
admin.site.register(Course_Schedule)
admin.site.register(Course_Content)


admin.site.site_header = "InnovationBed AI Labs"
admin.site.index_title = "Manage InnovationBedAI Labs"