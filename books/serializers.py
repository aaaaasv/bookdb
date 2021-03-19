from rest_framework import serializers
from .models import Book, Author

from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from .documents import BookDocument


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'url', 'name')


# class BookSerializer(serializers.HyperlinkedModelSerializer):
#     author = serializers.HyperlinkedRelatedField(many=False, view_name='author-detail', queryset=Author.objects.all())


    # class Meta:
    #     model = Book
    #     fields = ('url', 'author', 'id', 'title', 'cover_picture', 'pub_year',)


class BookDocumentSerializer(DocumentSerializer):
    class Meta:
        document = BookDocument
        fields = (
            'id',
            'title',
            'author',
            'pub_year',
            'cover_picture',
            'rating',
            'rating_sum',
            'rating_voters_number'
        )
