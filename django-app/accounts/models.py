from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.choice_classes import AccountRoleOptions
# from utils.function_account import generate_unique_uuid, generate_student_code
import uuid


class Account(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=AccountRoleOptions.choices,
    )

    # COMMON DETAILS - FOR ROLES: OWNER, TEACHER AND STUDENT
    cpf = models.BigIntegerField(
        unique=True,
        error_messages={"unique": "This C.P.F field must be unique."},
        # need REGEX
    )
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=128, null=True)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(
        max_length=127,
        unique=True,
        error_messages={"unique": "This email field must be unique."}
    )
    birthdate = models.DateField(
        null=True
        # need REGEX
    )
    phone = models.BigIntegerField(
        null=True
        # need REGEX
    )
    photo = models.CharField(max_length=255, null=True)
    bio = models.TextField(null=True)
    updated_at = models.DateTimeField(auto_now=True)

    # TEACHER DETAILS - ONLY FOR ROLE: TEACHER
    teacher_id = models.UUIDField(unique=True, editable=False, null=True)
    major = models.CharField(max_length=50, null=True)
    fired_at = models.DateField(null=True)
    fired_reason = models.CharField(max_length=255, null=True)

    # STUDENT DETAILS - ONLY FOR ROLE: STUDENT
    student_id = models.UUIDField(unique=True, editable=False, null=True)
    student_code = models.CharField(max_length=20, editable=False, unique=True, null=True)

    school = models.ForeignKey(
        'schools.School',
        on_delete=models.SET_NULL,
        related_name='accounts',
        null=True
    )

    @classmethod
    def generate_student_code(cls, model, field):
        """
        Generate a unique student_code for Account role Student.
        """
        now = datetime.now()
        occurrence = 0

        while True:
            student_code = f"{now.year}{now.month:02d}{now.day:02d}-{now.hour:02d}{now.minute:02d}{now.minute:02d}.{occurrence:02d}"
            try:
                model.objects.create(**{field: student_code})
            except IntegrityError:
                occurrence = occurrence + 1
                continue
            else:
                return student_code

    @classmethod
    def generate_unique_uuid(cls, model, field):
        """
        Generate a unique UUID for Account role Student and Teacher.
        """
        while True:
            uuid_value = uuid.uuid4()
            try:
                model.objects.create(**{field: uuid_value})
            except IntegrityError:
                continue
            else:
                return uuid_value

    # def save(self, *args, **kwargs):
    #     if self.request.method == 'POST':
    #         if self.role == 'Teacher':
    #             self.username = str(self.cpf)
    #             self.password = f"{self.cpf[:4]}@{self.last_name}"
    #             self.teacher_id = self.generate_unique_uuid(Account, 'teacher_id')
    #         elif self.role == 'Student':
    #             self.username = self.cpf
    #             self.password = f"{self.cpf[:4]}@{self.last_name}"
    #             self.student_code = self.generate_student_code(Account, 'student_code')
    #             self.student_id = self.generate_unique_uuid(Account, 'student_id')
    #     super(Account, self).save(*args, **kwargs)
