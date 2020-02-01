from django import forms


class BookForm(forms.Form):
    ftitle = forms.CharField(label='Title', max_length=100)
    fauthor = forms.CharField(label='Author', max_length=100)


class Ratings(forms.Form):
    rate = forms.ChoiceField(choices=((1, 1),
                                        (2, 2),
                                        (3, 3),
                                        (4, 4),
                                        (5, 5),
                                        (6, 6),
                                        (7, 7),
                                        (8, 8),
                                        (9, 9),
                                        (10, 10)))


