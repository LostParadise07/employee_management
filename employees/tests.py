# myapp/tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Employee
from django.contrib.auth import get_user_model

User = get_user_model()

class EmployeeTests(APITestCase):
    def setUp(self):
        # Create a sample user for testing
        self.user = User.objects.create_user(username='admin', password='admin')

        # Log in to get the token
        response = self.client.post(reverse('token_obtain_pair'), {
            'username': 'admin',
            'password': 'admin'
        })
        self.token = response.data['access']  # Store the access token

        # Create a sample employee for testing
        self.employee = Employee.objects.create(
            name="John Doe",
            email="john.doe@example.com",
            department="HR",
            role="Manager"
        )

    def test_create_employee(self):
        url = reverse('employee-list')  # Adjust to your URL pattern name
        data = {
            "name": "Jane Doe",
            "email": "jane.doe@example.com",
            "department": "Engineering",
            "role": "Developer"
        }
        # Include the token in the header
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_employee_not_found(self):
        url = reverse('employee-detail', args=[999])  # Use a non-existent ID
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_employee_with_existing_email(self):
        url = reverse('employee-list')
        data = {
            "name": "Another Employee",
            "email": "john.doe@example.com",  # This email already exists
            "department": "Engineering",
            "role": "Developer"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # Assuming email validation fails
