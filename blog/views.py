from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from .models import BlogPost


class BlogPostListView(ListView):
    """Список всех записей(read)"""

    model = BlogPost
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 5  # Пагинация по 5 записей на странице

    def get_queryset(self):
        """Функция принимает список записей и возврашает только опубликованные записи"""
        return BlogPost.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Наш блог"
        return context


class BlogPostDetailView(DetailView):
    """Детальный просмотр(read)"""

    model = BlogPost
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        """Функция увеличивает счетчик просмотров"""
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save(update_fields=["views_count"])
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.title
        return context


class BlogPostCreateView(LoginRequiredMixin, CreateView):
    """Cоздание записи (только для авторизованных, create)"""

    model = BlogPost
    template_name = "blog/post_form.html"
    fields = ["title", "content", "preview_image", "is_published"]
    success_url = reverse_lazy("blog:post_list")

    def form_valid(self, form):
        """Функция автоматически устанавливает автора"""
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Создание новой записи"
        context["submit_text"] = "Создать запись"
        return context


class BlogPostUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование записи (только для автора/админа, update)"""

    model = BlogPost
    template_name = "blog/post_form.html"
    fields = ["title", "content", "preview_image", "is_published"]

    def get_success_url(self):
        """При успешном редактировании отправляет на страницу post_detail, когда это необходимо"""
        return reverse_lazy("blog:post_detail", kwargs={"slug": self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Редактирование: {self.object.title}"
        context["submit_text"] = "Сохранить изменения"
        return context


class BlogPostDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление записи (только для автора/админа, delete)"""

    model = BlogPost
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("blog:post_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Удаление записи: {self.object.title}"
        return context
