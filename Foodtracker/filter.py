import django_filters
from .models import CanteenItems


class CanteenItemsFilter(django_filters.FilterSet):
    """
    FilterSet for CanteenItems model using django-filter.
    Allows filtering snacks by name with case-insensitive search.
    """
    item_name = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Snack Name',
        help_text='Enter the name of the snack to search'
    )

    # Optional: Add more filters if needed
    min_rating = django_filters.NumberFilter(
        field_name='rating_out_of_5',
        lookup_expr='gte',
        label='Minimum Rating',
        help_text='Filter by minimum rating (out of 5)'
    )

    max_price = django_filters.NumberFilter(
        field_name='price_rs',
        lookup_expr='lte',
        label='Maximum Price',
        help_text='Filter by maximum price (₹)'
    )

    class Meta:
        model = CanteenItems

        fields = ['item_name']  # Primary field for search
