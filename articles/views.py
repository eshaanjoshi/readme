from django.shortcuts import render
import markdown

# Create your views here.

from django.http import HttpResponseRedirect
from articles.forms import (
    CommentForm,
    ArticleForm,
    CategoryForm,
    UploadImageForm,
    ArticlePublishForm,
)
from articles.models import (
    Post,
    Comment,
    Author,
    Issue,
    Category,
    Folder,
    UploadedImage,
)
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


def article_index(request):
    posts = Post.objects.all().order_by("-created_on").filter(published=True)
    context = {
        "posts": posts,
    }
    return render(request, "articles/index.html", context)


def article_author_index(request):
    authors = Author.objects.all()
    context = {
        "authors": authors,
    }
    return render(request, "articles/authorlist.html", context)


def article_category_index(request):
    categories = Category.objects.all().order_by("name")
    context = {
        "categories": categories,
    }
    return render(request, "articles/categorylist.html", context)


def article_issues_index(request):
    issues = Issue.objects.all().order_by("vol")
    issues_by_volume = {}

    for issue in issues:
        volume = issue.vol
        if volume not in issues_by_volume:
            issues_by_volume[volume] = []
        issues_by_volume[volume].append(issue)
    issue = issues
    return render(
        request,
        "articles/issuelist.html",
        {"issues": issue, "issues_by_volume": issues_by_volume},
    )


def article_category(request, category):
    posts = (
        Post.objects.filter(categories__name__contains=category)
        .order_by("-created_on")
        .filter(published=True)
    )
    context = {
        "category": category,
        "posts": posts,
    }
    return render(request, "articles/category.html", context)


def article_author(request, author):
    posts = (
        Post.objects.filter(authors__name__contains=author)
        .order_by("-created_on")
        .filter(published=True)
    )
    aut = Author.objects.filter(name__contains=author).first()
    context = {
        "a": aut,
        "author": author,
        "posts": posts,
    }
    return render(request, "articles/author.html", context)


def article_issue(request, vol, num):
    issue = Issue.objects.get(num=num, vol=vol)
    posts = Post.objects.filter(issues__name__contains=issue.name).order_by(
        "-created_on"
    )

    context = {
        "i": issue,
        "issue": issue.name,
        "posts": posts,
    }
    return render(request, "articles/issue.html", context)


def article_detail(request, slug, pk):
    post = Post.objects.get(slug=slug, pk=pk)
    comments = Comment.objects.filter(post=post)
    form = CommentForm()
    md = markdown.Markdown(extensions=["fenced_code"])
    content = md.convert(post.body)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post,
            )
            comment.save()
            return HttpResponseRedirect(request.path_info)

    context = {
        "post": post,
        "comments": comments,
        "form": CommentForm(),
        "content": content,
    }

    return render(request, "articles/detail.html", context)


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("editor_tools")
        else:
            return render(
                request, "articles/login.html", {"error": "Invalid credentials"}
            )
    return render(request, "articles/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "articles/signup.html", {"form": form})


@login_required
def home_view(request):
    user = request.user
    context = {"user": user}

    return render(request, "articles/editor_tools.html", context)


def create_article_view(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("article_success")
    else:
        form = ArticleForm()
    return render(request, "articles/create_article.html", {"form": form})


def article_success_view(request):
    return render(request, "articles/article_success.html")


def create_category(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("article_category_index")  # Redirect to category list view
    else:
        form = CategoryForm()
    return render(request, "articles/create_category.html", {"form": form})


def category_list(request):
    categories = Category.objects.all()
    return render(request, "articles/categorylist.html", {"categories": categories})


def editor_tools(request):
    return render(request, "articles/editor_tools.html")


def folder_list(request):
    folders = Folder.objects.all()
    return render(request, "articles/folder_list.html", {"folders": folders})


def display_folder(request, folder_id):
    folder = Folder.objects.get(pk=folder_id)
    return render(request, "articles/display_folder.html", {"folder": folder})


def upload_image(request, folder_id):
    if not request.user.is_authenticated:
        return redirect("login")
    folder = Folder.objects.get(pk=folder_id)
    if request.method == "POST":
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.image.name = form["name"]
            instance.folder = folder
            instance.save()
            return redirect("upload_success")  # Redirect to a success page
    else:
        form = UploadImageForm()
    return render(
        request, "articles/upload_image.html", {"form": form, "folder": folder}
    )


def upload_success(request):
    return render(request, "articles/upload_success.html")


def article_create_or_edit(request, article_id=None):
    if not request.user.is_authenticated:
        return redirect("login")
    if article_id:
        article = get_object_or_404(Post, id=article_id)
    else:
        article = None

    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect(
                "article_issues_edit"
            )  # Adjust the redirect target as necessary
    else:
        form = ArticleForm(instance=article)

    return render(
        request, "articles/article_form.html", {"form": form, "article": article}
    )


def article_issues_edit(request):
    issues = Issue.objects.all().order_by("vol").prefetch_related("articles")
    issues_by_volume = {}

    for issue in issues:
        volume = issue.vol
        if volume not in issues_by_volume:
            issues_by_volume[volume] = []
        issues_by_volume[volume].append(issue)

    return render(
        request,
        "articles/issueedit.html",
        {"issues": issues, "issues_by_volume": issues_by_volume},
    )


def article_publish(request):
    issues = Issue.objects.all().order_by("vol").prefetch_related("articles")
    issues_by_volume = {}

    if not request.user.is_authenticated:
        return redirect("login")
    for issue in issues:
        volume = issue.vol
        if volume not in issues_by_volume:
            issues_by_volume[volume] = []
        issues_by_volume[volume].append(issue)
    form = ArticlePublishForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            publish_ids = form.cleaned_data.get("publish_ids")
            unpublish_ids = form.cleaned_data.get("unpublish_ids")

            if publish_ids:
                Post.objects.filter(id__in=publish_ids).update(published=True)
            if unpublish_ids:
                Post.objects.filter(id__in=unpublish_ids).update(published=False)

            return redirect(
                "article_publish"
            )  # Redirect to refresh the page after changes

    context = {
        "issues": issues,
        "issues_by_volume": issues_by_volume,
        "form": form,
    }
    return render(request, "articles/article_publish.html", context)
