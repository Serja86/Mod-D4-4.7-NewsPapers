import django.forms
from django_filters import FilterSet, CharFilter, DateFilter, ModelChoiceFilter
from .models import Post, Author


class PostSearch(FilterSet):
    dateCreation = DateFilter(
        lookup_expr='gte',
        widget=django.forms.DateInput(attrs={'type': 'date'})
    )
    title = CharFilter(
        field_name='title',
        lookup_expr = 'icontains',
        label = 'Название статьи'
    )

    author = ModelChoiceFilter(
        field_name='author',
        queryset = Author.objects.all(),
        lookup_expr=('exact'),
        label = 'Автор'
    )

    class Meta:
        model = Post
        fields = []
        # ('date', 'title', 'author')