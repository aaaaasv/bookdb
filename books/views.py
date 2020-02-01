from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse

import django.contrib.sessions

import requests
import random

from .models import Book, Author
from .forms import BookForm, Ratings

color_dictionary = {0: '#AF9500;', 1: '#B4B4B4', 2: '#AD8A56'}  # gold, silver and bronze


def startpage(request):
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    # print(Book.objects.all().values_list('rating', flat=True))
    random_book_id = random.choice(range(1, len(Book.objects.all()) - 1))
    p = Book.objects.order_by('-rating')[:3]
    return render(request, 'books/index.html', {'books': p,
                                                'random': random_book_id,
                                                'colors': color_dictionary,
                                                'num_visits':num_visits})


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


class TopListView(ListView):
    model = Book
    paginate_by = 250
    queryset = Book.objects.exclude(rating=0)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = self.get_queryset().count()
        context['colors'] = color_dictionary

        return context


class BookDetailView(DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = Ratings()
        return context


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

            current_voters_number = book.rating_voters_number
            book.rating_voters_number = int(current_voters_number) + 1

            book.rating_sum = int(book.rating_sum) + int(form.cleaned_data['rate'])

            book.save()

            book.rating = book.rating_sum / book.rating_voters_number

            book.save()

            return HttpResponseRedirect("../book/%s" % request.POST.get("id"))
    else:
        form = Ratings()

    # return render(request, 'books/edit.html', {'form': form, 'books': Book.objects.all()})


from rest_framework import viewsets
from .serializers import BookSerializer, AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows books to be viewed or edited
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer