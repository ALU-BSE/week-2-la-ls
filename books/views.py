from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Book

# Create your views here.
def book_list(request):
    # Get search parameters
    search_query = request.GET.get('search', '')
    author_filter = request.GET.get('author', '')
    year_filter = request.GET.get('year', '')

    # Get per_page parameter (default to 5)
    per_page = request.GET.get('per_page', 5)
    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 5

    # Apply filters
    books = Book.objects.all().order_by('title')

    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) | 
            Q(author__icontains=search_query)
        )

    if author_filter:
        books = books.filter(author__icontains=author_filter)

    if year_filter:
        try:
            year = int(year_filter)
            books = books.filter(published_year=year)
        except ValueError:
            pass

    # Paginate results
    paginator = Paginator(books, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Prepare context with all necessary data
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'author_filter': author_filter,
        'year_filter': year_filter,
        'per_page': per_page,
        'per_page_options': [5, 10, 20, 50],
    }

    return render(request, 'books/book_list.html', context)
