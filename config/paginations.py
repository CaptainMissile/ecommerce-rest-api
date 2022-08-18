from rest_framework import pagination


class PagePagination(pagination.PageNumberPagination):
    page_size = 10