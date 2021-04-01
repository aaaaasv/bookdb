from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User


class Author(models.Model):
    name = models.CharField(max_length=70)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# class PublishingHouse(models.Model):
#     name = models.CharField(max_length=150)

class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    pub_year = models.IntegerField(default=0)
    description = models.TextField(null=True)
    cover = models.ImageField(upload_to="book_covers", default="default.png")
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    genres = models.ManyToManyField(Genre)

    is_public = models.BooleanField(default=False)

    def get_rating(self):
        rates_number = self.rate_set.all().count()
        rates_sum = self.rate_set.aggregate(Sum('score'))['score__sum']
        try:
            return round(rates_sum / rates_number, 1)
        except TypeError:
            return ""

    def get_genre_list(self):
        return ', '.join(self.genres.all().values_list('name', flat=True))

    # 0-4 = red; 4-6 = orange; 6-8 = yellow; 8-10 = green
    def get_rating_color(self):
        if self.rating >= 8:
            return '#00ff10'  # green
        elif self.rating >= 6:
            return '#649c0a'  # dark green
        elif self.rating >= 4:
            return '#b34d05'  # orange
        elif self.rating >= 0:
            return '#ff0000'  # red

    class Meta:
        ordering = ['-rating']

    def __str__(self):
        return "%s %s" % (self.author, self.title)


class Rate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    # class Meta:
    #     unique_together = [
    #         ('user', 'book'),
    #     ]

    def __str__(self):
        return "%s : %s(%s)" % (self.user, self.book.title, self.score)


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
