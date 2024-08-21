"""
Views for the Component APIs.
"""

from rest_framework import viewsets                                 # type: ignore  # noqa: E501
from rest_framework.authentication import TokenAuthentication       # type: ignore  # noqa: E501
from rest_framework.permissions import IsAuthenticated              # type: ignore  # noqa: E501

from core.models import Component
from component import serializers


class ComponentViewSet(viewsets.ModelViewSet):
    """View for manage component APIs."""
    serializer_class = serializers.ComponentDetailSerializer
    queryset = Component.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve the component for the authenticated user."""
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.ComponentSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new component."""
        serializer.save(user=self.request.user)
