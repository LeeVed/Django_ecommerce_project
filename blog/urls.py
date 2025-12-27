from django.urls import path

from blog.apps import BlogConfig

from . import views

app_name = BlogConfig.name

urlpatterns = [
    path("", views.BlogPostListView.as_view(), name="post_list"),
    path("post/<slug:slug>/", views.BlogPostDetailView.as_view(), name="post_detail"),
    # Create
    path("create/", views.BlogPostCreateView.as_view(), name="post_create"),
    # Update
    path("post/<slug:slug>/edit/", views.BlogPostUpdateView.as_view(), name="post_update"),
    # Delete
    path("post/<slug:slug>/delete/", views.BlogPostDeleteView.as_view(), name="post_delete"),
]
