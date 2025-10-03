from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from api.models import Category
from api.serializers import CategorySerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction


class CategoryViewSet(viewsets.ViewSet):
    """ViewSet for Category CRUD operations"""
    
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['POST'], url_path='create-category')
    @transaction.atomic
    def create_category(self, request):
        """Create a new category"""
        serializer = CategorySerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Failed to create category",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        
        return Response({
            "success": True,  # Fixed: was False
            "message": "Category created successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['PATCH'], url_path='update-category')
    @transaction.atomic
    def update_category(self, request, pk=None):
        """Update existing category"""
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        
        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": f"Category update failed",  # Fixed: removed self.pk
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)  # Added status code
        
        serializer.save()
        
        return Response({
            "success": True,
            "message": f"Category '{category.name}' updated successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['DELETE'], url_path='delete-category')
    @transaction.atomic
    def delete_category(self, request, pk=None):
        """Delete category"""
        category = get_object_or_404(Category, pk=pk)
        category_name = category.name  
        blog_count = category.blogs.count()
        if blog_count > 0:
            return Response({
                "success": False,
                "message": f"Cannot delete category. It has {blog_count} associated blog(s)",
                "suggestion": "Please reassign or delete the associated blogs first"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        category.delete()
        
        return Response({
            "success": True,
            "message": f"Category '{category_name}' deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'], url_path='fetch-all')
    def fetch_all(self, request):
        """Fetch all categories"""
        categories = Category.objects.all().order_by('name')
        serializer = CategorySerializer(categories, many=True)

        return Response({
            "success": True,
            "message": "All categories fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)