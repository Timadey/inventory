from rest_framework import generics, status
from rest_framework.response import Response
from items.models import Item
from items.serializers import SupplierWithItemsSerializer
from suppliers.serializers import SupplierSerializer
from suppliers.models import Supplier
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse

class ListCreateSupplierView(generics.ListCreateAPIView):
    """View to list and create a supplier"""
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()

    @extend_schema(
        summary="List all suppliers",
        auth=None,
        responses={200: SupplierSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new supplier",
        auth=None,
        request=SupplierSerializer,
        responses={201: SupplierSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class RetrieveUpdateDestroySupplierView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, and destroy a supplier"""
    serializer_class = SupplierSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'supplier'
    queryset = Supplier.objects.all()

    @extend_schema(
        summary="Retrieve a supplier",
        description="Get a particular supplier uisng it's ID",
        auth=None,
        responses={200: SupplierSerializer, 404: OpenApiResponse(description="Not found")}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Update a supplier",
        auth=None,
        description="Update a particular supplier uisng it's ID",
        request=SupplierSerializer,
        responses={200: SupplierSerializer, 404: OpenApiResponse(description="Not found")}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary="Partially update a supplier",
        description="Patch a particular supplier uisng it's ID",
        auth=None,
        request=SupplierSerializer,
        responses={200: SupplierSerializer, 404: OpenApiResponse(description="Not found")}
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a supplier",
        description="Delete a particular supplier uisng it's ID",
        auth=None,
        responses={204: OpenApiResponse(description="No content"), 404: OpenApiResponse(description="Not found")}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

class SupplierItemListCreateView(generics.RetrieveUpdateAPIView):
    """All items by a particular supplier"""
    serializer_class = SupplierWithItemsSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'supplier'
    queryset = Supplier.objects.all()

    @extend_schema(
        summary="Retrieve all items for a supplier",
        description="Get a particular supplier including their items",
        auth=None,
        responses={200: SupplierWithItemsSerializer, 404: OpenApiResponse(description="Not found")}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Update items for a supplier",
        description="Add an item to a supplier",
        auth=None,
        request=SupplierWithItemsSerializer,
        responses={200: SupplierWithItemsSerializer, 404: OpenApiResponse(description="Not found")},
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        items_id = request.data.get('items_id', [])
        for item_id in items_id:
            try:
                item = Item.objects.get(id=item_id)
                if item not in instance.items.all():
                    instance.items.add(item)
            except Item.DoesNotExist:
                return Response({'error': f'Item with id {item_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        self.perform_update(serializer)

        return Response(serializer.data)
    

class SupplierItemRemoveView(generics.UpdateAPIView):
    """Remove items from a supplier"""
    serializer_class = SupplierWithItemsSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'supplier'
    queryset = Supplier.objects.all()

    
    @extend_schema(
        summary="Remove items from a supplier",
        description="Remove an item from a particular supplier",
        auth=None,
        request=SupplierWithItemsSerializer,
        responses={204: OpenApiResponse(description="No content"), 404: OpenApiResponse(description="Not found")},
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        items_id = request.data.get('items_id', [])

        for item_id in items_id:
            try:
                item = Item.objects.get(id=item_id)
                if item in instance.items.all():
                    instance.items.remove(item)
            except Item.DoesNotExist:
                return Response({'error': f'Item with id {item_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
