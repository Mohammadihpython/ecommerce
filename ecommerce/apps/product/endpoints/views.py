from django.db.models import Prefetch
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from ..models import (
    Brand,
    Category,
    Media,
    Product,
    ProductAttribute,
    ProductAttributeValue,
    ProductAttributeValues,
    ProductInventory,
    ProductType,
    ProductTypeAttribute,
    Stock,
)
from .serializers import (
    BrandSerializer,
    CategorySerializer,
    MediaSerializer,
    ProductAttributeSerializer,
    ProductAttributeValueSerializer,
    ProductAttributeValuesSerializer,
    ProductInventoryLightSerializer,
    ProductInventorySerializer,
    ProductSerializer,
    ProductTypeAttributeSerializer,
    ProductTypeSerializer,
    StockSerializer,
)
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest


class ProductByCategory(viewsets.GenericViewSet, mixins.RetrieveModelMixin):

    """
    API endpoint that returns products by category
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "category_slug"

    def retrieve(self, request, category_slug: str, *args, **kwargs):
        queryset = (
            self.queryset.annotate(
                similarity=Greatest(
                    TrigramSimilarity("category__slug", category_slug),
                    TrigramSimilarity("category__name", category_slug),
                )
            )
            .filter(similarity__gte=0.3)
            .order_by("-similarity")
        )

        serializer = ProductSerializer(
            queryset, context={"request": request}, many=True
        )
        return Response(serializer.data)


class AllProductViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin
):
    """
    API endpoint that returns all products and get one product with slug
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "slug"

    def retrieve(self, request, slug=None):
        queryset = Product.objects.filter(slug__icontains=slug)
        serializer = ProductSerializer(
            queryset,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)


class AllInventoryProductByProduct(viewsets.GenericViewSet, mixins.RetrieveModelMixin):

    """
    API endpoint that returns variant of products
    """

    serializer_class = ProductInventoryLightSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "productId"
    queryset = ProductInventory.objects.all()

    def retrieve(self, request, productId=None, *args, **kwargs):
        queryset = self.queryset.filter(  # type: ignore
            product_id=productId
        ).prefetch_related(
            Prefetch(
                "media_product_inventory",
                queryset=Media.objects.filter(is_feature=True),
                to_attr="filtered_media",
            )
        )
        serializer = ProductInventorySerializer(
            queryset,
            many=True,
            context={"request": request},
        )
        return Response(
            serializer.data,
        )


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = ProductSerializer


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = BrandSerializer


class ProductInventoryViewSet(viewsets.ModelViewSet):
    queryset = ProductInventory.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = ProductInventorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = CategorySerializer


class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = MediaSerializer


class Product_inventoryStockViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class ProductAttributeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer


class ProductAttributeValueViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = ProductAttributeValue.objects.all()
    serializer_class = ProductAttributeValueSerializer


class ProductTypeViewsets(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer


class StockViewsets(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class ProductAttributeValuesViewSets(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = ProductAttributeValues.objects.all()
    serializer_class = ProductAttributeValuesSerializer


class ProductTypeAttributeViewSets(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = ProductTypeAttribute.objects.all()
    serializer_class = ProductTypeAttributeSerializer


class InventoryProductDetailViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = ProductInventory.objects.select_related(
        "product_inventory"
    ).prefetch_related("media_product_inventory")

    serializer_class = ProductInventorySerializer
