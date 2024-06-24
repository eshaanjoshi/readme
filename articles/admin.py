from django.contrib import admin

# Register your models here.
from django.contrib import admin
from articles.models import Issue, Author, Category, Comment, Post, Folder

class CategoryAdmin(admin.ModelAdmin):
    pass

class PostAdmin(admin.ModelAdmin):
    pass

class CommentAdmin(admin.ModelAdmin):
    pass 

class AuthorAdmin(admin.ModelAdmin):
    pass

class IssueAdmin(admin.ModelAdmin):
    pass

class FolderAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Folder, FolderAdmin)