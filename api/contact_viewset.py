from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status
from api.models import Contact
from api.serializers import ContactSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

class ContactViewset(viewsets.ModelViewSet):
    
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    
    def get_permissions(self):
        # Allow anyone to submit a contact form
        if self.action == 'create_contact':
            return [AllowAny()]
        # Require authentication for viewing contacts (admin only)
        return [IsAuthenticated()]

    @action(detail=False, methods=['POST'], url_path='submit-contact')
    def create_contact(self, request):
        serializer = ContactSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Failed to submit contact form",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response({
            "success": True,
            "message": "Contact form submitted successfully. We will get back to you soon!",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['GET'], url_path='fetch-contacts')
    def fetch_contacts(self, request):
        contacts = self.get_queryset().order_by('-id')
        serializer = self.get_serializer(contacts, many=True)
        return Response({
            "success": True,
            "count": len(serializer.data),
            "contacts": serializer.data
        })
    
    @action(detail=True, methods=['GET'], url_path='contact-detail')
    def contact_detail(self, request, pk=None):
        contact = self.get_object()
        serializer = self.get_serializer(contact)
        return Response({
            "success": True,
            "contact": serializer.data
        })
    
    @action(detail=True, methods=['DELETE'], url_path='delete-contact')
    def delete_contact(self, request, pk=None):
        contact = self.get_object()
        contact_name = contact.name
        contact.delete()
        
        return Response({
            "success": True,
            "message": f"Contact from '{contact_name}' deleted successfully"
        }, status=status.HTTP_200_OK)