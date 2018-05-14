from django.shortcuts import render

from django.http import HttpResponse, Http404

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, Review
from .serializers import ProductSerializers, ReviewSerializers
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly

from rest_framework.permissions import IsAuthenticatedOrReadOnly

## Create your views here.

## Class based View, APIView Class and also have Json response implimented


# class ProductList(APIView):
#
#     def get(self, request, format=None):
#         products= Product.objects.all()
#         serializer= ProductSerializers(products, many=True)
#         return Response(serializer.data)
#

### There is also another way of writing the same view. Let's try it with ListAPIView.

# class ProductList(generics.ListAPIView):
#     queryset= Product.objects.all()
#     serializer_class= ProductSerializers


# class ProductList(APIView):
#
#     def get(self, request, format=None):
#             products= Product.objects.all()
#             serializer= ProductSerializers(products, many=True)
#             return Response(serializer.data)
#
#
#     def post(self, request, format=None):
#         serializer= ProductSerializers(data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#


class ProductList(generics.ListCreateAPIView):
    queryset= Product.objects.all()
    serializer_class= ProductSerializers
    permission_classes= (IsAdminOrReadOnly,)
    lookup_url_kwarg= 'product_id'



## Creating view with APIView

# class ProductDetail(APIView):
#
#     def get_object(self, pk):
#
#         try:
#             return Product.objects.get(pk=pk)
#         except Product.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         product = self.get_object(pk)
#         serializer = ProductSerializers(product)
#         return Response(serializer.data)
#
#
#     def put(self, request, pk, format=None):
#         product = self.get_object(pk)
#         serializer = ProductSerializers(product, data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         product= self.get_object(pk)
#         product.delete()
#         return Response(status= status.HTTP_204_NO_CONTENT)

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset= Product.objects.all()
    serializer_class=ProductSerializers
    permission_classes= (IsAdminOrReadOnly,)
    lookup_url_kwarg = 'product_id'


class ReviewList(generics.ListCreateAPIView):
    # queryset= Review.objects.all()
    serializer_class = ReviewSerializers
    permission_classes= (IsAuthenticatedOrReadOnly, )
    lookup_url_kwarg= 'product_id'


    def perform_create(self, serializer):
        print(self.request.user.id)
        serializer.save(
            created_by= self.request.user,
            product_id= self.kwargs['product_id']
        )

    def get_queryset(self):
        product=self.kwargs['product_id']
        return Review.objects.filter(product_id=product)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class= ReviewSerializers
    permission_classes= (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    lookup_url_kwarg= 'review_id'

    def get_queryset(self):
        review= self.kwargs['review_id']
        return Review.objects.filter(id=review)