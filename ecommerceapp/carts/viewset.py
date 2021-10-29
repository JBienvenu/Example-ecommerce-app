from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT,
    HTTP_201_CREATED,
)

from carts import models
from carts.serializers import (
    CreateCartSerializer,
    CartResponseSerializer,
    AddProductSerializer,
)
from common.permissions import IsBuyer, IsCartOwner
from products.models import Product


class CartsViewset(viewsets.ViewSet):
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [IsAuthenticated]
        elif self.action == "create":
            permission_classes = [IsBuyer]
        elif self.action in ["update", "destroy", "add_product_to_cart"]:
            permission_classes = [IsCartOwner]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    @swagger_auto_schema(responses={200: CartResponseSerializer(many=True)})
    def list(self, request):
        queryset = models.Cart.objects.filter(owner=request.user)
        serializer = CartResponseSerializer(queryset, many=True)

        return Response(data=serializer.data, status=HTTP_200_OK)

    @swagger_auto_schema(
        request_body=CreateCartSerializer,
        responses={201: openapi.Response("The cart has been created")},
    )
    def create(self, request):
        serializer = CreateCartSerializer(data=request.data)
        if serializer.is_valid():
            models.Cart.objects.create(
                name=serializer.validated_data["name"], owner=self.request.user
            )

            return Response(status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={200: CartResponseSerializer()},
    )
    def retrieve(self, request, pk=None):
        queryset = models.Cart.objects.get(pk=pk)
        serializer = CartResponseSerializer(queryset)

        return Response(serializer.data, status=HTTP_200_OK)

    def destroy(self, request, pk=None):
        cart = models.Cart.objects.get(pk=pk)
        self.check_object_permissions(request, cart)
        cart.delete()

        return Response(status=HTTP_204_NO_CONTENT)

    @action(methods=["POST"], url_path="add-product", detail=True)
    @swagger_auto_schema(
        request_body=AddProductSerializer,
        responses={201: openapi.Response("The product has been added")},
    )
    def add_product_to_cart(self, request, pk=None):
        cart = models.Cart.objects.get(pk=pk)
        self.check_object_permissions(request, cart)
        serializer = AddProductSerializer(data=request.data)
        if serializer.is_valid():
            product_to_add = Product.objects.get(pk=serializer.validated_data["product_id"])
            cart.products.add(product_to_add)

            return Response(status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
