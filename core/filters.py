from django import forms
import django_filters
from django_filters import FilterSet
from .models import Customer


# class PostFilter(FilterSet):
#     sitter = django_filters.filters.ModelChoiceFilter(queryset=Customer.objects.filter(), lookup_expr='exact',
#                                               label='Выберите автора')
#     title = django_filters.CharFilter(lookup_expr='icontains', label='Поиск по словам в заголовке новости')
#     date_time = django_filters.DateFilter(widget=DateInput(attrs={'type': 'date'}),
#                                           label='Показать все новости, размещенные позднее',
#                                           lookup_expr='date__gt')