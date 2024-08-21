"""
Serializers for Component APIs
"""

from rest_framework import serializers       # type: ignore

from core.models import Component


class ComponentSerializer(serializers.ModelSerializer):
    """Serializer for Component object."""

    class Meta:
        model = Component
        fields = ['id', 'name', 'parent', 'version', 'type', 'level', 'index']
        read_only_fields = ['id']


class ComponentDetailSerializer(ComponentSerializer):
    """Serializer for Component object detail view."""

    class Meta(ComponentSerializer.Meta):
        fields = ComponentSerializer.Meta.fields + ['description']
