from django.db import models
import markdown
# Create your models here.
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=255)
    img = models.TextField(default="anon.png")
    bio = models.TextField()
    roles = models.TextField()
    class Meta:
        verbose_name_plural = "authors"
    def __str__(self) -> str:
        return self.name

class Issue(models.Model):
    name = models.CharField(max_length=255)
    vol = models.IntegerField(default=0)
    num = models.IntegerField(default=0)
    #name = f"Vol {vol}, Issue {num}"
    class Meta:
        verbose_name_plural = "issues"
    def __str__(self):
        return f"Vol {self.vol}, Issue {self.num}, '{self.name}'"

class Post(models.Model):
    title = models.CharField(max_length=225)

    authors = models.ManyToManyField("Author", related_name="posts")
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField("Category", related_name="posts")
    slug = models.SlugField()
    issues = models.ForeignKey("Issue", on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.title

class Comment(models.Model):
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    def __str__(self) -> str:
        return f"{self.author} on '{self.post}'"
