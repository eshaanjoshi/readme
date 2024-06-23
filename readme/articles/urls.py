from django.urls import path

from . import views

urlpatterns = [
    path("", views.article_index, name="article_index"),
    path("authors", views.article_author_index, name="article_author_index"),
    path("tags", views.article_category_index, name="article_category_index"),
    path("issues", views.article_issues_index, name="article_issues_index"),
    path("post/<str:slug>/<int:pk>", views.article_detail, name="article_detail"),
    path("category/<category>/", views.article_category, name="article_category"),
    path("author/<author>/", views.article_author, name="article_author"),
    path("issue/<int:vol>/<int:num>", views.article_issue, name="article_issue"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('home', views.home_view, name='home'),
    path('create-article/', views.create_article_view, name='create_article'),
    path('article-success/', views.article_success_view, name='article_success'),
    path('create-category/', views.create_category, name='create_category'),
     path('editor/', views.editor_tools, name='editor_tools'),
     path('folders/', views.folder_list, name='folder_list'),
    path('folder/<int:folder_id>/', views.display_folder, name='display_folder'),
    path('folders/', views.folder_list, name='folder_list'),
    path('folder/<int:folder_id>/', views.display_folder, name='display_folder'),
    path('folder/<int:folder_id>/upload/', views.upload_image, name='upload_image'),
    path('upload/success/', views.upload_success, name='upload_success'),
]