from django import forms
from .models import *
from django.contrib.auth.models import User

class MyBlogForm(forms.Form):
    title = forms.CharField(max_length=200, )
    post_body = forms.CharField(widget=forms.Textarea)
    data = forms.DateField(widget=forms.SelectDateWidget)
    widget = forms.Select(attrs={'class':'form-control', 'required':'required'})
    

class MyblogModelForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'
        widgets = {
            'category': forms.Select(attrs={'class':'form-control', 'placeholder':'Select Category'}),
            'title': forms.TextInput(attrs={'class':'form-control col-6', 'placeholder':'Enter Title'}),
            'post_body': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Enter Post Body'}),
            'created_date': forms.SelectDateWidget(attrs={'class':'form-control'})
        }
        
class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_staff']
        