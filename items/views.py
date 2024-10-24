from django.forms import ValidationError
from django.http import Http404
from rest_framework import generics, status, request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from .models import Item
from .serializers import ItemSerializer
from django.db import IntegrityError
from rest_framework.exceptions import NotFound

class ItemCreateView(generics.CreateAPIView):
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)

            item = serializer.save()
            return Response({"item": serializer.data}, status=status.HTTP_201_CREATED)
        
        except IntegrityError:
            return Response({"error": "Item already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        item_id = self.kwargs.get('pk')
        item = cache.get(f'item_{item_id}')
        if not item:
            try:
                item = self.get_object()
                cache.set(f'item_{item_id}', item)
            except Http404:
                return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(ItemSerializer(item).data)

    def update(self, request, *args, **kwargs):
        try:
            item = self.get_object()
        except Http404:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            item = self.get_object()
        except Http404:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        
        item.delete()
        return Response({"message": "Success"}, status=status.HTTP_204_NO_CONTENT)


