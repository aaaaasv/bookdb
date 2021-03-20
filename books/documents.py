from django_elasticsearch_dsl import (
    Document,
    fields,
    Index,
    Completion,
    Keyword,
    Long,
    Text,
    Integer
)
from itertools import permutations
from elasticsearch_dsl import (
    analyzer,
    connections,
    token_filter,
    tokenizer,
)
from django_elasticsearch_dsl.registries import registry
from books.models import Book, Author

# book_index = Index('books')
#
# book_index.settings(
#     number_of_shards=1,
#     number_of_replicas=0
# )

ascii_fold = analyzer(
    "ascii_fold",
    tokenizer="whitespace",
    filter=["lowercase", token_filter("ascii_fold", "asciifolding")],
)

my_analyzer = analyzer(
    "my_analyzer",
    tokenizer=tokenizer('standard'),
    filter=["lowercase",
            token_filter(name_or_instance='shingle', type="shingle", min_shingle_size=2, max_shingle_size=3)]
)


@registry.register_document
class BookDocument(Document):
    title = fields.TextField(
        attr="title",
        fields={
            'suggest': fields.Completion(analyzer=my_analyzer),
        }
    )
    author = fields.ObjectField(
        properties={
            'name': fields.TextField(),
        }
    )

    def clean(self):
        self.suggest = {
            "input": [" ".join(p) for p in permutations(self.title.split())],
        }

    class Django:
        model = Book
        fields = [
            'id',
            'pub_year',
            'cover',
            'rating',
            'rating_sum',
            'rating_voters_number'
        ]
        related_models = [Author]

    class Index:
        name = 'book'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    def get_queryset(self):
        return super().get_queryset().select_related(
            'author'
        )

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Author):
            return related_instance.book_set.all()
