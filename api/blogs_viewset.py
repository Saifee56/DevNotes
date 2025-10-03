from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets,status
from api.models import Category,Blogs
from api.serializers import CategorySerializer,BlogsSerializer,CommentSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

class BlogsViewset(viewsets.ModelViewSet):
    
    permission_classes=[IsAuthenticated]
    queryset=Blogs.objects.all()
    serializer_class = BlogsSerializer


    @action(detail=False,methods=['POST'],url_path='create-blogs')
    def create_blogs(self,request):
        category_id=request.data.get('category')

        if not category_id:
            return Response({
                "message":"Category ID is required"
            })
        data=request.data
        serializer=BlogsSerializer(data=data,context={'request': request})
        if not serializer.is_valid():
            return Response({
                "success":False,
                "message":"Failed to create blog",
                "errors":serializer.errors
            })
        serializer.save(user=request.user)
        return Response({
            "success":True,
            "message":f"Blog created by successfully",
            "data":serializer.data
        })
    
    @action(detail=True,methods=['PATCH'],url_path='like-blog')
    def like_blog(self,request,pk=None):
        blog=get_object_or_404(Blogs,pk=pk)
        user=request.user

        if user in blog.likes.all():
            blog.likes.remove(user)
            message="Blogs unliked"
        else:
            blog.likes.add(user)
            message=f"{blog.title} liked by {user}"
        return Response(
            {
                "success":True,
                "message":message,
                "total_likes":blog.likes.count()
            }
        )
    @action(detail=False, methods=['GET'], url_path='fetch-blogs')
    def fetch_blogs(self, request):
        blogs = self.get_queryset().order_by('-time') 
        serializer = self.get_serializer(blogs, many=True)
        return Response({
            "success": True,
            "count": len(serializer.data),
            "blogs": serializer.data
        })
    
    @action(detail=True, methods=['PATCH'], url_path='comment')
    def comment(self, request, pk=None):
        blog = get_object_or_404(Blogs, pk=pk)
        serializer = CommentSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Failed to comment",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        comment = serializer.save(user=request.user, blogs=blog)

        # Serialize again to include user field properly
        comment_data = CommentSerializer(comment).data

        return Response({
            "success": True,
            "message": "Comment added successfully",
            "comment": comment_data
        }, status=status.HTTP_201_CREATED)

    
    @action(detail=True,methods=['PATCH'],url_path='update-blog')
    def update_blog(self,request,pk=None):
        blog=get_object_or_404(Blogs,pk=pk)

        if blog.user != request.user:
            return Response({
                "success":False,
                "message":"You do not have permission to update this blog",
            
            },status=status.HTTP_403_FORBIDDEN)
        serializer=BlogsSerializer(blog,data=request.data,partial=True)
        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Failed to update blog",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    
        serializer.save()
        return Response({
            "success": True,
            "message": "Blog updated successfully",
            "data": serializer.data
        })
    
    @action(detail=True, methods=['DELETE'], url_path='delete-blog')
    def delete_blog(self, request, pk=None):
        blog = get_object_or_404(Blogs, pk=pk)
        
        if blog.user != request.user:
            return Response({
                "success": False,
                "message": "You do not have permission to delete this blog"
            }, status=status.HTTP_403_FORBIDDEN)
        
        blog_title = blog.title
        blog.delete()
        
        return Response({
            "success": True,
            "message": f"Blog '{blog_title}' deleted successfully"
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['GET'], url_path='fetch-user-blogs')
    def fetch_user_blogs(self, request):
        """
        Fetch blogs created by the logged-in user only.
        """
        user = request.user
        blogs = self.get_queryset().filter(user=user).order_by('-time')
        serializer = self.get_serializer(blogs, many=True)
        return Response({
            "success": True,
            "count": blogs.count(),
            "blogs": serializer.data
        })