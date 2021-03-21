from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(
    prefix=r'',
    basename='books',
    viewset=views.BookViewSet
)

app_name = 'books'
urlpatterns = [
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.startpage, name='start-page'),
    path('edit', views.edit),
    path('create/', views.create),
    path('top/', views.TopListView, name='book-list'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='onebook-detail'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('api/', include(router.urls)),
    path('suggest-ajax/', views.book_suggester, name='book-suggest')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
