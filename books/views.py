from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse
from django.http import HttpResponseNotFound
import django.contrib.sessions

from elasticsearch_dsl import Search
import requests
import random

from django.db.models import Sum

from django.contrib.auth.models import User
from .models import Book, Author, Rate
from .forms import BookForm, Ratings

color_dictionary = {0: '#AF9500;', 1: '#B4B4B4', 2: '#AD8A56'}  # gold, silver and bronze


def startpage(request):
    # random_book_id = random.choice(range(1, len(Book.objects.all()) - 1))
    p = Book.objects.order_by('-rating')[:3]
    return render(request, 'books/index.html', {'books': p,
                                                # 'random': random_book_id,
                                                'colors': color_dictionary
                                                })


def create(request):
    if request.method == "POST":
        book = Book()
        author = Author()
        book.title = request.POST.get("ftitle")
        book.author = Author(name=request.POST.get("fauthor"))
        book.author.save()
        book.save()
    return HttpResponseRedirect('../edit')


def edit(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            if 'remove' in request.POST:
                try:
                    book = Book.objects.get(id=request.POST.get("pk"))
                    book.delete()
                    return HttpResponseRedirect("edit")
                except Book.DoesNotExist:
                    return HttpResponseNotFound("<h2>Book not found</h2>")
            else:
                mybook = Book.objects.get(id=request.POST.get("pk"))
                myauthor = Author.objects.get(name=mybook.author)
                mybook.title = request.POST.get("ftitle")
                myauthor.name = request.POST.get("fauthor")
                myauthor.save()
                mybook.save()
                return HttpResponseRedirect('edit')
    else:
        form = BookForm()

    return render(request, 'books/edit.html', {'form': form, 'books': Book.objects.all()})


def delete(request):
    try:
        book = Book.objects.get(id=request.POST.get("pk"))
        book.delete()
        return HttpResponseRedirect("../edit")
    except Book.DoesNotExist:
        return HttpResponseNotFound("<h2>Book not found</h2>")


from django.http import JsonResponse


def book_suggester(request):
    from books.documents import BookDocument
    search_text = request.GET['search_text']
    s = BookDocument.search()
    s = s.suggest(
        'auto_completion',
        search_text,
        phrase={
            'field': 'title.suggest',
            'size': 1,
            'gram_size': 3,
            # "direct_generator": [{
            # "field": "title.suggest",
            # "suggest_mode": "always"
            # }],
        },
    )
    response = s.execute()
    # for i in response.suggest.auto_completion:
    #     print(i.options)
    # return response.suggest.phrase.options[0].title
    try:
        text = response.suggest.auto_completion[0].options[0]['text']
        return JsonResponse({'completed': text}, status=200)
    except IndexError:
        return JsonResponse({"error": ""})


def TopListView(request):
    context = {
        'object_list': Book.objects.all()
    }
    if request.GET and 'search-text' in request.GET:
        from books.documents import BookDocument
        search_text = request.GET.get('search-text')
        filtered_books = BookDocument.search().query('wildcard', title=f'*{search_text}*')
        if filtered_books.count() >= 1:
            context = {
                'object_list': filtered_books.to_queryset().all()
            }
    return render(request, 'books/book_list.html', context=context)


# class TopListView(ListView):
#     model = Book
#     paginate_by = 250
#     queryset = Book.objects.exclude(rating=0)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['count'] = self.get_queryset().count()
#         context['colors'] = color_dictionary
#
#         return context
#
#     def get_queryset(self):
#         if self.request.GET.get('search-text'):
#             from books.documents import BookDocument
#             search_text = self.request.GET.get('search-text')
#             # filtered_books = BookDocument.search().query('wildcard', title=f'*{search_text}*')
#             # if filtered_books.count() >= 1:
#             #     return filtered_books.to_queryset().all()
#             s = BookDocument.search()
#             s = s.suggest(
#                 'auto_complete',
#                 search_text,
#                 completion={'field': 'title.suggest'}
#             )
#             response = s.execute()
#             for option in response.suggest.auto_complete[0].options:
#                 print(option._source.title)
#             # for option in response.suggest.auto_complete[0].options:
#             # raise TypeError(option._source.title)
#             return response.suggest.auto_complete[0].options
#         return super().get_queryset()


class BookDetailView(DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = Ratings()
        try:
            context['rate'] = Rate.objects.get(user=self.request.user, book=self.object)
        except:
            context['rate'] = None
        return context

    def post(self, request, *args, **kwargs):
        book = Book.objects.get(pk=self.kwargs.get('pk'))
        user = request.user
        try:
            rate = Rate.objects.get(book=book, user=user)
            rate.score = request.POST.get('rating')
            rate.save()
        except Rate.DoesNotExist:
            Rate.objects.create(book=book, user=user, score=request.POST.get('rating'))

        return super(BookDetailView, self).get(request, *args, **kwargs)


class AuthorDetailView(DetailView):
    model = Author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.filter(author=context['author'])
        return context


def update_rating(request):
    if request.method == 'POST':
        form = Ratings(request.POST)
        if form.is_valid():
            book = Book.objects.get(id=request.POST.get("id"))

            # rate = Rate(user=request.user, book=book, score=form.cleaned_data['rate'])
            # rate.save()
            rate, created = Rate.objects.update_or_create(
                user=request.user, book=book, defaults={"score": form.cleaned_data['rate']}
            )

            # current_voters_number = book.rating_voters_number
            # book.rating_voters_number = int(current_voters_number) + 1

            book.rating_voters_number = len(Rate.objects.filter(book=book))
            summ = Rate.objects.filter(book=book).aggregate(Sum('score'))

            # book.rating_sum = int(book.rating_sum) + int(form.cleaned_data['rate'])
            book.rating_sum = summ['score__sum']
            book.save()

            book.rating = book.rating_sum / book.rating_voters_number

            book.save()

            return HttpResponseRedirect("../book/%s" % request.POST.get("id"))
    else:
        form = Ratings()

    # return render(request, 'books/edit.html', {'form': form, 'books': Book.objects.all()})


from rest_framework import viewsets
from .serializers import AuthorSerializer


# class BookViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows books to be viewed or edited
#     """
# queryset = Book.objects.all()
# serializer_class = BookSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_RANGE,
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_LT,
    LOOKUP_QUERY_LTE,
    SUGGESTER_COMPLETION,
)
from django_elasticsearch_dsl_drf.filter_backends import (
    DefaultOrderingFilterBackend,
    FacetedSearchFilterBackend,
    FilteringFilterBackend,
    SearchFilterBackend,
    SuggesterFilterBackend

)

from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from .documents import BookDocument
from .serializers import BookDocumentSerializer


class BookViewSet(DocumentViewSet):
    document = BookDocument
    serializer_class = BookDocumentSerializer
    ordering = ('id',)
    lookup_field = 'id'

    filter_backends = [
        DefaultOrderingFilterBackend,
        # FacetedSearchFilterBackend,
        FilteringFilterBackend,
        SearchFilterBackend,
        SuggesterFilterBackend,
    ]

    search_fields = (
        'title',
    )

    filter_fields = {
        'id': {
            'field': 'id',
            'lookups': [
                LOOKUP_FILTER_RANGE,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_GT,
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_LT,
                LOOKUP_QUERY_LTE,
            ],
        },
        'title': 'title'
    }

    suggester_fields = {
        'title_suggest': {
            'field': 'title.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION
            ]
        }
    }
    # s = s.suggest(
    #     'phrase',
    #     search_text,
    #     phrase={'field': 'title.suggest', 'size': 1, 'gram_size': 3, "direct_generator": [{
    #         "field": "title.suggest",
    #         "suggest_mode": "always"
    #     }], },
    # )
