from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import ContactSubmission, DonationSubmission, Feedback
from .serializers import ContactSubmissionSerializer, DonationSubmissionSerializer, FeedbackSerializer


class ContactSubmissionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for contact form submissions

    Only allows creating new submissions (POST) for public
    Admin access required for list/retrieve operations
    """
    queryset = ContactSubmission.objects.all()
    serializer_class = ContactSubmissionSerializer
    http_method_names = ['post', 'get', 'head', 'options']

    def get_permissions(self):
        """
        Allow anyone to create (POST), but require authentication for list/retrieve
        """
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        """Handle contact form submission"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Capture metadata
        ip_address = self.get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        # Save with metadata
        contact = serializer.save(
            ip_address=ip_address,
            user_agent=user_agent
        )

        # Return success response
        return Response({
            'success': True,
            'message': 'Thank you for contacting us! We will respond within 48 hours.',
            'id': contact.id
        }, status=status.HTTP_201_CREATED)

    def get_client_ip(self, request):
        """Get client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class DonationSubmissionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for donation form submissions

    Only allows creating new submissions (POST) for public
    Admin access required for list/retrieve operations
    """
    queryset = DonationSubmission.objects.all()
    serializer_class = DonationSubmissionSerializer
    http_method_names = ['post', 'get', 'head', 'options']

    def get_permissions(self):
        """
        Allow anyone to create (POST), but require authentication for list/retrieve
        """
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        """Handle donation form submission"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Capture metadata
        ip_address = self.get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        # Save with metadata
        donation = serializer.save(
            ip_address=ip_address,
            user_agent=user_agent
        )

        # Return success response
        return Response({
            'success': True,
            'message': 'Thank you for your donation! We will process your submission shortly.',
            'id': donation.id
        }, status=status.HTTP_201_CREATED)

    def get_client_ip(self, request):
        """Get client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class FeedbackViewSet(viewsets.ModelViewSet):
    """
    ViewSet for feedback submissions from Citizens Voice page

    Only allows creating new submissions (POST) for public
    Admin access required for list/retrieve operations
    """
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    http_method_names = ['post', 'get', 'head', 'options']

    def get_permissions(self):
        """
        Allow anyone to create (POST), but require authentication for list/retrieve
        """
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        """Handle feedback form submission"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Capture metadata
        ip_address = self.get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        # Save with metadata
        feedback = serializer.save(
            ip_address=ip_address,
            user_agent=user_agent
        )

        # Return success response
        return Response({
            'success': True,
            'message': 'Thank you for your feedback! We appreciate your input.',
            'id': feedback.id
        }, status=status.HTTP_201_CREATED)

    def get_client_ip(self, request):
        """Get client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip