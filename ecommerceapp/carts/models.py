from django.db import models
from common.models import Base
from django.contrib.auth import get_user_model
from products.models import Product


class Cart(Base):
    name = models.CharField(max_length=80)
    owner = models.ForeignKey(
        get_user_model(), related_name="carts", on_delete=models.CASCADE
    )
    products = models.ManyToManyField(Product, related_name="carts")
