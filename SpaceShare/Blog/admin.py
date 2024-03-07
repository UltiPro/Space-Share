from django.contrib import admin
from django.http.request import HttpRequest
from .models import Newsletter, Author, Tag, Post, User, Comment


class NewsletterAdmin(admin.ModelAdmin):
    list_display = ("__str__", "email")
    search_fields = ("name", "surname")
    readonly_fields = ("name", "surname", "email")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request: HttpRequest, obj=...):
        return False


class AuthorAdmin(admin.ModelAdmin):
    list_display = ("__str__", "email")
    search_fields = ("name", "surname")
    prepopulated_fields = {"slug": ("name", "surname")}

    class Media:
        js = ("Blog/js/textarea_tabs.js",)

    def save_model(self, request, obj, form, change):
        obj.description = obj.description.replace("    ", "&emsp;")
        return super().save_model(request, obj, form, change)


class UserAdmin(admin.ModelAdmin):
    list_display = ("__str__", "email")
    search_fields = ("nickname", "email")
    readonly_fields = ("login", "password", "email")
    prepopulated_fields = {"slug": ("nickname",)}

    class Media:
        js = ("Blog/js/textarea_tabs.js",)

    def save_model(self, request, obj, form, change):
        obj.description = obj.description.replace("    ", "&emsp;")
        return super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        return False


class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "date")
    list_filter = ("date",)
    search_fields = ("user", "post")
    readonly_fields = ("post", "user")

    class Media:
        js = ("Blog/js/textarea_tabs.js",)

    def save_model(self, request, obj, form, change):
        obj.content = obj.content.replace("    ", "&emsp;")
        return super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        return False


class PostAdmin(admin.ModelAdmin):
    list_display = ("author", "title", "date")
    list_filter = ("author", "tags", "date")
    search_fields = ("author", "title")
    prepopulated_fields = {"slug": ("title",)}

    class Media:
        js = ("Blog/js/textarea_tabs.js",)

    def save_model(self, request, obj, form, change):
        obj.content = obj.content.replace("    ", "&emsp;")
        return super().save_model(request, obj, form, change)


admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, PostAdmin)
