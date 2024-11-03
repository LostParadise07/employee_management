from rest_framework.pagination import PageNumberPagination

class EmployeePagination(PageNumberPagination):
    page_size = 10  # Limit to 10 employees per page
    page_size_query_param = 'page_size'  # Allow the client to set page size
    max_page_size = 100  # Maximum allowed page size
