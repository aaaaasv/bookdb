from rest_framework import serializers
from .models import Book, Author


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'url', 'name')


class BookSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.HyperlinkedRelatedField(many=False, view_name='author-detail', queryset=Author.objects.all())
    # author = AuthorSerializer(many=False)

    class Meta:
        model = Book
        fields = ('url', 'author','id' , 'title', 'cover_picture', 'pub_year', )


