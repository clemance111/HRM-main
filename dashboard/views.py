from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from dashboard.serializers import DashboardStatsSerializer,EmployeeSerializer,DepartmentSerializer,EmployeeListSerializer
from accounts.models import Employee, Department, PaySlip, JobApplication


class DashboardAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        total_employees = Employee.objects.count()
        total_department = Department.objects.count()
        total_payslips = PaySlip.objects.count()
        total_job_applies = JobApplication.objects.count()
        females=Employee.objects.filter(gender=Employee.FEMALE).count()
        males=Employee.objects.filter(gender=Employee.MALE).count()
        composition={
            "males":males,
            "females":females
        }
        data = {
            "total_employees": total_employees,
            "total_department": total_department,
            "total_payslips": total_payslips,
            "total_job_applies": total_job_applies,
            "employee_composition":composition
        }
        serializer=DashboardStatsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data,status=200)

class EmployeesViewset(ModelViewSet):
    queryset=Employee.objects.all()
    permission_classes=[IsAuthenticated]
    serializer_class=EmployeeSerializer

class DepartmentViewSet(ModelViewSet):
    queryset=Department.objects.all()
    permission_classes=[IsAuthenticated]
    serializer_class=DepartmentSerializer

class EmployeeStatusAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        query=Employee.objects.all()
        serializer=EmployeeListSerializer(query,many=True)
        return Response(serializer.data,status=200)
