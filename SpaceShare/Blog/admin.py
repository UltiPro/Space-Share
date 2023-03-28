from django.contrib import admin

from .models import Newsletter, Author, Tag, User, Comment, Post


class AuthorAdmin(admin.ModelAdmin):
    pass


class UserAdmin(admin.ModelAdmin):
    pass


class CommentAdmin(admin.ModelAdmin):
    pass


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ("title",)
    }
    list_filter = ("author", "tags", "date")
    list_display = ("title", "author", "date")


admin.site.register(Newsletter)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Tag)
admin.site.register(User, UserAdmin)
admin.site.register(Comment)
admin.site.register(Post, PostAdmin)
