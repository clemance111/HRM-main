from rest_framework import serializers
from django.utils import timezone
from accounts.models import Employee,Department
class DashboardStatsSerializer(serializers.Serializer):
    total_employees=serializers.IntegerField()
    total_department=serializers.IntegerField()
    total_payslips=serializers.IntegerField()
    total_job_applies=serializers.IntegerField()
    employee_composition=serializers.DictField()

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Employee
        fields='__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Department
        fields='__all__'

class EmployeeListSerializer(serializers.ModelSerializer):
    department=serializers.SerializerMethodField()
    date_of_bith=serializers.SerializerMethodField()
    class Meta:
        model=Employee
        fields='__all__'
    def get_date_of_bith(self,obj):
        current_year=timezone.now().year
        employee_dob_year=obj.dob.year
        age=current_year-employee_dob_year
        return age
    def get_department(self,obj):
        department=Department.objects.filter(employees_id__in=[obj.id])
        return department.values_list('name',flat=True)
