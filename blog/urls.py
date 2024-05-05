from django.urls import path


from blog.apps import BlogConfig
from blog.views import ArticlesListView, ArticlesDetailView, ArticlesCreateView, ArticlesUpdateView, ArticlesDeleteView, \
    NotPublishedView, toggle_published, ArticlesDeleteNotPublished

app_name = BlogConfig.name

urlpatterns = [
    path('', ArticlesListView.as_view(), name='list'),
    path('view/<int:pk>', ArticlesDetailView.as_view(), name='blog_detail'),
    path('create/', ArticlesCreateView.as_view(), name='create'),
    path('edit/<int:pk>', ArticlesUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', ArticlesDeleteView.as_view(), name='delete'),
    path('not_is_published/', NotPublishedView.as_view(), name='not_is_published'),
    path('is_published/<int:pk>', toggle_published, name='is_published'),
    path('delete_not_is_published/<int:pk>', ArticlesDeleteNotPublished.as_view(), name='delete_not_is_published'),
]