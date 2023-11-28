from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from ..product.models import Product, ProductInventory


@registry.register_document
class ProductDocument(Document):
    category = fields.ObjectField(
        properties={
            "parent": fields.TextField(),
            "name": fields.TextField(),
        }
    )

    class Index:
        name = "products"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }

    class Django:
        model = Product
        """
        this fields must same with fields in your serializer
        """
        fields = [
            "slug",
            "name",
            "web_id",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        ]

    # def prepare_category(self, instance):
    #     if instance.category:
    #         return {
    #             "parent": instance.category.parent.name
    #             if instance.category.parent
    #             else None,
    #             "name": instance.category.name,
    #         }
    #     return {}


@registry.register_document
class ProductInventoryDocument(Document):
    product = fields.ObjectField(
        properties={
            "name": fields.TextField(),
            "description": fields.TextField(),
            "slug": fields.TextField(),
        }
    )
    brand = fields.ObjectField(
        properties={
            "name": fields.TextField(),
        }
    )

    class Index:
        name = "inventory_products"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }

    class Django:
        model = ProductInventory
        """
        this fields must same with fields in your serializer
        """
        fields = [
            "id",
            "retail_price",
            "store_price",
            "sale_price",
            "weight",
            "created_at",
            "updated_at",
        ]
        # related_models = [Product,Brand]

    # def get_queryset(self):
    #     return super(ProductInventoryDocument, self).get_queryset().select_related(
    #         'product',
    #     )

    # def get_instances_from_related(self, related_instance):
    #     if isinstance(related_instance, Product):
    #         return related_instance.product.all()


products = ProductInventoryDocument.search(index="inventory_products").query(
    "match", product_name="product_11"
)
