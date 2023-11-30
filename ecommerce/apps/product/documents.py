from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import ProductInventory


@registry.register_document
class ProductInventoryDocument(Document):
    product = fields.NestedField(
        properties={
            "category": fields.ObjectField(properties={"name": fields.TextField()}),
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
    media_product_inventory = fields.ObjectField(
        properties={
            "imf_url": fields.KeywordField(),
        }
    )
    product_type = fields.NestedField(
        properties={
            "name": fields.TextField(),
            "product_type_attribute": fields.ObjectField(
                properties={
                    "name": fields.TextField(),
                    "description": fields.TextField(),
                }
            ),
        }
    )

    attribute_values = fields.NestedField(
        properties={
            "attribute_value": fields.TextField(),
            "product_attribute": fields.ObjectField(
                properties={
                    "name": fields.TextField(),
                    "description": fields.TextField(),
                }
            ),
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
            "sale_price",
            "store_price",
            "is_default",
            "retail_price",
        ]
