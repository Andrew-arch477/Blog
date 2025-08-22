from django import forms
from .models import Announcement, Article, User, Tag, Rating, Category, Comment
from django.contrib.auth.forms import UserCreationForm

class Login_Form(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

class Registration_Form(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        label='Username:',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    first_name = forms.CharField(
        max_length=150,
        label='First name:',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    last_name = forms.CharField(
        max_length=150,
        label='Last name:',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    email = forms.EmailField(
        label='Email:',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    password1 = forms.CharField(
        label='Password:',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    password2 = forms.CharField(
        label='Confirm:',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name' ,'last_name', 'email', 'password1', 'password2']

ROLE_CHOICES = [
    ('writer', 'Writer'),
    ('user', 'User'),
]

class User_Form(UserCreationForm):
    first_name = forms.CharField(
        max_length=150,
        label='First name:',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    last_name = forms.CharField(
        max_length=150,
        label='Last name:',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    email = forms.EmailField(
        label='Email:',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    password1 = forms.CharField(
        label='Password:',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    password2 = forms.CharField(
        label='Confirm:',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    role = forms.ChoiceField(
        label='Roles:',
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['first_name' ,'last_name', 'role', 'email', 'password1', 'password2']

class Article_Form(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['name', 'text', 'category', 'tags', 'stage']

class Article_Filtration_Form(forms.Form):
    name = forms.CharField(required=False)
    stage = forms.ChoiceField(choices=Article.STAGE_CHOICES, required=False)
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), required=False)
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)

class Comment_Form(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
