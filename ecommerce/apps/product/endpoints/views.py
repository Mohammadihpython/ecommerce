from rest_framework import mixins, viewsets
from django.db.models import Prefetch
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)
from rest_framework.response import Response

from .serializers import (
    BrandSerializer,
    CategorySerializer,
    MediaSerializer,
    ProductAttributeSerializer,
    ProductAttributeValueSerializer,
    ProductAttributeValuesSerializer,
    ProductInventoryLightSerializer,
    ProductSerializer,
    ProductInventorySerializer,
    ProductTypeAttributeSerializer,
    ProductTypeSerializer,
    StockSerializer,
)
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


class ProductByCategory(mixins.ListModelMixin, viewsets.GenericViewSet):

    """
    API endpoint that returns products by category
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, slug=None, *args, **kwargs):
        queryset = self.queryset.filter(
            product__category__slug=slug,
        ).filter(is_default=True)

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
        queryset = Product.objects.filter(slug=slug)
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


class AllInventoryProductByProduct(mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    """
    API endpoint that returns variant of products
    """

    serializer_class = ProductInventoryLightSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        product_id = self.request.query_params.get("product_id")  # type: ignore
        return ProductInventory.objects.filter(product_id=product_id).prefetch_related(
            Prefetch(
                "product_inventory_media",
                queryset=Media.objects.filter(is_feature=True),
                to_attr="filtered_media",
            )
        )

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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
    ).prefetch_related("product_inventory_media")

    serializer_class = ProductInventorySerializer
