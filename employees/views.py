from django_filters import rest_framework as filters
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Employee
from .serializers import EmployeeSerializer
from rest_framework.pagination import PageNumberPagination

# Define a filter set for Employee
class EmployeeFilter(filters.FilterSet):
    department = filters.CharFilter(field_name='department', lookup_expr='iexact')
    role = filters.CharFilter(field_name='role', lookup_expr='iexact')

    class Meta:
        model = Employee
        fields = ['department', 'role']

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]  # Require authentication for all operations
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EmployeeFilter
    pagination_class = PageNumberPagination  # Set pagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # 201 Created
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # 400 Bad Request

    def retrieve(self, request, *args, **kwargs):
        try:
            employee = self.get_object()
            serializer = self.get_serializer(employee)
            return Response(serializer.data)  # 200 OK
        except Employee.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)  # 404 Not Found

    def update(self, request, *args, **kwargs):
        try:
            employee = self.get_object()
            serializer = self.get_serializer(employee, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)  # 200 OK
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # 400 Bad Request
        except Employee.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)  # 404 Not Found

    def destroy(self, request, *args, **kwargs):
        try:
            employee = self.get_object()
            employee.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)  # 204 No Content
        except Employee.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)  # 404 Not Found
