from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import SimpleRouter

from . import views

# router = routers.DefaultRouter()
# router.register('books', views.BookViewSet, basename="Books")
# router.register('authors', views.AuthorViewSet)

router = SimpleRouter()
router.register(
    prefix=r'',
    basename='books',
    viewset=views.BookViewSet
)

app_name = 'books'
urlpatterns = [
                  path('', views.startpage, name='start-page'),
                  path('edit', views.edit),
                  path('create/', views.create),
                  path('top/', views.TopListView, name='book-list'),
                  path('book/<int:pk>/', views.BookDetailView.as_view(), name='onebook-detail'),
                  path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
                  path('upd/', views.update_rating, name='upd'),
                  # path('top/', views.UpdateRating.as_view(), name='book-rating'),
                  path('api/', include(router.urls)),
                  # path('api/', include('rest_framework.urls')),
                  path('suggest-ajax/', views.book_suggester, name='book-suggest')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
