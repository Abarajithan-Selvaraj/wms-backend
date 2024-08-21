"""
Tests for the mass properties API.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status           # type: ignore
from rest_framework.test import APIClient   # type: ignore

from core.models import MassProperties

from component.serializers import MassPropertiesSerializer


MASS_PROPERTIES_URL = reverse('component:massproperties-list')


def detail_url(mass_props_id):
    """Create and return a mass propeties detail URL."""
    return reverse('component:massproperties-detail', args=[mass_props_id])


def create_user(email='test@example.com', password='test123'):
    """Create a user with given parameters and return the same."""
    return get_user_model().objects.create_user(email=email, password=password)


def create_mass_properties(user, csys_name='DEFAULT'):
    """Create a mass property with given parameters and return the same."""
    mass_props = MassProperties.objects.create(user=user, csys_name=csys_name)
    return mass_props


class PublicMassPropertiesAPITests(TestCase):
    """Test unauthenticated mass properties API request."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test authentication is required to retrieve mass properties."""
        res = self.client.get(MASS_PROPERTIES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateMassPropertiesAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_mass_properties(self):
        """Test retrieving a list of mass properties."""
        create_mass_properties(user=self.user)
        create_mass_properties(user=self.user)

        res = self.client.get(MASS_PROPERTIES_URL)

        mass_props = MassProperties.objects.all().order_by('id')
        serializer = MassPropertiesSerializer(mass_props, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_mass_properties_list_limited_to_user(self):
        """Test that the list of mass_properties is limited to the authenticated user."""        # noqa: E501
        other_user = create_user(
            email='other@example.com',
            password='testpass123'
        )
        create_mass_properties(user=other_user)
        mass_props = create_mass_properties(
            user=self.user,
            csys_name='DEFAULT_OTHER_USER'
        )

        res = self.client.get(MASS_PROPERTIES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['csys_name'], mass_props.csys_name)
        self.assertEqual(res.data[0]['id'], mass_props.id)

    def test_update_ingrediant(self):
        """Test updating a mass properties."""
        mass_props = MassProperties.objects.create(user=self.user)

        payload = {'csys_name': 'ORIG_DEFAULT'}
        url = detail_url(mass_props.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        mass_props.refresh_from_db()
        self.assertEqual(mass_props.csys_name, payload['csys_name'])

    def test_delete_mass_properties(self):
        """Test deleting a component is successful."""
        mass_props = create_mass_properties(user=self.user)

        url = detail_url(mass_props.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            MassProperties.objects.filter(id=mass_props.id).exists()
        )
