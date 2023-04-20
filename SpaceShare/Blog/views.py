from django.views.generic import ListView, DetailView, CreateView, FormView
from django.views.generic.base import TemplateView

from .models import Post as PostModel, Tag as TagModel, Author as AuthorModel, User as UserModel
from .forms import NewsletterForm, UserForm


class Index(FormView):
    template_name = "Blog/index.html"
    form_class = NewsletterForm
    success_url = "/newsletter"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = PostModel.objects.all().order_by("-date")[0:4]
        return context

    def form_valid(self, form):
        form.save()
        try:
            form.send_email(form.cleaned_data['email'],form.cleaned_data['name'],form.cleaned_data['surname'])
        except ConnectionRefusedError:
            pass
        return super().form_valid(form)


class Posts(FormView):
    template_name = "Blog/posts.html"
    form_class = NewsletterForm
    success_url = "/newsletter"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = "All Posts"
        context["posts"] = PostModel.objects.all().order_by("-date")
        context['tags'] = TagModel.objects.all().order_by("tag")
        return context

    def form_valid(self, form):
        form.save()
        try:
            form.send_email(form.cleaned_data['email'],form.cleaned_data['name'],form.cleaned_data['surname'])
        except ConnectionRefusedError:
            pass
        return super().form_valid(form)


class PostsByTag(Posts):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["posts"] = PostModel.objects.all().order_by(
            "-date").filter(tags__tag=TagModel.objects.get(tag=self.kwargs['str']))
        context['active_tag'] = self.kwargs['str']
        return context


class Post(DetailView):
    template_name = "Blog/post.html"
    model = PostModel
    context_object_name = "post"


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
        return super().get_queryset().filter(tags__tag=TagModel.objects.get(tag=self.kwargs['str']))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['active_tag'] = self.kwargs['str']
        return context


class About(TemplateView):
    # END THAT
    template_name = "Blog/about.html"


class Register(CreateView):
    template_name = "Blog/register.html"
    model = UserModel
    form_class = UserForm
    success_url = "/login"


class Login(TemplateView):
    # END THAT
    template_name = "Blog/login.html"


class Newsletter(TemplateView):
    # END THAT
    template_name = "Blog/newsletter.html"
