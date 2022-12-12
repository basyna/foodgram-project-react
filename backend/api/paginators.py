from rest_framework.pagination import PageNumberPagination


class PageLimitPagination(PageNumberPagination):
    """Переопределение параметра размера страницы."""
    page_size_query_param = 'limit'
