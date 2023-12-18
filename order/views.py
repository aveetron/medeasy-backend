from rest_framework.generics import GenericAPIView
from rest_framework import permissions, status
from rest_framework.response import Response
from .serializers import *


class OrderApiView(GenericAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            orders = Order.objects.filter(created_by=request.user,
                                          status=True)
            order_serializer = self.serializer_class(orders,
                                                     many=True)
            return Response({
                "data": order_serializer.data,
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
            order_serializer = self.serializer_class(data=payload)
            if order_serializer.is_valid():
                order_serializer.save(status=True,
                                      created_by=request.user)
                return Response({
                    "data": order_serializer.data,
                    "response_message": "order created!",
                    "response_code": status.HTTP_201_CREATED
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    "data": {},
                    "response_message": order_serializer.errors,
                    "response_code": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "data": {},
                "response_message": e.args[0],
                "response_code": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailsApiView(GenericAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, order_guid):
        order = Order.objects.filter(guid=order_guid,
                                     status=True).last()

        if not order:
            return Response({
                "data": {},
                "response_message": "no order found!",
                "response_code": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

        order_serializer = self.serializer_class(order)
        return Response({
            "data": order_serializer.data,
            "response_message": "success",
            "response_code": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)

    def put(self, request, order_guid):
        payload = request.data
        order = Order.objects.filter(guid=order_guid,
                                       status=True).last()

        if not order:
            return Response({
                "data": {},
                "response_message": "no order found!",
                "response_code": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

        order_serializer = self.serializer_class(order, payload)
        if order_serializer.is_valid():
            order_serializer.save()
            return Response({
                "data": order_serializer.data,
                "response_message": "updated",
                "response_code": status.HTTP_200_OK
            })
        else:
            return Response({
                "data": {},
                "response_message": order_serializer.errors,
                "response_code": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, order_guid):
        order = Order.objects.filter(guid=order_guid,
                                     status=True).last()

        if not order:
            return Response({
                "data": {},
                "response_message": "no order found!",
                "response_code": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

        order.delete()
        return Response({
            "data": {},
            "response_message": "deleted",
            "response_code": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
