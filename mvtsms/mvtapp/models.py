from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


# Create your models here.
class SessionYearModel(models.Model):
    id = models.AutoField(primary_key=True)
    session_start_year = models.DateField()
    session_end_year = models.DateField()
    object = models.Manager()


class CustomUser(AbstractUser):
    user_type_data = ((1, "Admin"), (2, "Staff"), (3, "Student"), (4, "Parent"), (5, "Accountant"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)


class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=timezone.now())
    updated_at = models.DateTimeField(auto_now_add=timezone.now())
    objects = models.Manager()


class Staff(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=255)
    marital_status = models.TextField(max_length=255)
    address = models.CharField(max_length=500)
    phone_no = models.CharField(max_length=255)
    date_of_birth = models.DateField(auto_now_add=timezone.now())
    age = models.CharField(max_length=255)
    salary = models.CharField(max_length=255)
    employment_date = models.DateField(auto_now_add=timezone.now())
    profile_pic = models.FileField(default=timezone.now())
    created_at = models.DateTimeField(auto_now_add=timezone.now())
    updated_at = models.DateTimeField(auto_now_add=timezone.now())
    objects = models.Manager()


class Classes(models.Model):
    id = models.AutoField(primary_key=True)
    classes_name = models.CharField(max_length=255)
    staff_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=timezone.now())
    updated_at = models.DateTimeField(auto_now_add=timezone.now())
    objects = models.Manager()


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    classes_id = models.ForeignKey(Classes, on_delete=models.DO_NOTHING, default=1)
    gender = models.CharField(max_length=255)
    profile_pic = models.FileField()
    address = models.CharField(max_length=500)
    adm_date = models.DateField(auto_now_add=timezone.now())
    date_of_birth = models.DateField(auto_now_add=timezone.now())
    age = models.CharField(max_length=255)
    session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=timezone.now())
    updated_at = models.DateTimeField(auto_now_add=timezone.now())
    objects = models.Manager()


class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)
    classes_id = models.ForeignKey(Classes, on_delete=models.CASCADE, default=1)
    staff_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=timezone.now())
    updated_at = models.DateTimeField(auto_now_add=timezone.now())
    objects = models.Manager()


class Parent(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255)
    address = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=timezone.now())
    updated_at = models.DateTimeField(auto_now_add=timezone.now())
    objects = models.Manager()


class Accountant(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=255)
    marital_status = models.TextField(max_length=255)
    address = models.CharField(max_length=500)
    phone_no = models.CharField(max_length=255)
    date_of_birth = models.DateField(auto_now_add=timezone.now())
    age = models.CharField(max_length=255)
    salary = models.CharField(max_length=255)
    employment_date = models.DateField(auto_now_add=timezone.now())
    profile_pic = models.FileField()
    created_at = models.DateTimeField(auto_now_add=timezone.now())
    updated_at = models.DateTimeField(auto_now_add=timezone.now())
    objects = models.Manager()


class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    classes_id = models.ForeignKey(Classes, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=timezone.now())
    total_amount = models.FloatField()
    amount_paid = models.FloatField()
    balance = models.FloatField()
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=timezone.now())
    updated_at = models.DateTimeField(auto_now_add=timezone.now())
    objects = models.Manager()


class AccountantLeave(models.Model):
    id = models.AutoField(primary_key=True)
    accountant_id = models.ForeignKey(Accountant, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=timezone.now())
    updated_at = models.DateTimeField(auto_now_add=timezone.now())
    objects = models.Manager()


class TermDetails(models.Model):
    id = models.AutoField(primary_key=True)
    session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE, default=1)
    term_name = models.TextField()
    vacation_date = models.DateField(auto_now_add=timezone.now())
    resumption_date = models.DateField(auto_now_add=timezone.now())
    objects = models.Manager


class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.DO_NOTHING, default=1)
    classes_id = models.ForeignKey(Classes, on_delete=models.DO_NOTHING, default=1)
    term_id = models.ForeignKey(TermDetails, on_delete=models.CASCADE, default=1)
    times_absent = models.IntegerField(default=0)
    times_open = models.IntegerField(default=0)
    times_present = models.IntegerField(default=0)
    session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=timezone.now())
    updated_at = models.DateTimeField(auto_now_add=timezone.now())
    objects = models.Manager()


class PaymentReport(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    payment_id = models.ForeignKey(Payment, on_delete=models.DO_NOTHING)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=timezone.now())
    updated_at = models.DateTimeField(auto_now_add=timezone.now())
    objects = models.Manager()



class StaffLeave(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE, default=1)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=timezone.now())
    updated_at = models.DateTimeField(auto_now_add=timezone.now())
    objects = models.Manager()



class EngScores(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, default=1)
    classes_id = models.ForeignKey(Classes, on_delete=models.CASCADE, default=1)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE, default=1)
    eng_score1 = models.IntegerField(default=0)
    eng_score2 = models.IntegerField(default=0)
    eng_score3 = models.IntegerField(default=0)
    eng_project_score = models.IntegerField(default=0)
    eng_exam_score = models.IntegerField(default=0)
    eng_remarks = models.TextField()
    eng_total_score = models.IntegerField(default=0)
    term_id = models.ForeignKey(TermDetails, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=timezone.now())
    updated_at = models.DateTimeField(auto_now_add=timezone.now())
    objects = models.Manager()

#mathematics scores
class MthScores(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, default=1)
    classes_id = models.ForeignKey(Classes, on_delete=models.CASCADE, default=1)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE, default=1)
    mth_score1 = models.IntegerField(default=0)
    mth_score2 = models.IntegerField(default=0)
    mth_score3 = models.IntegerField(default=0)
    mth_project_score = models.IntegerField(default=0)
    mth_exam_score = models.IntegerField(default=0)
    mth_remarks = models.TextField()
    mth_total_score = models.IntegerField(default=0)
    term_id = models.ForeignKey(TermDetails, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=timezone.now())
    updated_at = models.DateTimeField(auto_now_add=timezone.now())
    objects = models.Manager()



class SciScores(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, default=1)
    classes_id = models.ForeignKey(Classes, on_delete=models.CASCADE, default=1)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE, default=1)
    sci_score1 = models.IntegerField(default=0)
    sci_score2 = models.IntegerField(default=0)
    sci_score3 = models.IntegerField(default=0)
    sci_project_score = models.IntegerField(default=0)
    sci_exam_score = models.IntegerField(default=0)
    sci_remarks = models.TextField()
    sci_total_score = models.IntegerField(default=0)
    term_id = models.ForeignKey(TermDetails, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=timezone.now())
    updated_at = models.DateTimeField(auto_now_add=timezone.now())
    objects = models.Manager()


class IctScores(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, default=1)
    classes_id = models.ForeignKey(Classes, on_delete=models.CASCADE, default=1)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE, default=1)
    ict_score1 = models.IntegerField(default=0)
    ict_score2 = models.IntegerField(default=0)
    ict_score3 = models.IntegerField(default=0)
    ict_project_score = models.IntegerField(default=0)
    ict_exam_score = models.IntegerField(default=0)
    ict_remarks = models.TextField()
    ict_total_score = models.IntegerField(default=0)
    term_id = models.ForeignKey(TermDetails, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=timezone.now())
    updated_at = models.DateTimeField(auto_now_add=timezone.now())
    objects = models.Manager()

#national values scores
class NvScores(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, default=1)
    classes_id = models.ForeignKey(Classes, on_delete=models.CASCADE, default=1)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE, default=1)
    nv_score1 = models.IntegerField(default=0)
    nv_score2 = models.IntegerField(default=0)
    nv_score3 = models.IntegerField(default=0)
    nv_project_score = models.IntegerField(default=0)
    nv_exam_score = models.IntegerField(default=0)
    nv_remarks = models.TextField()
    nv_total_score = models.IntegerField(default=0)
    term_id = models.ForeignKey(TermDetails, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=timezone.now())
    updated_at = models.DateTimeField(auto_now_add=timezone.now())
    objects = models.Manager()


class PheScores(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, default=1)
    classes_id = models.ForeignKey(Classes, on_delete=models.CASCADE, default=1)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE, default=1)
    phe_score1 = models.IntegerField(default=0)
    phe_score2 = models.IntegerField(default=0)
    phe_score3 = models.IntegerField(default=0)
    phe_project_score = models.IntegerField(default=0)
    phe_exam_score = models.IntegerField(default=0)
    phe_remarks = models.TextField()
    phe_total_score = models.IntegerField(default=0)
    term_id = models.ForeignKey(TermDetails, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=timezone.now())
    updated_at = models.DateTimeField(auto_now_add=timezone.now())
    objects = models.Manager()


class IrsScores(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, default=1)
    classes_id = models.ForeignKey(Classes, on_delete=models.CASCADE, default=1)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE, default=1)
    irs_score1 = models.IntegerField(default=0)
    irs_score2 = models.IntegerField(default=0)
    irs_score3 = models.IntegerField(default=0)
    irs_project_score = models.IntegerField(default=0)
    irs_exam_score = models.IntegerField(default=0)
    irs_remarks = models.TextField()
    irs_total_score = models.IntegerField(default=0)
    term_id = models.ForeignKey(TermDetails, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=timezone.now())
    updated_at = models.DateTimeField(auto_now_add=timezone.now())
    objects = models.Manager()


class CrkScores(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, default=1)
    classes_id = models.ForeignKey(Classes, on_delete=models.CASCADE, default=1)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE, default=1)
    crk_score1 = models.IntegerField(default=0)
    crk_score2 = models.IntegerField(default=0)
    crk_score3 = models.IntegerField(default=0)
    crk_project_score = models.IntegerField(default=0)
    crk_exam_score = models.IntegerField(default=0)
    crk_remarks = models.TextField()
    crk_total_score = models.IntegerField(default=0)
    term_id = models.ForeignKey(TermDetails, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=timezone.now())
    updated_at = models.DateTimeField(auto_now_add=timezone.now())
    objects = models.Manager()


class QuranScores(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, default=1)
    classes_id = models.ForeignKey(Classes, on_delete=models.CASCADE, default=1)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE, default=1)
    quran_score1 = models.IntegerField(default=0)
    quran_score2 = models.IntegerField(default=0)
    quran_score3 = models.IntegerField(default=0)
    quran_project_score = models.IntegerField(default=0)
    quran_exam_score = models.IntegerField(default=0)
    quran_remarks = models.TextField()
    quran_total_score = models.IntegerField(default=0)
    term_id = models.ForeignKey(TermDetails, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=timezone.now())
    updated_at = models.DateTimeField(auto_now_add=timezone.now())
    objects = models.Manager()


class BroadSheet(models.Model):
    id = models.AutoField(primary_key=True)
    term1_bs_score = models.IntegerField(default=0)
    term2_bs_score = models.IntegerField(default=0)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, default=1)
    classes_id = models.ForeignKey(Classes, on_delete=models.CASCADE, default=1)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE, default=1)
    score1 = models.IntegerField(default=0)
    score2 = models.IntegerField(default=0)
    score3 = models.IntegerField(default=0)
    project_score = models.IntegerField(default=0)
    exam_score = models.IntegerField(default=0)
    total_score = models.IntegerField(default=0)
    grand_total_score = models.IntegerField(default=0)
    objects = models.Manager()


class TermTrait(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, default=1)
    term_id = models.ForeignKey(TermDetails, on_delete=models.CASCADE, default=1)
    punctuality = models.IntegerField(default=0)
    reliability = models.IntegerField(default=0)
    neatness = models.IntegerField(default=0)
    honesty = models.IntegerField(default=0)
    leadership = models.IntegerField(default=0)
    politeness = models.IntegerField(default=0)
    relationship = models.IntegerField(default=0)
    attentiveness = models.IntegerField(default=0)
    self_discipline = models.IntegerField(default=0)
    perseverance = models.IntegerField(default=0)
    handwriting = models.IntegerField(default=0)
    sports = models.IntegerField(default=0)
    drawing = models.IntegerField(default=0)
    craft = models.IntegerField(default=0)
    musical = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=timezone.now())
    updated_at = models.DateTimeField(auto_now_add=timezone.now())
    objects = models.Manager()


class TermRemarks(models.Model):
    id = models.AutoField(primary_key=True)
    term_id = models.ForeignKey(TermDetails, on_delete=models.CASCADE, default=1)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, default=0)
    teachers_remark = models.TextField()
    principals_remark = models.TextField()
    objects = models.Manager


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            Admin.objects.create(admin=instance)
        if instance.user_type == 2:
            Staff.objects.create(admin=instance, address=" ",profile_pic=" ",gender=" ",phone_no=" ", employment_date="2020-01-01", date_of_birth="2020-01-01", marital_status=" ", age=" ", salary=" ")
        if instance.user_type == 3:
            Student.objects.create(admin=instance, classes_id=Classes.objects.get(id=1),adm_date="2020-01-01",session_year_id = SessionYearModel.object.get(id=1), address=" ",profile_pic=" ", gender=" ", date_of_birth="2020-01-01")
        if instance.user_type == 4:
            Parent.objects.create(admin=instance)
        if instance.user_type == 5:
            Accountant.objects.create(admin=instance, address=" ",profile_pic=" ",gender=" ",phone_no=" ", employment_date="2020-01-01", date_of_birth="2020-01-01", marital_status=" ", age=" ", salary=" ")


#session_year_id = SessionYearModel.object.get(id=1),
@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.staff.save()
    if instance.user_type == 3:
        instance.student.save()
    if instance.user_type == 4:
        instance.parent.save()
    if instance.user_type == 5:
        instance.accountant.save()




