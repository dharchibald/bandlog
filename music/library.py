from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Yields a list chunk of size n from list
def group(list, n):

  for i in range(0, len(list), n):
    yield list[i:i+n]


# Takes requested data and breaks it up into a number of pages,
# each with n pages
def pagebreak(request, data, n):

  paginator = Paginator(data, 1)
  page = request.GET.get('page')
  items = paginator.get_page(page)

  # Generate page numbers to provide a link to from current page
  page_span = 2

  last = paginator.num_pages
  index = items.number
  prev = (index - page_span) if index > page_span else 1
  next = (index + page_span) if index < (last - page_span) else last
  page_range = paginator.page_range[prev:next]

  return items, page_range
