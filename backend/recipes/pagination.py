from rest_framework.pagination import PageNumberPagination
from rest_framework.views import Response


class PageNumberPaginationDataOnly(PageNumberPagination):

    def get_paginated_response(self, data):
        return Response(data)


class CustomPagination(PageNumberPagination):
    page_size_query_param = "limit"
