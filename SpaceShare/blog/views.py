from django.shortcuts import render

def index(request):
    return render(request, "blog/index.html")

def posts(request):
    return render(request, "blog/all-posts.html")

def posts_detail(request, slug):
    return request(request, "blog/post.html")