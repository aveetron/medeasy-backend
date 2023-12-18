from rest_framework.generics import GenericAPIView
from rest_framework import permissions, status
from rest_framework.response import Response
from .serializers import *


class ProductApiView(GenericAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            products = Product.objects.filter(status=True)
            product_serializer = self.serializer_class(products,
                                                       many=True)
            return Response({
                "data": product_serializer.data,
                "response_message": "success",
                "response_code": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "data": {},
                "response_message": e.args[0],
                "response_code": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            payload = request.data
            if Product.objects.filter(name=payload["name"],
                                      status=True).exists():
                return Response({
                    "data": {},
                    "response_message": "Restaurant with this name already exists!",
                    "response_code": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_400_BAD_REQUEST)

            product_serializer = self.serializer_class(data=payload)
            if product_serializer.is_valid():
                product_serializer.save(status=True,
                                        created_by=request.user)
                return Response({
                    "data": product_serializer.data,
                    "response_message": "product created!",
                    "response_code": status.HTTP_201_CREATED
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    "data": {},
                    "response_message": product_serializer.errors,
                    "response_code": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "data": {},
                "response_message": e.args[0],
                "response_code": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)



class ProductDetailsApiView(GenericAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, product_guid):
        product = Product.objects.filter(guid=product_guid,
                                         status=True).last()

        if not product:
            return Response({
                "data": {},
                "response_message": "no product found!",
                "response_code": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

        product_serializer = self.serializer_class(product)
        return Response({
            "data": product_serializer.data,
            "response_message": "success",
            "response_code": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)

    def put(self, request, product_guid):
        payload = request.data
        product = Product.objects.filter(guid=product_guid,
                                         status=True).last()

        if not product:
            return Response({
                "data": {},
                "response_message": "no product found!",
                "response_code": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

        product_serializer = self.serializer_class(product, payload)
        if product_serializer.is_valid():
            product_serializer.save()
            return Response({
                "data": product_serializer.data,
                "response_message": "updated",
                "response_code": status.HTTP_200_OK
            })
        else:
            return Response({
                "data": {},
                "response_message": product_serializer.errors,
                "response_code": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_guid):
        product = Product.objects.filter(guid=product_guid,
                                         status=True).last()

        if not product:
            return Response({
                "data": {},
                "response_message": "no product found!",
                "response_code": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

        product.delete()
        return Response({
            "data": {},
            "response_message": "deleted",
            "response_code": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)


class ReviewApiView(GenericAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            product_quid = request.query_params.get("product_quid")
            reviews = Review.objects.filter(status=True,
                                            product__guid=product_quid)
            review_serializer = self.serializer_class(reviews,
                                                      many=True)
            return Response({
                "data": review_serializer.data,
                "response_message": "success",
                "response_code": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "data": {},
                "response_message": e.args[0],
                "response_code": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        # try:
            payload = request.data
            review_serializer = self.serializer_class(data=payload)
            if review_serializer.is_valid():
                review_serializer.save(status=True,
                                       created_by=request.user)
                return Response({
                    "data": review_serializer.data,
                    "response_message": "review created!",
                    "response_code": status.HTTP_201_CREATED
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    "data": {},
                    "response_message": review_serializer.errors,
                    "response_code": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_400_BAD_REQUEST)
        # except Exception as e:
        #     return Response({
        #         "data": {},
        #         "response_message": e.args[0],
        #         "response_code": status.HTTP_400_BAD_REQUEST
        #     }, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetailsApiView(GenericAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, review_guid):
        review = Review.objects.filter(guid=review_guid,
                                       status=True).last()

        if not review:
            return Response({
                "data": {},
                "response_message": "no review found!",
                "response_code": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

        review_serializer = self.serializer_class(review)
        return Response({
            "data": review_serializer.data,
            "response_message": "success",
            "response_code": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)

    def put(self, request, review_guid):
        payload = request.data
        review = Review.objects.filter(guid=review_guid,
                                       status=True).last()

        if not review:
            return Response({
                "data": {},
                "response_message": "no review found!",
                "response_code": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

        review_serializer = self.serializer_class(review, payload)
        if review_serializer.is_valid():
            review_serializer.save()
            return Response({
                "data": review_serializer.data,
                "response_message": "updated",
                "response_code": status.HTTP_200_OK
            })
        else:
            return Response({
                "data": {},
                "response_message": review_serializer.errors,
                "response_code": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, review_guid):
        review = Review.objects.filter(guid=review_guid,
                                         status=True).last()

        if not review:
            return Response({
                "data": {},
                "response_message": "no review found!",
                "response_code": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

        review.delete()
        return Response({
            "data": {},
            "response_message": "deleted",
            "response_code": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)