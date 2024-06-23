from items.serializers import ItemSerializer, ItemSupplierSerializer
from suppliers.models import Supplier
from items.models import Item
from rest_framework import generics, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse

class ListCreateItemView(generics.ListCreateAPIView):
    """View to list and create an item"""
    serializer_class = ItemSerializer
    queryset = Item.objects.all()

    @extend_schema(
        summary="List all items",
        auth=None,
        responses={200: ItemSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new item",
        auth=None,
        request=ItemSerializer,
        responses={201: ItemSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class RetrieveUpdateDestroyItemView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, and destroy an item"""
    serializer_class = ItemSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'item'
    queryset = Item.objects.all()

    @extend_schema(
        summary="Retrieve an item",
        auth=None,
        responses={200: ItemSerializer, 404: OpenApiResponse(description="Item not found")}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Update an item",
        auth=None,
        request=ItemSerializer,
        responses={200: ItemSerializer, 404: OpenApiResponse(description="Item not found")}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary="Partially update an item",
        auth=None,
        request=ItemSerializer,
        responses={200: ItemSerializer, 404: OpenApiResponse(description="Item not found")}
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary="Delete an item",
        auth=None,
        responses={204: OpenApiResponse(description="No content"), 404: OpenApiResponse(description="Item not found")}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

class ItemSupplierRetrieveView(generics.RetrieveUpdateAPIView):
    """Get an Item including all its suppliers"""
    serializer_class = ItemSupplierSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'item'
    queryset = Item.objects.all()

    @extend_schema(
        summary="Retrieve an item with its suppliers",
        auth=None,
        responses={200: ItemSupplierSerializer, 404: OpenApiResponse(description="Item not found")}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Update the suppliers for an item",
        auth=None,
        request=ItemSupplierSerializer,
        responses={200: ItemSupplierSerializer, 404: OpenApiResponse(description="Not found")},
        parameters=[
            OpenApiParameter(name="suppliers", 
                             description="List of supplier IDs to add to the item", 
                             required=True, 
                             type={"type": "array", "items": {"type": "string", "format": "uuid"}})
        ],
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        suppliers = request.data.get('suppliers', [])
        for supplier_id in suppliers:
            try:
                supplier = Supplier.objects.get(id=supplier_id)
                if supplier not in instance.suppliers.all():
                    instance.suppliers.add(supplier)
            except Supplier.DoesNotExist:
                return Response({'error': f'Supplier with id {supplier_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        self.perform_update(serializer)

        return Response(serializer.data)

class ItemSupplierRemoveView(generics.UpdateAPIView):
    """Remove a supplier from an item """
    serializer_class = ItemSupplierSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'item'
    queryset = Item.objects.all()


    @extend_schema(
        summary="Remove suppliers from an item",
        auth=None,
        description="Remove supplier(s) from the supplier list of an item",
        request=ItemSupplierSerializer,
        responses={204: OpenApiResponse(description="No content"), 404: OpenApiResponse(description="Not found")},
        parameters=[
            OpenApiParameter(name="suppliers", 
                             description="List of supplier IDs to remove from the item", 
                             required=True, 
                             type={"type": "array", "items": {"type": "string", "format": "uuid"}})
        ]
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        suppliers = request.data.get('suppliers', [])

        for supplier_id in suppliers:
            try:
                supplier = Supplier.objects.get(id=supplier_id)
                if supplier in instance.suppliers.all():
                    instance.suppliers.remove(supplier)
            except Supplier.DoesNotExist:
                return Response({'error': f'Supplier with id {supplier_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)

        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
