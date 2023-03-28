from django.contrib import admin

from .models import User, Tag, Post


class UserAdmin(admin.ModelAdmin):
    pass


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ("title",)
    }
    list_filter = ("author", "tags", "date")
    list_display = ("title", "author", "date")


admin.site.register(User, UserAdmin)
admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
