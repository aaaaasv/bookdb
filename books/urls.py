from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('books', views.BookViewSet)
router.register('authors', views.AuthorViewSet)


# app_name = 'book'
urlpatterns = [
    path('', views.startpage),
    path('edit', views.edit),
    path('create/', views.create),
    path('top/', views.TopListView.as_view(), name='topbook-list'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='onebook-detail'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('upd/', views.update_rating, name='upd'),
    # path('top/', views.UpdateRating.as_view(), name='book-rating'),
    path('api/', include(router.urls)),

]
