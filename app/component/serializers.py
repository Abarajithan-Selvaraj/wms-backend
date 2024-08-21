"""
Serializers for Component APIs
"""

from rest_framework import serializers       # type: ignore

from core.models import Component, MassProperties


class MassPropertiesSerializer(serializers.ModelSerializer):
    """Serializer for Mass Properties object."""

    class Meta:
        model = MassProperties
        fields = [
            'id', 'csys_name', 'xform_matrix', 'position', 'mass', 'cog_lsl',
            'cog_usl',
        ]
        read_only_fields = ['id']


class ComponentSerializer(serializers.ModelSerializer):
    """Serializer for Component object."""
    mass_properties = MassPropertiesSerializer(many=True, required=False)

    class Meta:
        model = Component
        fields = [
            'id', 'name', 'parent', 'version', 'type', 'level', 'index',
            'skeleton', 'mass_properties',
        ]
        read_only_fields = ['id']

    def _get_or_create_mass_properties(self, mass_properties, component):
        """Handle getting or creating mass properties as needed."""
        auth_user = self.context['request'].user
        for mp in mass_properties:
            mp_obj, create = MassProperties.objects.get_or_create(
                user=auth_user,
                **mp
            )
            component.mass_properties.add(mp_obj)

    def create(self, validated_data):
        """Create a new Component object."""
        mass_properties = validated_data.pop('mass_properties', [])
        component = Component.objects.create(**validated_data)
        self._get_or_create_mass_properties(mass_properties, component)

        return component

    def update(self, instance, validated_data):
        """Update an existing Component object."""
        mass_properties = validated_data.pop('mass_properties', None)
        if mass_properties is not None:
            instance.mass_properties.clear()
            self._get_or_create_mass_properties(mass_properties, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class ComponentDetailSerializer(ComponentSerializer):
    """Serializer for Component object detail view."""

    class Meta(ComponentSerializer.Meta):
        fields = ComponentSerializer.Meta.fields + ['description']
