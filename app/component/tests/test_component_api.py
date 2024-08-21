"""
Tests for component API.
"""

# from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient     # type: ignore
from rest_framework import status             # type: ignore

from core.models import Component

from component.serializers import (
    ComponentSerializer,
    ComponentDetailSerializer,
)


COMPONENT_URL = reverse('component:component-list')


def detail_url(component_id):
    """Create and return a component detail URL."""
    return reverse('component:component-detail', args=[component_id])


def create_component(user, **params):
    """Create a component with given parameters and return the same."""
    defaults = {
        'name': 'Sample Component',
        'description': 'Sample Component Description',
        'parent': 'NULL',
        'version': '0.0',
        'type': 'component',
        'level': 0,
        'index': 0
    }
    defaults.update(params)

    component = Component.objects.create(user=user, **defaults)
    return component


def create_user(**params):
    """Create a user with given parameters and return the same."""
    return get_user_model().objects.create_user(**params)


class PublicComponentAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(COMPONENT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateComponentAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_components(self):
        """Test retrieving a list of components."""
        create_component(user=self.user)
        create_component(user=self.user)

        res = self.client.get(COMPONENT_URL)

        components = Component.objects.all().order_by('id')
        serializer = ComponentSerializer(components, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_components_list_limited_to_user(self):
        """Test that the list of components is limited to the authenticated user."""        # noqa: E501
        other_user = create_user(
            email='other@example.com',
            password='testpass123'
        )
        create_component(user=other_user)
        create_component(user=self.user)

        res = self.client.get(COMPONENT_URL)

        components = Component.objects.filter(user=self.user)
        serializer = ComponentSerializer(components, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_component_detail(self):
        """Test retrieving a component's detail view."""
        component = create_component(user=self.user)

        url = detail_url(component.id)
        res = self.client.get(url)

        serializer = ComponentDetailSerializer(component)
        self.assertEqual(res.data, serializer.data)

    def test_create_component(self):
        """Test creating a component."""
        payload = {
            'name': 'Test Component 1',
            'version': '1.0',
            'type': 'PART',
            'level': 0,
            'index': 0
        }
        res = self.client.post(COMPONENT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        component = Component.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(component, k), v)

        self.assertEqual(component.user, self.user)

    def test_partial_update(self):
        """Test partial update of a component."""
        original_desc = 'The Original Component Description'
        component = create_component(
            user=self.user,
            name="Original Component",
            description=original_desc
        )

        payload = {'name': 'New Updated Component'}
        url = detail_url(component.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        component.refresh_from_db()
        self.assertEqual(component.name, payload['name'])
        self.assertEqual(component.description, original_desc)
        self.assertEqual(component.user, self.user)

    def test_full_update(self):
        """Test full update of a component."""
        component = create_component(
            user=self.user,
            name='Original Component',
            version='1.0',
            type='PART',
            level=0,
            index=0,
            description='The Original Component Description'
        )

        payload = {
            'name': 'New Updated Component',
            'parent': 'New Parent Component',
            'version': '1.4',
            'type': 'PART',
            'level': 2,
            'index': 4,
            'description': 'The New Updated Component Description'
        }
        url = detail_url(component.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        component.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(component, k), v)

        self.assertEqual(component.user, self.user)

    def test_update_user_returns_error(self):
        """Test that changing the user of a component results in an error."""
        new_user = create_user(email='user2@example.com', password='test123')
        component = create_component(user=self.user)

        payload = {'user': new_user.id}
        url = detail_url(component.id)
        self.client.patch(url, payload)

        component.refresh_from_db()
        self.assertEqual(component.user, self.user)

    def test_delete_component(self):
        """Test deleting a component is successful."""
        component = create_component(user=self.user)

        url = detail_url(component.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Component.objects.filter(id=component.id).exists())

    def test_delete_other_users_component_error(self):
        """Test deleting a component created by another user throws error."""
        new_user = create_user(email='user2@example.com', password='test123')
        component = create_component(user=new_user)

        url = detail_url(component.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Component.objects.filter(id=component.id).exists())
