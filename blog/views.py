from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage
from django.template.loader import render_to_string
from django.views.generic.edit import FormView, DeleteView, UpdateView, CreateView
from django.views.generic.base import TemplateView
from django.views.generic import DetailView
from django.views.generic.list import ListView
from blog.models import Article, Announcement, User, Category, Comment, Rating, Tag
from blog.forms import Login_Form, Registration_Form, User_Form, Article_Form, Comment_Form, Article_Filtration_Form
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.mixins import UserIsAdminMixin, UserIsOwnerMixin, UserIsWriterMixin
from django.urls import reverse, reverse_lazy

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

class Main_Page_View(ListView):
    model = Article
    template_name = "Main_Page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["articles"] = Article.objects.order_by('-created_at')[:5]
        return context

class Profile_View(LoginRequiredMixin, UpdateView):
    model = User
    form_class = User_Form 
    template_name = 'User_Profile_Page.html'
    success_url = reverse_lazy('profile_page')

    def get_object(self):
        return self.request.user

class Article_List_View(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'All_Article.html'
    context_object_name = 'articles'
    paginate_by = 3

    def get_queryset(self):
        queryset = Article.objects.all().prefetch_related('category', 'tags').order_by('-id')
        self.form = Article_Filtration_Form(self.request.GET or None)

        if self.form.is_valid():
            data = self.form.cleaned_data
            name = (data.get("name") or '').strip()
            stage = data.get("stage")
            category = data.get("category")
            tags = data.get("tags")

            if name:
                queryset = queryset.filter(name__icontains=name)
            if stage:
                queryset = queryset.filter(stage=stage)
            if category:
                queryset = queryset.filter(category=category)
            if tags:
                queryset = queryset.filter(tags=tags)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        return context

    def paginate_queryset(self, queryset, page_size):
        paginator = Paginator(queryset, page_size)
        page = self.request.GET.get('page') or 1
        try:
            page_obj = paginator.page(page)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages) 
        return (paginator, page_obj, page_obj.object_list, page_obj.has_other_pages())

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string(self.template_name, context=context, request=self.request)
            return JsonResponse({'html': html})
        return super().render_to_response(context, **response_kwargs)

class Article_Create_View(LoginRequiredMixin, UserIsWriterMixin, CreateView):
    model = Article
    form_class = Article_Form
    template_name = "Create_Article.html"
    success_url = "/articles/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class Article_Detail_View(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'Detail_Article.html'
    context_object_name = "article"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        writer = self.object.user
        user = self.request.user
        context['is_subscribed'] = writer and writer in user.subscription.all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        writer = self.object.user

        if writer and writer.role == 'writer' and writer != request.user:
            if writer in request.user.subscription.all():
                request.user.subscription.remove(writer)
            else:
                request.user.subscription.add(writer)

        return redirect(reverse('articles_detail_page', args=[self.object.pk]))

class Article_Update_View(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Article
    form_class = Article_Form
    template_name = "Update_Article.html"
    success_url = "/articles/"

class Article_Delete_View(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Article
    template_name = "Delete_Article.html"
    success_url = "/articles/"

class Comment_View(LoginRequiredMixin, CreateView):
    template_name = 'Comments_For_Article.html'
    form_class = Comment_Form

    def dispatch(self, request, *args, **kwargs):
        self.article = get_object_or_404(Article, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.article = self.article
        comment = form.save()

        return JsonResponse({
            'id': form.instance.id,
            'user': form.instance.user.username,
            'text': form.instance.text,
            'article_name': form.instance.article.name
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article'] = self.article
        context['comments'] = Comment.objects.filter(article=self.article)
        return context

class Comment_Update_View(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Comment
    form_class = Comment_Form
    template_name = "Update_Comment.html"
    success_url = "/articles/"

class Comment_Delete_View(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Comment
    template_name = "Delete_Comment.html"
    success_url = "/articles/"

class Announcement_List_View(LoginRequiredMixin, ListView):
    model = Announcement
    template_name = 'Announcements_page.html'
    context_object_name = 'announcements'
    paginate_by = 2

    def get_queryset(self):
        return Announcement.objects.all().order_by('id')












