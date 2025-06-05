import abc

from elasticsearch import Elasticsearch

from elasticsearch.dsl import Q
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView

from ecommerce.apps.product.documents import ProductInventoryDocument

from ..product.endpoints.serializers import ProductInventorySerializer


class PaginatedElasticSearchAPIView(APIView, LimitOffsetPagination):
    serializer_class = None
    document_class = None
    client = Elasticsearch("http://localhost:9200")

    @abc.abstractmethod
    def generate_q_expression(self, query):
        """This method should be overridden
        and return a Q() expression."""

    def get(self, request):
        query = request.query_params.get("query")  # type: ignore
        q = self.generate_q_expression(query)
        search = self.document_class.search().query(q)  # type: ignore
        response = search.execute()

        # pprint(f"Found {response.hits.hits} hit(s) for query: '{query}'")

        results = self.paginate_queryset(response, request, view=self)
        serializer = self.serializer_class(results, many=True)  # type: ignore
        return self.get_paginated_response(serializer.data)
        # return Response(serializer.data)


class SearchProductInventoryView(PaginatedElasticSearchAPIView):
    serializer_class = ProductInventorySerializer
    document_class = ProductInventoryDocument

    """
    the multi_match query builds on the
    match query to allow multi-field queries

    Q(): short way of creating a query instance
    fuzziness make a work if has wrong word
    """

    def generate_q_expression(self, query):
        return Q(
            "multi_match",
            query=self.request.query_params.get("search"),  # type: ignore
            fields=["product.name", "product.description"],
            fuzziness="auto",
        )
