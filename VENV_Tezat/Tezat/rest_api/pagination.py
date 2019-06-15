from rest_framework.pagination import (
    PageNumberPagination,
    )
from rest_framework.response import  Response


class CommentPageNumberPagination(PageNumberPagination):
    page_size = 15
   # def get_paginated_response(self, data):
   #    return Response(data)

class ReplyPageNumberPagination(PageNumberPagination):
    page_size = 5