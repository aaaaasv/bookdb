from django.db import models

from django.contrib.auth.models import User


class Author(models.Model):
    name = models.CharField(max_length=70)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    pub_year = models.IntegerField(default=0)
    cover_picture = models.CharField(max_length=500,
                                     default='https://images-na.ssl-images-amazon.com/images/I/617LYNQsELL.jpg',
                                     blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    rating_sum = models.IntegerField(default=0)
    rating_voters_number = models.IntegerField(default=0)

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

    def plural_form(self):
        if self.rating_voters_number == 1:
            return ''
        else:
            return 's'

    def rated_or_not(self):
        if self.rating_voters_number == 0:
            return 'No rating available'
        else:
            return self.rating

    def number_of_stars(self):
        return '1' * int(self.rating)

    def half_of_star(self):
        if self.rating > int(self.rating):
            return True

    class Meta:
        ordering = ['-rating']

    def __str__(self):
        return "%s %s" % (self.author, self.title)


class Rate(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    score = models.IntegerField(default=0)

    # class Meta:
    #     unique_together = [
    #         ('user', 'book'),
    #     ]

    def __str__(self):
        return "%s : %s(%s)" % (self.user, self.book.title, self.score)
