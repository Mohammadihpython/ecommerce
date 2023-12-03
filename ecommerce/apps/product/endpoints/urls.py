from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"products", views.ProductViewSet)
router.register(r"brands", views.BrandViewSet)
router.register(r"product-inventory", views.ProductInventoryViewSet)
router.register(r"categories", views.CategoryViewSet)
router.register(r"media", views.MediaViewSet)
router.register(r"stock", views.Product_inventoryStockViewSet)
router.register(r"product-attributes", views.ProductAttributeViewSet)
router.register(r"product-attribute-values", views.ProductAttributeValueViewSet)
router.register(r"product-type", views.ProductTypeViewsets)
router.register(r"product-attribute-values", views.ProductAttributeValuesViewSets)
router.register(r"product-type-attributes", views.ProductTypeAttributeViewSets)
router.register(r"inventory-product-detail", views.InventoryProductDetailViewSet)
router.register(r"all-products", views.AllProductViewSet, basename="all-products")
router.register(
    r"all-inventory-product-by-product",
    views.AllInventoryProductByProduct,
    basename="all-inventory-product-by-product",
)
router.register(
    r"products-by-category", views.ProductByCategory, basename="products-by-category"
)
