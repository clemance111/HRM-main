from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, gender, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email), first_name=first_name, last_name=last_name, **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
            **extra_fields
        )
        user.staff = True
        user.is_active = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})


class User(AbstractBaseUser):
    HR = "HR"
    EMPLOYEE = "EMPLOYEE"
    USER_TYPE_CHOICES = (
        (HR, "Human Resource"),
        (EMPLOYEE, "Employees"),
    )
    MALE = "M"
    FEMALE = "F"
    GENDER_CHOICES = (
        (MALE, "Male"),
        (FEMALE, "Female"),
    )
    first_name = models.CharField(null=True, max_length=50)
    last_name = models.CharField(null=True, max_length=50)
    email = models.EmailField(unique=True, max_length=254)
    user_type = models.CharField(
        max_length=50, choices=USER_TYPE_CHOICES, default=HR)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1)
    active = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'gender']
    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email

    @property
    def get_full_name(self):
        # The user is identified by their email address
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


class Employee(models.Model):
    MALE = "M"
    FEMALE = "F"
    GENDER_CHOICES = (
        (MALE, "Male"),
        (FEMALE, "Female"),
    )
    PERMANENT = "PERMANENT"
    CONTRACT = "CONTRACT"
    EMPLOYEMENT_TYPE_CHOICES = (
        (PERMANENT, "Permanent"),
        (CONTRACT, "Contract"),
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True, max_length=254)
    qualification = models.TextField()
    address = models.CharField(max_length=250, null=True)
    joining_salary = models.CharField(max_length=50)
    id_number = models.BigIntegerField()
    role = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=12)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1)
    user = models.OneToOneField(
        User, null=True, related_name="employment_profile", on_delete=models.SET_NULL)
    employment_type = models.CharField(
        choices=EMPLOYEMENT_TYPE_CHOICES, max_length=50)
    dob=models.DateField()
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class OtpCode(models.Model):
    REGISTRATION = "R"
    RESET_PASSWORD = "RP"
    OTP_TYPE_CHOICES = (
        (REGISTRATION, "Registration"),
        (RESET_PASSWORD, "Reset password"),
    )
    code = models.CharField(max_length=6)
    user = models.ForeignKey(
        User, related_name="otp_codes", on_delete=models.CASCADE)
    otp_type = models.CharField(choices=OTP_TYPE_CHOICES, max_length=2)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "OtpCode"
        verbose_name_plural = "OtpCodes"

    def __str__(self):
        return self.code

    @property
    def is_valid(self):
        return self.created_on+timezone.timedelta(minutes=5) > timezone.now()


class Department(models.Model):
    name = models.CharField(max_length=50)
    designation = models.TextField()
    code = models.CharField(unique=True, max_length=50)
    employees = models.ManyToManyField(Employee, related_name="departments")

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"

    def __str__(self):
        return self.name

    @property
    def employees_count(self):
        return self.employees.count()


class Vacancie(models.Model):
    title = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    description = models.TextField()

    class Meta:
        verbose_name = "Vacancie"
        verbose_name_plural = "Vacancies"

    def __str__(self):
        return self.title


class ViewedVacancie(models.Model):
    vacancie = models.ForeignKey(Vacancie, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "ViewedVacancie"
        verbose_name_plural = "ViewedVacancies"

    def __str__(self):
        return self.name


class JobApplication(models.Model):
    full_names = models.CharField(max_length=250)
    email = models.EmailField(max_length=254)
    position = models.CharField(max_length=50)
    cover_letter = models.TextField()
    vacancie = models.ForeignKey(Vacancie, on_delete=models.CASCADE)
    cv = models.FileField(upload_to="candidates/cv/",
                          max_length=100, null=True)

    class Meta:
        verbose_name = "Job Applies"
        verbose_name_plural = "Job Appliess"

    def __str__(self):
        return self.full_names


class PaySlip(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    amount = models.FloatField()

    def __str__(self) -> str:
        return self.employee.email
