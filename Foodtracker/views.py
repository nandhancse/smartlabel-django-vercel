from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.urls import reverse

from .models import CanteenItems
from .filter import CanteenItemsFilter


def snack_list(request):
    """
    Home page view that handles snack search.
    Uses Django filters to search for snacks in the database.
    If an exact match or single result is found, redirects to the detail page.
    Otherwise, displays the home page with search form.
    """
    # Get the search query from GET parameters
    item_name = request.GET.get("item_name", "").strip()

    # If a search query exists, search for items
    if item_name:
        # First try exact match (case-insensitive)
        try:
            item = CanteenItems.objects.get(item_name__iexact=item_name)
            # Build the URL and redirect
            detail_url = reverse("snack_detail", kwargs={"item_name": item.item_name})
            return redirect(detail_url)
        except CanteenItems.DoesNotExist:
            # If no exact match, use Django filters for contains search
            filter_set = CanteenItemsFilter(request.GET, queryset=CanteenItems.objects.all())
            items = filter_set.qs

            # If any results are found, redirect to the first one
            if items.exists():
                item = items.first()
                detail_url = reverse("snack_detail", kwargs={"item_name": item.item_name})
                return redirect(detail_url)
            # If no results, fall through to render home page

    # Render the home page template
    return render(request, "Home.html")


def snack_detail(request, item_name):
    """
    Detail page view that displays information about a specific snack.
    Handles URL-encoded item names and case-insensitive lookups.
    """
    try:
        # Get the snack item (case-insensitive lookup)
        # This handles URL encoding automatically
        item = get_object_or_404(CanteenItems, item_name__iexact=item_name)

        # Calculate rating_int for star display
        if item.rating_out_of_5 is not None:
            rating_int = int(float(item.rating_out_of_5))
        else:
            rating_int = 0

        # Pass item and rating_int to template
        context = {
            "item": item,
            "rating_int": rating_int,
        }

        return render(request, "details.html", context)

    except Http404:
        # If item not found, redirect back to home
        return redirect("home")


