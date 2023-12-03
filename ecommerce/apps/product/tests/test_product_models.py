import pytest


@pytest.mark.django_db
def test_category_model(db, category_factory):
    category = category_factory.build()
    assert str(category) == category.name


@pytest.mark.django_db
def test_product_model(db, product_factory):
    product = product_factory.build()
    assert str(product) == product.name


@pytest.mark.django_db
def test_product_attribute_model(db, product_attribute_factory):
    product_att = product_attribute_factory.build()
    assert str(product_att) == product_att.name


@pytest.mark.django_db
def test_product_type_model(db, product_type_factory):
    product_type = product_type_factory.build()
    assert str(product_type) == product_type.name


@pytest.mark.django_db
def test_brand_model(db, brand_factory):
    brand = brand_factory.build()
    assert str(brand) == brand.name


@pytest.mark.django_db
def test_product_attribute_value_model(
    db, product_attribute_factory, attribute_value_factory
):
    pt = product_attribute_factory.create()
    p = attribute_value_factory(product_attribute=pt)
    assert str(p) == f"{p.pt.name} : {p.attribute_value}"


@pytest.mark.django_db
def test_product_inventory_model(db, product_factory, product_inventory_factory):
    product = product_factory.create()
    inventory_product = product_inventory_factory(product=product)
    assert str(inventory_product) == inventory_product.product.name
