from typing import Any
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth.hashers import check_password

from .models import Post as PostModel, Comment as CommentModel, Tag as TagModel, Author as AuthorModel, User as UserModel
from .forms import NewsletterForm, UserRegisterForm, UserLoginForm, CommentForm, ChangeEmailForm, ChangePasswordForm, ChangeImageForm, ChangeDescriptionForm, DeleteAccountForm


class Index(FormView):
    template_name = "Blog/index.html"
    form_class = NewsletterForm
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = PostModel.objects.all().order_by("-date")[0:4]
        return context

    def form_valid(self, form):
        form.save()
        try:
            form.send_email(
                form.cleaned_data['email'], form.cleaned_data['name'], form.cleaned_data['surname'])
        except ConnectionRefusedError:
            pass
        return super().form_valid(form)

    def post(self, request, *args, **kwargs): # TUTAJ SKOŃCZ BO SYF
        if request.method == "POST":
            form = NewsletterForm(request.POST)
            if form.is_valid():
                super().get_context_data()
                return render(request, "Blog/newsletter.html")
        return super().post(request, *args, **kwargs)


class Posts(FormView):
    template_name = "Blog/posts.html"
    form_class = NewsletterForm
    success_url = "/newsletter"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = "Posts"
        context["posts"] = PostModel.objects.all().order_by("-date")
        context['tags'] = TagModel.objects.all().order_by("tag")
        return context

    def form_valid(self, form):
        form.save()
        try:
            form.send_email(
                form.cleaned_data['email'], form.cleaned_data['name'], form.cleaned_data['surname'])
        except ConnectionRefusedError:
            pass
        return super().form_valid(form)


class PostsByTag(Posts):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = f"{self.kwargs['str']} Posts"
        tag = get_object_or_404(TagModel, tag=self.kwargs['str'])
        context["posts"] = PostModel.objects.all().order_by(
            "-date").filter(tags__tag=tag)
        context['active_tag'] = self.kwargs['str']
        return context


class PostsBySearch(ListView):  # dokończ
    template_name = "Blog/posts_search.html"
    model = PostModel
    context_object_name = "posts"

    def get(self, request, *args, **kwargs):
        if not kwargs.get("search"):
            return redirect("/")
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if not self.request.GET['search']:
            return super().get_queryset().filter(title__icontains="Space").order_by("-date")
        return super().get_queryset().filter(title__icontains=self.request.GET['search']).order_by("-date")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if (not self.request.GET['search']):
            context['search'] = "Space"
        else:
            context['search'] = f"{self.request.GET['search']}"
        return context


class Post(FormView):
    template_name = "Blog/post.html"
    form_class = CommentForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        print(self.success_url)
        context['post'] = PostModel.objects.get(slug=self.kwargs['slug'])
        context['comments'] = CommentModel.objects.all().filter(
            post=PostModel.objects.get(slug=self.kwargs['slug']))
        return context

    def form_valid(self, form):
        if not self.request.session.get("nickname"):
            return redirect("/logout")
        else:
            form.save(self.request.session.get(
                "nickname"), self.kwargs["slug"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("post", kwargs={"slug": self.kwargs['slug']})


class Authors(ListView):
    template_name = "Blog/authors.html"
    model = AuthorModel
    context_object_name = "authors"

    def get_queryset(self):
        return super().get_queryset().order_by("surname", "name")


class Author(DetailView):
    template_name = "Blog/author.html"
    model = AuthorModel
    context_object_name = "author"


class AuthorPosts(ListView):
    template_name = "Blog/author_posts.html"
    model = PostModel
    context_object_name = "posts"

    def get_queryset(self):
        return super().get_queryset().filter(author=AuthorModel.objects.get(slug=self.kwargs['slug'])).order_by("-date")

    def get_context_data(self, *args, **kwargs):
        author = AuthorModel.objects.get(slug=self.kwargs['slug'])
        context = super().get_context_data(*args, **kwargs)
        context['author_slug'] = author.slug
        context['author_name'] = author.name
        context['author_surname'] = author.surname
        context['tags'] = TagModel.objects.all().order_by("tag")
        return context


class AuthorPostsByTag(AuthorPosts):
    def get_queryset(self):
        tag = get_object_or_404(TagModel, tag=self.kwargs['str'])
        return super().get_queryset().filter(tags__tag=tag)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['active_tag'] = self.kwargs['str']
        return context


class About(TemplateView):
    template_name = "Blog/about.html"


class Register(CreateView):
    template_name = "Blog/register.html"
    model = UserModel
    form_class = UserRegisterForm
    success_url = "/login"


class Login(FormView):
    template_name = "Blog/login.html"
    form_class = UserLoginForm
    success_url = "/"

    def post(self, request, *args, **kwargs):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            try:
                user = UserModel.objects.get(login=form["login"].value())
            except UserModel.DoesNotExist:
                user = None
            if user != None:
                if check_password(form["password"].value(), user.password):
                    request.session["nickname"] = user.nickname
                else:
                    return render(request, self.template_name, {"form": form, "error": True})
            else:
                return render(request, self.template_name, {"form": form, "error": True})
        else:
            return render(request, self.template_name, {"form": form, "error": False})
        return super().post(request, *args, **kwargs)


def Logout(request):
    if request.method == "POST" or request.method == "GET":
        request.session.flush()
    return redirect("/")


class Settings(TemplateView):  # dokończ
    template_name = "Blog/settings.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_changeemail"] = ChangeEmailForm()
        context["form_changepassword"] = ChangePasswordForm()
        context["form_changeimage"] = ChangeImageForm()
        context["form_changedescription"] = ChangeDescriptionForm()
        context["form_deleteaccount"] = DeleteAccountForm()
        return context

    def get(self, request, *args, **kwargs):
        if not self.request.session.get("nickname"):
            return render(request, "Blog/do_not_access.html")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not self.request.session.get("nickname"):
            return redirect("/logout")
        if "change_email" in request.POST:
            self.change_email(request)
        else:
            return self.render_settings(request)
        return super().get(request, *args, **kwargs)

    def change_email(self, request):
        form = ChangeEmailForm(request.POST)
        if form.is_valid():
            user = UserModel.objects.get(
                nickname=self.request.session.get("nickname"))
            if form["old_email"].value() == user.email:
                pass
            else:
                return self.render_settings(request, email=form, password_error=True)
        else:
            return self.render_settings(request, email=form)

    def render_settings(self, request, email=ChangeEmailForm(), email_error=False, password=ChangePasswordForm(), password_error=False, image=ChangeImageForm(), description=ChangeDescriptionForm(), delete=DeleteAccountForm()):
        return render(request, self.template_name, {
            "form_changeemail": email,
            "form_changeemail_error": email_error,
            "form_changepassword": password,
            "form_changepassword_error": password_error,
            "form_changeimage": image,
            "form_changedescription": description,
            "form_deleteaccount": delete
        })


class User(TemplateView):  # dokończ
    template_name = "Blog/newsletter.html"
