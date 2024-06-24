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
    img = models.TextField(default="anon.jpg")
    bio = models.TextField(default="Unknowable and Mysterious")
    roles = models.TextField(default="Staffwriter")
    pronouns = models.CharField(max_length=255, default="LEFT_EMPTY")
    major = models.CharField(max_length=255, default="LEFT_EMPTY")
    year = models.CharField(max_length=255, default="LEFT_EMPTY")
    location = models.CharField(max_length=255, default="LEFT_EMPTY")
    fact = models.CharField(max_length=255, default="LEFT_EMPTY")
    email = models.CharField(max_length=255, default="LEFT_EMPTY")
    socials = models.CharField(max_length=255, default="LEFT_EMPTY")
    class Meta:
        verbose_name_plural = "authors"
    def __str__(self) -> str:
        return self.name

class Issue(models.Model):
    name = models.CharField(max_length=255)
    vol = models.IntegerField(default=0)
    num = models.IntegerField(default=0)
    class Meta:
        verbose_name_plural = "issues"
    def __str__(self):
        return f"Vol {self.vol}, Issue {self.num}, '{self.name}'"
    def fold(self):
        return f"{self.vol}-{self.num}"

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


class Folder(models.Model):
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
def upload_location(instance, filename):
    # Customize the filename here using instance.name
    filename = f"{instance.folder.path}/{instance.name}"
    return f"static/{filename}"

class UploadedImage(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=upload_location)

    def __str__(self):
        return self.name
