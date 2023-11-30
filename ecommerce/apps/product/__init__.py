# # your_app/__init__.py
# import django
# django.setup()

# default_app_config = 'product.apps.ProductAppConfig'  # Replace with your actual AppConfig if used

# # Import signals to ensure they are connected
# # from ecommerce.apps.search import signals


from django.apps import AppConfig


def ready():
    # Import signals inside the ready function to ensure they are connected properly
    from ecommerce.apps.search import signals  # Import your signals here
