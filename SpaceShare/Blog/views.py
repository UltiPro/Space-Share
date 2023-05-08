from django.views.generic import ListView, DetailView, CreateView, FormView
from django.views.generic.base import TemplateView
from django.utils.datastructures import MultiValueDictKeyError
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth.hashers import check_password

from .models import Post as PostModel, Comment as CommentModel, Tag as TagModel, Author as AuthorModel, User as UserModel
from .forms import NewsletterForm, UserRegisterForm, UserLoginForm, CommentForm, ChangeEmailForm, ChangePasswordForm, ChangeImageForm, DeleteAccountForm, ChangeDescriptionForm


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

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            form = NewsletterForm(request.POST)
            if form.is_valid():
                self.form_valid(form)
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

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            form = NewsletterForm(request.POST)
            if form.is_valid():
                self.form_valid(form)
                return render(request, "Blog/newsletter.html")
        return super().post(request, *args, **kwargs)


class PostsByTag(Posts):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = f"{self.kwargs['str']} Posts"
        tag = get_object_or_404(TagModel, tag=self.kwargs['str'])
        context["posts"] = PostModel.objects.all().order_by(
            "-date").filter(tags__tag=tag)
        context['active_tag'] = self.kwargs['str']
        return context


class PostsBySearch(ListView):
    template_name = "Blog/posts_search.html"
    model = PostModel
    context_object_name = "posts"

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except MultiValueDictKeyError:
            return redirect("/")

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
        context['post'] = PostModel.objects.get(slug=self.kwargs['slug'])
        context['comments'] = CommentModel.objects.all().filter(
            post=PostModel.objects.get(slug=self.kwargs['slug'])).order_by("-date")
        return context

    def form_valid(self, form):
        if not self.request.session.get("nickname"):
            return redirect("/logout")
        else:
            form.save(self.request.session.get(
                "nickname"), self.kwargs["slug"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("post", kwargs={"slug": self.kwargs['slug']}) + "#comments"


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
            if user != None and check_password(form["password"].value(), user.password):
                request.session["nickname"] = user.nickname
                request.session["image"] = user.image.url
            else:
                return render(request, self.template_name, {"form": form, "error": True})
        else:
            return render(request, self.template_name, {"form": form, "error": False})
        return super().post(request, *args, **kwargs)


def Logout(request):
    if request.method == "POST" or request.method == "GET":
        request.session.flush()
    return redirect("/")


class Settings(TemplateView):
    template_name = "Blog/settings.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_changeemail"] = ChangeEmailForm()
        context["form_changepassword"] = ChangePasswordForm()
        context["form_changeimage"] = ChangeImageForm()
        context["form_deleteaccount"] = DeleteAccountForm()
        context["form_changedescription"] = ChangeDescriptionForm(instance=UserModel.objects.get(
            nickname=self.request.session.get("nickname")))
        context["user_slug"] = UserModel.objects.get(
            nickname=self.request.session.get("nickname")).slug
        return context

    def get(self, request, *args, **kwargs):
        if not self.request.session.get("nickname"):
            return redirect("/logout")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not self.request.session.get("nickname"):
            return redirect("/logout")
        if "change_email" in request.POST:
            return self.change_email(request)
        elif "change_password" in request.POST:
            return self.change_password(request)
        elif "change_image" in request.POST:
            return self.change_image(request)
        elif "delete_account" in request.POST:
            return self.delete_account(request)
        elif "change_description" in request.POST:
            return self.change_description(request)

    def change_email(self, request):
        form = ChangeEmailForm(request.POST, instance=UserModel.objects.get(
            nickname=self.request.session.get("nickname")))
        if form.is_valid():
            form.save()
            return self.render_settings(request, email=form, email_success=True)
        else:
            return self.render_settings(request, email=form)

    def change_password(self, request):
        form = ChangePasswordForm(request.POST, instance=UserModel.objects.get(
            nickname=self.request.session.get("nickname")))
        if form.is_valid():
            form.save()
            return self.render_settings(request, password=form, password_success=True)
        else:
            return self.render_settings(request, password=form)

    def change_image(self, request):
        form = ChangeImageForm(request.POST, request.FILES, instance=UserModel.objects.get(
            nickname=self.request.session.get("nickname")))
        if form.is_valid():
            form.save()
            request.session["image"] = form.instance.image.url
            return self.render_settings(request, image=form, image_success=True)
        else:
            return self.render_settings(request, image=form)

    def delete_account(self, request):
        form = DeleteAccountForm(request.POST, instance=UserModel.objects.get(
            nickname=self.request.session.get("nickname")))
        if form.is_valid():
            form.save()
            return redirect("/logout")
        else:
            return self.render_settings(request, delete=form)

    def change_description(self, request):
        form = ChangeDescriptionForm(request.POST, instance=UserModel.objects.get(
            nickname=self.request.session.get("nickname")))
        if form.is_valid():
            form.save()
            return self.render_settings(request, description=form, description_success=True)
        else:
            return self.render_settings(request, description=form)

    def render_settings(self, request, email=ChangeEmailForm(), email_success=False, password=ChangePasswordForm(), password_success=False, image=ChangeImageForm(), image_success=False, delete=DeleteAccountForm(), description=ChangeDescriptionForm(), description_success=False):
        return render(request, self.template_name, {
            "form_changeemail": email,
            "form_changeemail_success": email_success,
            "form_changepassword": password,
            "form_changepassword_success": password_success,
            "form_changeimage": image,
            "form_changeimage_success": image_success,
            "form_deleteaccount": delete,
            "form_changedescription": description,
            "form_changedescription_success": description_success,
            "user_slug": UserModel.objects.get(nickname=self.request.session.get("nickname")).slug
        })


class User(DetailView):
    template_name = "Blog/user.html"
    model = UserModel
    context_object_name = "user"
