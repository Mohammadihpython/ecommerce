import abc

from django.http import HttpResponse
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Q
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView

from ecommerce.apps.search.product_documents import ProductInventoryDocument

from .product_search_serializers import SearchProductInventorySerializer


class PaginatedElasticSearchAPIView(APIView, LimitOffsetPagination):
    serializer_class = None
    document_class = None
    client = Elasticsearch("http://localhost:9200")

    @abc.abstractmethod
    def generate_q_expression(self, query):
        """This method should be overridden
        and return a Q() expression."""

    def get(self, request):
        try:
            query = request.query_params.get("query")  # type: ignore
            q = self.generate_q_expression(query)
            search = self.document_class.search().query(q)  # type: ignore
            response = search.e

            print(f"Found {response.hits.total.value} hit(s) for query: '{query}'")

            results = self.paginate_queryset(response, request, view=self)
            serializer = self.serializer_class(results, many=True)  # type: ignore
            return self.get_paginated_response(serializer.data)
        except Exception as e:
            return HttpResponse(e, status=500)  # type: ignore


class SearchProductInventoryView(PaginatedElasticSearchAPIView):
    serializer_class = SearchProductInventorySerializer
    document_class = ProductInventoryDocument

    """
    the multi_match query builds on the
    match query to allow multi-field queries

    Q(): short way of creating a query instance
    fuzziness make a work if has wrong word
    """

    def generate_q_expression(self, query):
        q = Q(
            "multi_match",
            query=self.request.query_params.get("query"),  # type: ignore
            fields=["product__name", "description"],
            fuzziness="auto",
        )
        print(
            f"Generated Query: {q.to_dict()}"
        )  # Add this line to see the generated query
        return q
