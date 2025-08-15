from django.shortcuts import redirect
from django.views.generic.edit import FormView, DeleteView, UpdateView, CreateView
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from blog.models import Article, Announcement, User, Category, Comment, Rating, Tag
from blog.forms import Login_Form, Registration_Form, User_Form, Article_Form
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
#from blog.mixins import 
from django.urls import reverse_lazy

class Login_View(FormView):
    template_name = "Login.html"
    form_class = Login_Form
    success_url = reverse_lazy('main_page')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, 'Невірний логін або пароль')
            return self.form_invalid(form)

class Registration_View(FormView):
    template_name = "Registration.html"
    form_class = Registration_Form
    success_url = reverse_lazy('login_page')

    def form_valid(self, form):
        user = form.save()
        self.object = user
        return super().form_valid(form)

class Logout_View(TemplateView):
    def get(self, request):
        logout(request)
        return redirect('/login/')

class Main_Page_View(TemplateView):
    template_name = "Main_Page.html"

class Profile_View(LoginRequiredMixin, UpdateView):
    model = User
    form_class = User_Form 
    template_name = 'User_Profile_Page.html'
    success_url = reverse_lazy('profile_page')

    def get_object(self):
        return self.request.user

class Article_List_View(ListView):
    model = Article
    template_name = 'All_Article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["articles"] = Article.objects.all()
        return context

class Article_Create_View(CreateView):
    pass



























