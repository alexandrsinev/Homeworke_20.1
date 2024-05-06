from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from pytils.translit import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.models import Articles


# Контроллер для просмотра всех статей
class ArticlesListView(ListView):
    model = Articles

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


# Контроллер для просмотра выбранной статьи
class ArticlesDetailView(DetailView):
    model = Articles

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


# Контроллер для добавления новой статьи
class ArticlesCreateView(CreateView):
    model = Articles
    fields = ('title', 'contents', 'preview',)
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        if form.is_valid():
            new_articles = form.save()
            new_articles.slug = slugify(new_articles.title)

        return super().form_valid(form)


# Контроллер для редактирования статьи
class ArticlesUpdateView(UpdateView):
    model = Articles
    fields = ('title', 'contents', 'preview',)
    success_url = reverse_lazy('blog:list')

    def get_success_url(self):
        return reverse('blog:blog_detail', args=[self.kwargs.get('pk')])


# Контроллер для удаления статьи
class ArticlesDeleteView(DeleteView):
    model = Articles
    success_url = reverse_lazy('blog:list')


# Контроллер для отображения неопубликованных статей
class NotPublishedView(ListView):
    model = Articles
    template_name = 'blog/not_is_published.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=False)
        return queryset


# Функция для переключения статуса публикации
def toggle_published(request, pk):
    artcles_item = get_object_or_404(Articles, pk=pk)
    if artcles_item.is_published:
        artcles_item.is_published = False
    else:
        artcles_item.is_published = True
    artcles_item.save()

    return redirect(reverse('blog:list'))


# Контроллер для удаления неопубликованных статей
class ArticlesDeleteNotPublished(DeleteView):
    model = Articles
    template_name = 'blog/delete_not_is_published.html'
    success_url = reverse_lazy('blog:not_is_published')
