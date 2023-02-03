from django.urls import path
from rest_framework.routers import DefaultRouter
from dashboard.views import (DashboardAPI, EmployeeStatusAPI,
                             DepartmentViewSet,
                             EmployeesViewset
                             )
router=DefaultRouter()
router.register('employees',EmployeesViewset)
router.register('departments',DepartmentViewSet)
urlpatterns = [
    path('stats', DashboardAPI.as_view(), name="dashboard_stats"),
    path('employee-status', EmployeeStatusAPI.as_view(), name="employee_status")
]+router.urls
