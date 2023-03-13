import datetime

from django.core.files.storage import FileSystemStorage
from django.db.models import F, Sum, Min, Max, Avg, Count, Value
from django.template import context
from django.urls import reverse
from mysql import connector as con
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from mvtapp.models import CustomUser, BroadSheet, TermRemarks, TermDetails,\
    Attendance, TermTrait, EngScores, Classes, Subject, Staff, Student, Accountant, Parent,\
    SessionYearModel, StaffLeave,MthScores, NvScores,SciScores,IctScores, IrsScores,QuranScores,CrkScores,PheScores

from mvtapp.forms import AddStudentForm, EditStudentForm




def home(request):
    student_count = Student.objects.all().count()
    classes_count = Classes.objects.all().count()
    subject_count = Subject.objects.all().count()
    staff_count = Staff.objects.all().count()
    parent_count = Parent.objects.all().count()
    accountant_count = Accountant.objects.all().count()
    student_m_gender = Student.objects.filter(gender="male").count()
    student_f_gender = Student.objects.filter(gender="female").count()
    staff_m_gender = Staff.objects.filter(gender="male").count()
    staff_f_gender = Staff.objects.filter(gender="female").count()
    leave = StaffLeave.objects.all()
    new_leave = StaffLeave.objects.filter(leave_status=0).count
    term = TermDetails.objects.all()
    return render(request, "admin_template/home_content.html", {"student_count":student_count,
                                                                "classes_count":classes_count,
                                                                "subject_count":subject_count,
                                                                "staff_count":staff_count,
                                                                "parent_count":parent_count,
                                                                "accountant_count":accountant_count,
                                                                "student_m_gender":student_m_gender,
                                                                "student_f_gender":student_f_gender,
                                                                "staff_m_gender":staff_m_gender,
                                                                "staff_f_gender":staff_f_gender,
                                                                "leave":leave,"term":term,
                                                                "new_leave":new_leave})


def addstaff(request):
    return render(request, "admin_template/add_staff.html")


def savestaff(request):
    if request.method != "POST":
        return HttpResponse("Input All Fields Correctly")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        gender = request.POST.get("gender")
        marital_status = request.POST.get("marital_status")
        address = request.POST.get("address")
        phone_no = request.POST.get("phone_no")
        date_of_birth = request.POST.get("date_of_birth")
        age = request.POST.get("age")
        salary = request.POST.get("salary")
        employment_date = request.POST.get("employment_date")
        profile_pic = request.POST.get("profile_pic")
        try:
            user = CustomUser.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password, user_type=2)
            user.staff.address = address
            user.staff.gender = gender
            user.staff.marital_status = marital_status
            user.staff.phone_no = phone_no
            user.staff.date_of_birth = date_of_birth
            user.staff.age = age
            user.staff.salary = salary
            user.staff.employment_date = employment_date
            user.staff.profile_pic = profile_pic
            user.save()
            messages.success(request, "Staff Added Successfully")
            return HttpResponseRedirect("/add_staff")
        except ValueError as v:
            messages.error(request, v)
            return HttpResponseRedirect("/add_staff")

        except con.Error as c:
            messages.error(request, c)
            return HttpResponseRedirect("/add_staff")

        except TypeError as t:
            messages.error(request, t)
            return HttpResponseRedirect("/add_staff")

        except NameError as n:
            messages.error(request, n)
            return HttpResponseRedirect("/add_staff")

        except Exception as e:
            messages.error(request, e)
            return HttpResponseRedirect("/add_staff")

        except:
            messages.error(request, "Failed To Add Staff")
            return HttpResponseRedirect("/add_staff")



def addstudent(request):
    form = AddStudentForm()
    return render(request, "admin_template/add_student.html", {"form":form})


def savestudent(request):
    if request.method == "POST":
        form = AddStudentForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            gender = form.cleaned_data["gender"]
            address = form.cleaned_data["address"]
            adm_date = form.cleaned_data["adm_date"]
            date_of_birth = form.cleaned_data["date_of_birth"]
            age = form.cleaned_data["age"]

            session_year_id = form.cleaned_data["session_year_id"]
            classes_id = form.cleaned_data["clas"]

            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)

            try:
                user = CustomUser.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password, user_type=3)
                classes_obj = Classes.objects.get(id=classes_id)
                user.student.classes_id = classes_obj
                user.student.gender = gender
                user.student.address = address
                user.student.adm_date = adm_date
                user.student.date_of_birth = date_of_birth
                user.student.age = age
                session_year = SessionYearModel.object.get(id=session_year_id)
                user.student.session_year_id = session_year
                #start_date = datetime.datetime.strptime(session_start, '%d-%m-%y').strftime('%y-%m-%d')
                #end_date = datetime.datetime.strptime(session_end, '%d-%m-%y').strftime('%y-%m-%d')



                if profile_pic_url != None:
                    user.student.profile_pic = profile_pic_url
                    user.save()
                    messages.success(request, "Student Added Successfully")
                    #return HttpResponseRedirect("/add_student")
                    return HttpResponseRedirect(reverse("addstudent"))

            except Exception as e:
                messages.error(request, e)
                return HttpResponseRedirect("/add_student")
            except:
                messages.error(request, " Failed To Add Student")
                return HttpResponseRedirect("/add_student")
        else:
           return render(request, "admin_template/add_student.html", {"form":form})

    else:
        return HttpResponse("Method Not Allowed")


def addclasses(request):
    staff = CustomUser.objects.filter(user_type=2)
    return render(request, "admin_template/add_classes.html", {"staff":staff})


def saveclasses(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed")
    else:
        classes_name = request.POST.get("classes")
        staff_id = request.POST.get("staff")
        staff = CustomUser.objects.get(id=staff_id)
        try:
            classes = Classes(classes_name=classes_name, staff_id=staff)
            classes.save()
            messages.success(request, "Class Added Successfully")
            return HttpResponseRedirect("/add_classes")
        except ValueError as v:
            messages.error(request, v)
            return HttpResponseRedirect("/add_classes")
        except con.Error as c:
            messages.error(request, c)
            return HttpResponseRedirect("/add_classes")
        except TypeError as t:
            messages.error(request, t)
            return HttpResponseRedirect("/add_classes")
        except NameError as n:
            messages.error(request, n)
            return HttpResponseRedirect("/add_classes")
        except Exception as e:
            messages.error(request, e)
            return HttpResponseRedirect("/add_classes")
        except:
            messages.error(request, " Failed To Add Class")
            return HttpResponseRedirect("/add_classes")


def addparent(request):
    return render(request, "admin_template/add_parent.html")


def saveparent(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        occupation = request.POST.get("occupation")
        try:
            user = CustomUser.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password, user_type=4)
            user.parent.address = address
            user.parent.phone = phone
            user.parent.occupation = occupation
            user.save()
            messages.success(request, "Parent Added Successfully")
            return HttpResponseRedirect("/add_parent")
        except ValueError as v:
            messages.error(request, v)
            return HttpResponseRedirect("/add_parent")
        except con.Error as c:
            messages.error(request, c)
            return HttpResponseRedirect("/add_parent")
        except TypeError as t:
            messages.error(request, t)
            return HttpResponseRedirect("/add_parent")
        except NameError as n:
            messages.error(request, n)
            return HttpResponseRedirect("/add_parent")
        except Exception as e:
            messages.error(request, e)
            return HttpResponseRedirect("/add_parent")
        except:
            messages.error(request, "Failed To Add Parent")
            return HttpResponseRedirect("/add_parent")


def addaccountant(request):
    return render(request, "admin_template/add_accountant.html")


def saveaccountant(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        gender = request.POST.get("gender")
        marital_status = request.POST.get("marital_status")
        address = request.POST.get("address")
        phone_no = request.POST.get("phone_no")
        date_of_birth = request.POST.get("date_of_birth")
        age = request.POST.get("age")
        salary = request.POST.get("salary")
        employment_date = request.POST.get("employment_date")
        profile_pic = request.POST.get("profile_pic")
        try:
            user = CustomUser.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password, user_type=5)
            user.accountant.address = address
            user.accountant.gender = gender
            user.accountant.marital_status = marital_status
            user.accountant.phone_no = phone_no
            user.accountant.date_of_birth = date_of_birth
            user.accountant.age = age
            user.accountant.salary = salary
            user.accountant.employment_date = employment_date
            user.accountant.profile_pic = profile_pic
            user.save()
            messages.success(request, "Accountant Added Successfully")
            return HttpResponseRedirect("/add_accountant")
        except ValueError as v:
            messages.error(request, v)
            return HttpResponse("Input All Fields Correctly")
        except con.Error as c:
            messages.error(request, c)
            return HttpResponseRedirect("/add_accountant")
        except TypeError as t:
            messages.error(request, t)
            return HttpResponseRedirect("/add_accountant")
        except NameError as n:
            messages.error(request, n)
            return HttpResponseRedirect("/add_accountant")
        except Exception as e:
            messages.error(request, e)
            return HttpResponseRedirect("/add_accountant")
        except:
            messages.error(request, "Failed To Add Accountant")


def addsubject(request):
    classes = Classes.objects.all()
    staff = CustomUser.objects.filter(user_type=2)
    return render(request, "admin_template/add_subject.html", {"staff":staff, "classes":classes})


def savesubject(request):
    if request.method == "POST":
        subject_name = request.POST.get("subject_name")
        classes_id = request.POST.get("classes")
        classes = Classes.objects.get(id=classes_id)
        staff_id = request.POST.get("staff")
        staff = CustomUser.objects.get(id=staff_id)
        try:
            subject = Subject(subject_name=subject_name, classes_id=classes, staff_id=staff)
            subject.save()
            messages.success(request, "Subject Added Successfully")
            return HttpResponseRedirect("/add_subject")
        except:
            messages.error(request, "Failed To Add Subject")
            return HttpResponseRedirect("/add_subject")
    else:
        return HttpResponse("Method is Invalid")


def managestaff(request):
    staff = Staff.objects.all()
    return render(request, "admin_template/manage_staff.html", {"staff":staff})


def manageparent(request):
    parent = Parent.objects.all()
    return render(request, "admin_template/manage_parent.html", {"parent":parent})


def managestudent(request):
    student = Student.objects.all()
    return render(request, "admin_template/manage_student.html", {"student":student})


def manageaccountant(request):
    accountant = Accountant.objects.all()
    return render(request, "admin_template/manage_accountant.html", {"accountant":accountant})


def manageclasses(request):
    classes = Classes.objects.all()
    return render(request, "admin_template/manage_classes.html", {"classes":classes})


def managesubject(request):
    subject = Subject.objects.all()
    return render(request, "admin_template/manage_subject.html", {"subject":subject})


def edit_staff(request, staff_id):
    staff = Staff.objects.get(admin=staff_id)
    return render(request, "admin_template/edit_staff.html", {"staff":staff})


def edit_staff_save(request):
    if request.method != "POST":
        return HttpResponse("INVALID METHOD")
    else:
        staff_id = request.POST.get("staff_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        gender = request.POST.get("gender")
        marital_status = request.POST.get("marital_status")
        address = request.POST.get("address")
        phone_no = request.POST.get("phone_no")
        date_of_birth = request.POST.get("date_of_birth")
        age = request.POST.get("age")
        salary = request.POST.get("salary")
        employment_date = request.POST.get("employment_date")
        profile_pic = request.POST.get("profile_pic")
        try:
            user = CustomUser.objects.get(id=staff_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()

            staff = Staff.objects.get(admin=staff_id)
            staff.address = address
            staff.gender = gender
            staff.marital_status = marital_status
            staff.phone_no = phone_no
            staff.date_of_birth = date_of_birth
            staff.age = age
            staff.salary = salary
            staff.employment_date = employment_date
            staff.profile_pic = profile_pic
            staff.save()
            messages.success(request, "Updated Successfully")
            return HttpResponseRedirect("/edit_staff/"+staff_id)
        except:
            messages.error(request, "Failed To Update")
            return HttpResponseRedirect("/edit_staff/"+staff_id)


def edit_student(request, student_id):
    request.session['student_id'] = student_id
    student = Student.objects.get(admin=student_id)
    form = EditStudentForm()
    form.fields['email'].initial = student.admin.email
    form.fields['username'].initial = student.admin.username
    form.fields['first_name'].initial = student.admin.first_name
    form.fields['last_name'].initial = student.admin.last_name
    form.fields['address'].initial = student.address
    form.fields['age'].initial = student.age
    form.fields['gender'].initial = student.gender
    form.fields['adm_date'].initial = student.adm_date
    form.fields['date_of_birth'].initial = student.date_of_birth
    form.fields['clas'].initial = student.classes_id.id
    form.fields['session_year_id'].initial = student.session_year_id.id
    return render(request, "admin_template/edit_student.html", {"form":form, "id":student_id, "username":student.admin.username})


def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("INVALID METHOD")
    else:
        student_id = request.session.get("student_id")
        if student_id == None:
            return HttpResponseRedirect(reverse("managestudent"))

        form = EditStudentForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            classes_id = form.cleaned_data["clas"]
            gender = form.cleaned_data["gender"]
            address = form.cleaned_data["address"]
            adm_date = form.cleaned_data["adm_date"]
            date_of_birth = form.cleaned_data["date_of_birth"]
            age = form.cleaned_data["age"]
            session_year_id = form.cleaned_data["session_year_id"]


            if request.FILES.get('profile_pic', False):
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None


            try:
                user = CustomUser.objects.get(id=student_id)
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.email = email
                user.save()

                student = Student.objects.get(admin=student_id)
                student.address = address
                student.age = age
                student.adm_date = adm_date
                student.date_of_birth = date_of_birth
                student.gender = gender
                clas = Classes.objects.get(id=classes_id)
                student.classes_id = clas
                session_year = SessionYearModel.object.get(id=session_year_id)
                student.session_year_id = session_year

                if profile_pic_url != None:
                    user.student.profile_pic = profile_pic_url
                student.save()
                del request.session['student_id']
                messages.success(request, "Updated Successfully")
                return HttpResponseRedirect(reverse("editstudent", kwargs={"student_id":student_id}))
            except:
                messages.error(request, "Failed To Update")
                return HttpResponseRedirect(reverse("editstudent", kwargs={"student_id":student_id}))
        else:
            form = EditStudentForm(request.POST)
            student = Student.objects.get(admin=student_id)
            return HttpResponseRedirect(reverse("editstudent", {"form":form, "id":student_id, "username":student.admin.username }))



def edit_accountant(request, accountant_id):
    accountant = Accountant.objects.get(admin=accountant_id)
    return render(request, "admin_template/edit_accountant.html", {"accountant":accountant})

def edit_accountant_save(request):
    if request.method != "POST":
        return HttpResponse("INVALID METHOD")
    else:
        accountant_id = request.POST.get("accountant_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        gender = request.POST.get("gender")
        marital_status = request.POST.get("marital_status")
        address = request.POST.get("address")
        phone_no = request.POST.get("phone_no")
        date_of_birth = request.POST.get("date_of_birth")
        age = request.POST.get("age")
        salary = request.POST.get("salary")
        employment_date = request.POST.get("employment_date")
        profile_pic = request.POST.get("profile_pic")
        try:
            user = CustomUser.objects.get(id=accountant_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()

            accountant = Accountant.objects.get(admin=accountant_id)
            accountant.gender = gender
            accountant.marital_status = marital_status
            accountant.address = address
            accountant.phone_no = phone_no
            accountant.date_of_birth = date_of_birth
            accountant.age = age
            accountant.salary = salary
            accountant.employment_date = employment_date
            accountant.profile_pic = profile_pic
            accountant.save()
            messages.success(request, "Updated Successfully")
            #return HttpResponseRedirect("/edit_accountant/"+accountant_id)
            return HttpResponseRedirect(reverse("editaccountant", kwargs={"accountant_id": accountant_id}))
        except:
            messages.error(request, "Failed To Update")
            #return HttpResponseRedirect("/edit_accountant/"+accountant_id)
            return HttpResponseRedirect(reverse("editaccountant", kwargs={"accountant_id": accountant_id}))


def edit_parent(request, parent_id):
    parent = Parent.objects.get(admin=parent_id)
    return render(request, "admin_template/edit_parent.html", {"parent":parent})


def edit_parent_save(request):
    if request.method == "POST":
        parent_id = request.POST.get("parent_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        phone = request.POST.get("phone")
        occupation = request.POST.get("occupation")
        address = request.POST.get("address")
        try:
            user = CustomUser.objects.get(id=parent_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()

            parent = Parent.objects.get(admin=parent_id)
            parent.phone = phone
            parent.occupation = occupation
            parent.address = address
            parent.save()
            messages.success(request, "Parent Details Updated Successfully")
            return HttpResponseRedirect("/edit_parent/"+parent_id)
        except:
            messages.error(request, "Failed To Update Parent Details")
            return HttpResponseRedirect("/edit_parent/"+parent_id)
    else:
        return HttpResponse("<h2> THIS IS INVALID</h2>")


def edit_subject(request, subject_id):
    subject = Subject.objects.get(id=subject_id)
    classes = Classes.objects.all()
    staff = CustomUser.objects.filter(user_type=2)
    return render(request, "admin_template/edit_subject.html", {"subject": subject, "classes": classes, "staff": staff})


def edit_subject_save(request):
    if request.method == "POST":
        subject_name = request. POST.get("subject_name")
        subject_id = request.POST.get("subject_id")
        classes_id = request.POST.get("clas")
        staff_id = request.POST.get("staf")
        try:
            subject = Subject.objects.get(id=subject_id)
            subject.subject_name = subject_name
            staf = CustomUser.objects.get(id=staff_id)
            subject.staff_id = staf
            clas = Classes.objects.get(id=classes_id)
            subject.classes_id = clas
            subject.save()
            messages.success(request, "Subject Updated Successfully")
            return HttpResponseRedirect("/edit_subject/" + subject_id)
        except:
            messages.error(request, "Failed To Update Subject Details")
            return HttpResponseRedirect("/edit_subject/" + subject_id)
    else:
        return HttpResponse("MYbad")


"""def edit_subject_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed </h2>")
    else:
        subject_id = request.POST.get("subject_id")
        subject_name = request.POST.get("subject_name")
        staff_id = request.POST.get("staf")
        classes_id = request.POST.get("clas")
        try:
            subject = Subject.objects.get(id=subject_id)
            subject.subject_name = subject_name
            staf = CustomUser.objects.get(id=staff_id)
            subject.staff_id = staf
            clas = Classes.objects.get(id=classes_id)
            subject.classes_id = clas
            subject.save()
            messages.success(request, "Subject Updated Successfully")
            return HttpResponseRedirect("/edit_subject/"+subject_id)
        except:
            messages.error(request, "Failed To Update Subject Details")
            return HttpResponseRedirect("/edit_subject/"+subject_id)"""


def edit_classes(request, classes_id):
    classes = Classes.objects.get(id=classes_id)
    staff = CustomUser.objects.filter(user_type=2)
    return render(request, "admin_template/edit_classes.html", {"classes":classes, "staff":staff})

def delete_classes(request, classes_id):
    classes = Classes.objects.get(id=classes_id)
    staff = CustomUser.objects.filter(user_type=2)
    return render(request, "admin_template/delete_classes.html", {"classes":classes, "staff":staff})


"""def edit_classes_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed </h2>")
    else:
        classes_name = request.POST.get("clas")
        classes_id = request.POST.get("classes_id")
        staff_id = request.POST.get("staf")
        try:
            classes = Classes.objects.get(id=classes_id)
            classes.classes_name = classes_name
            
            staf = CustomUser.objects.get(id=staff_id)
            classes.staff_id = staf

            classes.save()
            messages.success(request, "Class Updated Successfully")
            return HttpResponseRedirect("/edit_classes/"+classes_id)
        except:
            messages.error(request, "Failed To Update Class Details")
            return HttpResponseRedirect("/edit_classes/"+classes_id)"""

def edit_classes_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed </h2>")
    else:
        classes_name = request.POST.get("clas")
        classes_id = request.POST.get("classes_id")
        staff = request.POST.get("staf")
        staff_id = CustomUser.objects.get(id=staff)
        try:
            classes = Classes(classes_name=classes_name, id=classes_id, staff_id=staff_id)
            classes.save()
            messages.success(request, "Class Updated Successfully")
            return HttpResponseRedirect("/edit_classes/" + classes_id)
        except:
            messages.error(request, "Failed To Update Class Details")
            return HttpResponseRedirect("/edit_classes/" + classes_id)



def edit_classes_delete(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed </h2>")
    else:
        classes_id = request.POST.get("classes_id")
        try:
            data_exists = Classes.objects.filter(id=classes_id).exists()
            if data_exists:
                classes = Classes(id=classes_id)
                classes.delete()
                return HttpResponseRedirect("/manage_classes")
            else:
                messages.error(request, "Data Does Not Exit")
                return HttpResponseRedirect("/edit_classes")
        except:
            messages.error(request, "Failed To Update Class Details")
            return HttpResponseRedirect("/edit_classes")



def attend(request):
    return render(request, "admin_template/attendance_class.html")


def managesession(request):
    sessionyear = SessionYearModel.object.all()
    return render(request, "admin_template/manage_session.html",{"sessionyear":sessionyear})

def savesession(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("managesession"))
    else:
        session_start_year = request.POST.get("session_start")
        session_end_year = request.POST.get("session_end")

        try:
            sessionyear = SessionYearModel(session_start_year=session_start_year, session_end_year=session_end_year)
            sessionyear.save()
            messages.success(request, "Session Added Successfully")
            return HttpResponseRedirect(reverse("managesession"))
        except:
            messages.error(request, "Failed To Add Session Details")
            return HttpResponseRedirect(reverse("managesession"))



def delete_session(request, ses_id):
    ses = SessionYearModel.object.get(id=ses_id)
    return render(request, "admin_template/delete_session.html",{"ses":ses})


def delete_a_session(request):
    if request.method == "POST":
        session_id = request.POST.get("session_id")
        ses = SessionYearModel.object.get(id=session_id)
        ses.delete()
        return HttpResponseRedirect(reverse("managesession"))


def view_leave(request):
    leave = StaffLeave.objects.all()
    return render(request, "admin_template/view_leave.html", {"leave":leave})


def approve_leave(request, id):
    leave = StaffLeave.objects.get(id=id)
    leave.leave_status = 1
    leave.save()
    return render(request, "admin_template/view_leave.html")


def disapprove_leave(request, id):
    leave = StaffLeave.objects.get(id=id)
    leave.leave_status = 2
    leave.save()
    return render(request, "admin_template/view_leave.html")

def admin_viewresults(request, term_id):
    get_term = None
    total = None
    data = None
    data2 = None
    classes = Classes.objects.all()
    subject = Subject.objects.filter(staff_id=request.user.id)
    session_year = SessionYearModel.object.all()
    action = request.GET.get("action")
    get_classes = None
    get_session_year = None
    term1 = None
    traits = None
    student = None
    if action is not None and request.method == "POST":

        classes_id = request.POST.get('classes_id')

        get_term = TermDetails.objects.get(id=term_id)
        session_year_id = request.POST.get('session_year_id')
        get_classes = Classes.objects.get(id=classes_id)
        get_session_year = SessionYearModel.object.get(id=session_year_id)
        #classes = Classes.objects.get(staff_id=request.user.id)
        student = Student.objects.filter(classes_id=classes_id)

        student_id = request.POST.get('student_id')
        term1 = EngScores.objects.filter(student_id=student_id)
        traits =TermTrait.objects.filter(student_id=student_id)


        data = EngScores.objects.all().aggregate(sum=Sum("eng_total_score"), max=Max("eng_total_score"),
                                                      min=Min("eng_total_score"), avg=Avg("eng_total_score"))
        data2 = EngScores.objects.all().count()
    return render(request, "admin_template/view_results.html", {"get_term":get_term,  "traits":traits, "total":total,
                                                                "data2":data2, "data":data, "session_year":session_year,
                                                                "classes":classes, "subject":subject,
                                                                "get_classes":get_classes,"get_session_year":get_session_year,
                                                                "action":action, "student":student, "term1":term1})


def fetchresults(request):
    try:
        student_id = request.POST.get('student_id')
        classes_id = request.POST.get('classes_id')
        term_id = request.POST.get('term_id')
        get_term = TermDetails.objects.get(id=term_id)
        print(term_id)
        termdetails = TermDetails.objects.filter(id=term_id)
        #cls = Classes.objects.get(id=classes_id)
        student = Student.objects.filter(classes_id=classes_id)
        student_obj = Student.objects.get(id=student_id)
        broad = BroadSheet.objects.filter(student_id=student_id)
        subject_id = Subject.objects.filter(id=1)

        traits = TermTrait.objects.filter(student_id=student_id, term_id=get_term)

        get_traits = TermTrait.objects.get(student_id=student_id, term_id=get_term)

        c_id = get_traits.student_id.classes_id.id
        get_classes = Classes.objects.get(id=c_id)

        classes = Classes.objects.all()
        attendance = Attendance.objects.filter(student_id=student_id, term_id=get_term)

        remarks =TermRemarks.objects.filter(student_id=student_id, term_id=get_term)
        get_student = Student.objects.get(id=student_id)


            #data for subject scores on each total
        #Book.objects.annotate(num_authors=Count('authors')).aggregate(Avg('num_authors'))
        eng_scores = EngScores.objects.filter(student_id=student_obj, term_id=get_term)
        dat = EngScores.objects.filter(classes_id=get_classes, term_id=get_term).aggregate(avg=Avg("eng_total_score"),
                                                                              max=Max("eng_total_score"),
                                                                              min=Min("eng_total_score"))
        mth_scores = MthScores.objects.filter(student_id=student_obj, term_id=get_term)
        dat1 = MthScores.objects.filter(classes_id=get_classes, term_id=get_term).aggregate(avg=Avg("mth_total_score"),
                                                                                            max=Max("mth_total_score"),
                                                                                            min=Min("mth_total_score"))
        sci_scores = SciScores.objects.filter(student_id=student_obj, term_id=get_term)
        dat2 = SciScores.objects.filter(classes_id=get_classes, term_id=get_term).aggregate(avg=Avg("sci_total_score"),
                                                                                            max=Max("sci_total_score"),
                                                                                            min=Min("sci_total_score"))
        nv_scores = NvScores.objects.filter(student_id=student_obj, term_id=get_term)
        dat3 = NvScores.objects.filter(classes_id=get_classes, term_id=get_term).aggregate(avg=Avg("nv_total_score"),
                                                                                           max=Max("nv_total_score"),
                                                                                           min=Min("nv_total_score"))
        ict_scores = IctScores.objects.filter(student_id=student_obj, term_id=get_term)
        dat4 = IctScores.objects.filter(classes_id=get_classes, term_id=get_term).aggregate(avg=Avg("ict_total_score"),
                                                                                            max=Max("ict_total_score"),
                                                                                            min=Min("ict_total_score"))
        phe_scores = PheScores.objects.filter(student_id=student_id, term_id=get_term)
        dat5 = PheScores.objects.filter(classes_id=get_classes, term_id=get_term).aggregate(avg=Avg("phe_total_score"),
                                                                                            max=Max("phe_total_score"),
                                                                                            min=Min("phe_total_score"))
        irs_scores = IrsScores.objects.filter(student_id=student_obj, term_id=get_term)
        dat6 = IrsScores.objects.filter(classes_id=get_classes, term_id=get_term).aggregate(avg=Avg("irs_total_score"),
                                                                                            max=Max("irs_total_score"),
                                                                                            min=Min("irs_total_score"))
        crk_scores = CrkScores.objects.filter(student_id=student_obj, term_id=get_term)
        dat7 = CrkScores.objects.filter(classes_id=get_classes, term_id=get_term).aggregate(avg=Avg("crk_total_score"),
                                                                                            max=Max("crk_total_score"),
                                                                                            min=Min("crk_total_score"))
        quran_scores = QuranScores.objects.filter(student_id=student_obj, term_id=get_term)
        dat8 = QuranScores.objects.filter(classes_id=get_classes, term_id=get_term).aggregate(avg=Avg("quran_total_score"),
                                                                                              max=Max("quran_total_score"),
                                                                                              min=Min("quran_total_score"))

        eng =0
        count1 = 0
        for t in eng_scores:
            eng = t.eng_total_score
            count1 =1


        mth = 0
        count2 = 0
        for m in mth_scores:
            mth = m.mth_total_score
            count2 = 1


        sci = 0
        count3 = 0
        for s in sci_scores:
            sci = s.sci_total_score
            count3 = 1
            print(sci)

        phe = 0
        count4 = 0
        for p in phe_scores:
            phe = p.phe_total_score
            count4 = 1

        nv = 0
        count5 = 0
        for n in nv_scores:
            count5 = 1
            nv = n.nv_total_score


        irs = 0
        count6 = 0
        for i in irs_scores:
            count6 = 1
            irs = i.irs_total_score

        crk = 0
        count7 = 0
        for c in crk_scores:
            count7 = 1
            crk = c.crk_total_score


        quran = 0
        count8 = 0
        for q in quran_scores:
            count8 = 1
            quran = q.quran_total_score

        ict = 0
        count9 = 0
        for i in ict_scores:
            count9 = 1
            ict = i.ict_total_score

        total_score = int(eng) + int(mth) + int(sci) + int(ict) + int(nv) + int(phe) + int(irs) + int(crk) + int(quran)
        counts = count1 + count2 + count3 + count4 + count5 + count6 + count7 + count8 + count9

        #subject_count = Subject.objects.filter(classes_id=c_id).count()
        avg_scr = total_score /counts
        avg_score = round(avg_scr,1)
        #data subject avg but not iterable
        #data5 = EngScores.objects.filter(classes_id=get_classes, term_id=get_term).aggregate(sum=Sum("eng_total_score"),
                                                                             #  max=Max("eng_total_score"),
                                                                              # min=Min("eng_total_score"),
                                                                              # avg=Avg("eng_total_score"),

        agg = BroadSheet.objects.filter(subject_id=subject_id).annotate(score=Sum(F('term1_bs_score') + F('term2_bs_score') + F('total_score')))
        data = BroadSheet.objects.filter(classes_id=get_classes).aggregate(
            avg=Avg("total_score"),
            max=Max("total_score"),
            min=Min("total_score"))
        context={"get_term":get_term, "get_student":get_student,"counts":counts,
                 "total_score":total_score,"broad":broad,
                 "avg_score":avg_score,"dat":dat,"agg":agg,
                 "remarks":remarks,  "dat1":dat1, "dat2":dat2,
                 "dat3": dat3, "dat4":dat4, "dat5":dat5, "dat6":dat6,
                 "dat7": dat7, "dat8":dat8, "data":data,
                 "termdetails":termdetails, "attendance":attendance,
                 "traits":traits, "classes":classes,
                 "student":student, "eng_scores":eng_scores,
                 "mth_scores":mth_scores, "sci_scores":sci_scores,
                 "nv_scores":nv_scores, "ict_scores":ict_scores,
                 "irs_scores":irs_scores, "quran_scores":quran_scores,
                 "crk_scores":crk_scores, "phe_scores":phe_scores}
        if get_term.term_name == "THIRD TERM":
            try:
                return render(request, "admin_template/fetch_results3.html", context)
            except:
                return HttpResponse("<h2>error 505</h2>"
              " <h4>Teacher must enter complete student details before viewing will be available</h4>")
        else:
            return render(request, "admin_template/fetch_results.html", context)
    except:
        return HttpResponse("<h2>error 505</h2>"
                            " <h4>Teacher must enter complete student details before viewing will be available</h4>")

def admin_broadsheet(request, term_id):
    get_term = TermDetails.objects.get(id=term_id)
    total = None
    data = None
    data2 = None
    classes = Classes.objects.all()
    subject = Subject.objects.filter(staff_id=request.user.id)
    session_year = SessionYearModel.object.all()
    action = request.GET.get("action")
    get_classes = None
    get_session_year = None
    term1 = None
    traits = None
    student = None
    if action is not None and request.method == "POST":
        subject = Subject.objects.all()
        classes_id = request.POST.get('classes_id')

        get_term = TermDetails.objects.get(id=term_id)
        session_year_id = request.POST.get('session_year_id')
        get_classes = Classes.objects.get(id=classes_id)
        get_session_year = SessionYearModel.object.get(id=session_year_id)
        # classes = Classes.objects.get(staff_id=request.user.id)
        student = Student.objects.filter(classes_id=classes_id)

        student_id = request.POST.get('student_id')
        term1 = EngScores.objects.filter(student_id=student_id)
        traits = TermTrait.objects.filter(student_id=student_id)

        data = EngScores.objects.all().aggregate(sum=Sum("eng_total_score"), max=Max("eng_total_score"),
                                                 min=Min("eng_total_score"), avg=Avg("eng_total_score"))
        data2 = EngScores.objects.all().count()
    return render(request, "admin_template/view_broadsheet.html", {"get_term": get_term, "traits": traits, "total": total,
                                                                "data2": data2, "data": data,
                                                                "session_year": session_year,
                                                                "classes": classes, "subject": subject,
                                                                "get_classes": get_classes,
                                                                "get_session_year": get_session_year,
                                                                "action": action, "student": student, "term1": term1})


def broadsheet(request):
    try:
        classes_id = request.POST.get("classes_id")
        term_id = request.POST.get("term_id")
        subject_id = request.POST.get("subject_id")

        subject_id = Subject.objects.get(id=subject_id)
        term_obj = TermDetails.objects.get(id=term_id)
        classes_obj = Classes.objects.get(id=classes_id)
        eng_scores = EngScores.objects.filter(subject_id=subject_id,classes_id=classes_obj, term_id=term_obj)
        mth_scores = MthScores.objects.filter(subject_id=subject_id,classes_id=classes_obj, term_id=term_obj)
        sci_scores = SciScores.objects.filter(subject_id=subject_id,classes_id=classes_obj, term_id=term_obj)
        ict_scores = IctScores.objects.filter(subject_id=subject_id,classes_id=classes_obj, term_id=term_obj)
        phe_scores = PheScores.objects.filter(subject_id=subject_id,classes_id=classes_obj, term_id=term_obj)
        irs_scores = IrsScores.objects.filter(subject_id=subject_id,classes_id=classes_obj, term_id=term_obj)
        crk_scores = CrkScores.objects.filter(subject_id=subject_id,classes_id=classes_obj, term_id=term_obj)
        quran_scores = QuranScores.objects.filter(subject_id=subject_id,classes_id=classes_obj, term_id=term_obj)
        nv_scores = NvScores.objects.filter(subject_id=subject_id,classes_id=classes_obj, term_id=term_obj)

        dat = EngScores.objects.filter(classes_id=classes_obj, term_id=term_obj).aggregate(avg=Avg("eng_total_score"),
                                                                              max=Max("eng_total_score"),
                                                                              min=Min("eng_total_score"))
        dat1 = MthScores.objects.filter(classes_id=classes_obj, term_id=term_obj).aggregate(avg=Avg("mth_total_score"),
                                                                                        max=Max("mth_total_score"),
                                                                                        min=Min("mth_total_score"))
        dat2 = SciScores.objects.filter(classes_id=classes_obj, term_id=term_obj).aggregate(avg=Avg("sci_total_score"),
                                                                                            max=Max("sci_total_score"),
                                                                                            min=Min("sci_total_score"))
        dat3 = NvScores.objects.filter(classes_id=classes_obj, term_id=term_obj).aggregate(avg=Avg("nv_total_score"),
                                                                                       max=Max("nv_total_score"),
                                                                                       min=Min("nv_total_score"))
        dat4 = IctScores.objects.filter(classes_id=classes_obj, term_id=term_obj).aggregate(avg=Avg("ict_total_score"),
                                                                                        max=Max("ict_total_score"),
                                                                                        min=Min("ict_total_score"))
        dat5 = PheScores.objects.filter(classes_id=classes_obj, term_id=term_obj).aggregate(avg=Avg("phe_total_score"),
                                                                                        max=Max("phe_total_score"),
                                                                                        min=Min("phe_total_score"))
        dat6 = IrsScores.objects.filter(classes_id=classes_obj, term_id=term_obj).aggregate(avg=Avg("irs_total_score"),
                                                                                        max=Max("irs_total_score"),
                                                                                        min=Min("irs_total_score"))
        dat7 = CrkScores.objects.filter(classes_id=classes_obj, term_id=term_obj).aggregate(avg=Avg("crk_total_score"),
                                                                                        max=Max("crk_total_score"),
                                                                                        min=Min("crk_total_score"))
        dat8 = QuranScores.objects.filter(classes_id=classes_obj, term_id=term_obj).aggregate(avg=Avg("quran_total_score"),
                                                                                          max=Max("quran_total_score"),
                                                                                              min=Min("quran_total_score"))

        context={ "dat":dat,"dat1":dat1, "dat2":dat2,
                 "dat3": dat3, "dat4":dat4, "dat5":dat5, "dat6":dat6,
                 "dat7": dat7, "dat8":dat8, "term_obj":term_obj, "classes_obj":classes_obj,
                  "eng_scores":eng_scores, "subject_id":subject_id,
                 "mth_scores":mth_scores, "sci_scores":sci_scores,
                 "nv_scores":nv_scores, "ict_scores":ict_scores,
                 "irs_scores":irs_scores, "quran_scores":quran_scores,
                 "crk_scores":crk_scores, "phe_scores":phe_scores}

        if term_obj.term_name == "THIRD TERM":
            broad = BroadSheet.objects.filter(subject_id=subject_id)
            data = BroadSheet.objects.filter(subject_id=subject_id).aggregate(
                avg=Avg("total_score"),
                max=Max("total_score"),
                min=Min("total_score"))

            context2 = {"broad":broad, "data":data, "term_obj":term_obj, "classes_obj":classes_obj, "subject_id":subject_id}
            return render(request, "admin_template/broadsheet3.html", context2)
        else:
            return render(request, "admin_template/broadsheet.html", context)
    except:
        return HttpResponse("<h2>error 505</h2>"
                           " <h4>Not available</h4>")

def broadsheet_print(request, term_id, c_id,sub_id):
    try:
        session_year = SessionYearModel.object.all()
        subject_id = Subject.objects.get(id=sub_id)
        term_obj = TermDetails.objects.get(id=term_id)

        classes_obj = Classes.objects.get(id=c_id)
        eng_scores = EngScores.objects.filter(subject_id=subject_id,classes_id=classes_obj, term_id=term_obj)
        mth_scores = MthScores.objects.filter(subject_id=subject_id,classes_id=classes_obj, term_id=term_obj)
        sci_scores = SciScores.objects.filter(subject_id=subject_id,classes_id=classes_obj, term_id=term_obj)
        ict_scores = IctScores.objects.filter(subject_id=subject_id,classes_id=classes_obj, term_id=term_obj)
        phe_scores = PheScores.objects.filter(subject_id=subject_id,classes_id=classes_obj, term_id=term_obj)
        irs_scores = IrsScores.objects.filter(subject_id=subject_id,classes_id=classes_obj, term_id=term_obj)
        crk_scores = CrkScores.objects.filter(subject_id=subject_id,classes_id=classes_obj, term_id=term_obj)
        quran_scores = QuranScores.objects.filter(subject_id=subject_id,classes_id=classes_obj, term_id=term_obj)
        nv_scores = NvScores.objects.filter(subject_id=subject_id,classes_id=classes_obj, term_id=term_obj)




        dat = EngScores.objects.filter(classes_id=classes_obj, term_id=term_obj).aggregate(avg=Avg("eng_total_score"),
                                                                              max=Max("eng_total_score"),
                                                                              min=Min("eng_total_score"))
        dat1 = MthScores.objects.filter(classes_id=classes_obj, term_id=term_obj).aggregate(avg=Avg("mth_total_score"),
                                                                                        max=Max("mth_total_score"),
                                                                                        min=Min("mth_total_score"))
        dat2 = SciScores.objects.filter(classes_id=classes_obj, term_id=term_obj).aggregate(avg=Avg("sci_total_score"),
                                                                                            max=Max("sci_total_score"),
                                                                                            min=Min("sci_total_score"))
        dat3 = NvScores.objects.filter(classes_id=classes_obj, term_id=term_obj).aggregate(avg=Avg("nv_total_score"),
                                                                                       max=Max("nv_total_score"),
                                                                                       min=Min("nv_total_score"))
        dat4 = IctScores.objects.filter(classes_id=classes_obj, term_id=term_obj).aggregate(avg=Avg("ict_total_score"),
                                                                                        max=Max("ict_total_score"),
                                                                                        min=Min("ict_total_score"))
        dat5 = PheScores.objects.filter(classes_id=classes_obj, term_id=term_obj).aggregate(avg=Avg("phe_total_score"),
                                                                                        max=Max("phe_total_score"),
                                                                                        min=Min("phe_total_score"))
        dat6 = IrsScores.objects.filter(classes_id=classes_obj, term_id=term_obj).aggregate(avg=Avg("irs_total_score"),
                                                                                        max=Max("irs_total_score"),
                                                                                        min=Min("irs_total_score"))
        dat7 = CrkScores.objects.filter(classes_id=classes_obj, term_id=term_obj).aggregate(avg=Avg("crk_total_score"),
                                                                                        max=Max("crk_total_score"),
                                                                                        min=Min("crk_total_score"))
        dat8 = QuranScores.objects.filter(classes_id=classes_obj, term_id=term_obj).aggregate(avg=Avg("quran_total_score"),
                                                                                          max=Max("quran_total_score"),
                                                                                              min=Min("quran_total_score"))

        context={ "dat":dat,"dat1":dat1, "dat2":dat2,"classes_obj":classes_obj,
                 "dat3": dat3, "dat4":dat4, "dat5":dat5, "dat6":dat6,
                 "dat7": dat7, "dat8":dat8,"session_year":session_year,
                  "eng_scores":eng_scores, "term_obj":term_obj,
                 "mth_scores":mth_scores, "sci_scores":sci_scores,
                 "nv_scores":nv_scores, "ict_scores":ict_scores,
                 "irs_scores":irs_scores, "quran_scores":quran_scores,
                 "crk_scores":crk_scores, "phe_scores":phe_scores}

        if term_obj.term_name == "THIRD TERM":
            broad = BroadSheet.objects.filter(subject_id=subject_id)
            data = BroadSheet.objects.filter(subject_id=subject_id).aggregate(
                avg=Avg("total_score"),
                max=Max("total_score"),
                min=Min("total_score"))


            #data2=None
            student_obj=None
            #student_id = Student.objects.filter(classes_id=classes_obj)
            #for s in student_id:
               # student_obj = s


            #data2 = BroadSheet.objects.filter(classes_id=classes_obj).annotate(score=Sum(F('term1_bs_score') + F('term2_bs_score') + F('total_score')))

            context = {"broad":broad, "data":data, "term_obj":term_obj,
                       "session_year":session_year,"classes_obj":classes_obj,}
            return render(request, "admin_template/broadsheet-print3.html", context)
        else:
            return render(request, "admin_template/broadsheet-print.html", context)
    except:
        return HttpResponse("<h2>error 505</h2>"
                           " <h4>Not available</h4>")
    #return render(request, "admin_template/broadsheet-print.html",)


def termdetails(request):
    session_year = SessionYearModel.object.all()
    termdetails = TermDetails.objects.all()
    return render(request, "admin_template/term_details.html", {"session_year":session_year, "termdetails":termdetails})


def save_termdetails(request):
    if request.method == "POST":
        session_year = request.POST.get("session_year_id")
        session_year_id = SessionYearModel.object.get(id=session_year)
        term_name = request.POST.get("term_id")
        vacation_date = request.POST.get("vacation_date")
        resumption_date = request.POST.get("resumption_date")
        try:
            data_exists = TermDetails.objects.filter(term_name=term_name).exists()
            if data_exists:
                termdetails = TermDetails.objects.get(term_name=term_name)

                termdetails.save()
                messages.success(request, "Details Updated Successfully")
                return HttpResponseRedirect(reverse("termdetails"))
            else:
                termdetails = TermDetails(session_year_id=session_year_id,term_name=term_name,
                                          vacation_date=vacation_date, resumption_date=resumption_date)
                termdetails.save()
                messages.success(request, "Details Added Successfully")
                return HttpResponseRedirect(reverse("termdetails"))
        except:
            messages.error(request, "Failed To Add Session Details")
            return HttpResponseRedirect(reverse("termdetails"))


def del_termdetails(request, term_id):
    termdetails = TermDetails.objects.get(id=term_id)
    return render(request, "admin_template/del_termdetails.html",{"termdetails":termdetails} )


def delete_termdetails(request):
    if request.method == "POST":
        term_id = request.POST.get("term_id")
        termdetails = TermDetails.objects.get(id=term_id)
        termdetails.delete()
        messages.success(request, "Details Deleted Successfully")
    return HttpResponseRedirect(reverse("termdetails"))


def edit_termdetails(request,term_id):
    termdetails = TermDetails.objects.get(id=term_id)
    return render(request, "admin_template/edit_termdetails.html",{"termdetails":termdetails})


def edit_termdetails_save(request):
    if request.method == "POST":
        term_name = request.POST.get("term_name")
        term_id = request.POST.get("term_id")
        vacation_date = request.POST.get("vacation_date")
        resumption_date = request.POST.get("resumption_date")
        #termdetails = TermDetails.objects.get(id=term_id)

        data_exists = TermDetails.objects.filter(id=term_id).exists()
        if data_exists:
            try:
                termdetails = TermDetails.objects.get(id=term_id)
                termdetails.term_name = term_name,
                termdetails.vacation_date = vacation_date,
                termdetails.resumption_date = resumption_date,
                termdetails.save()
                messages.success(request, "Details Updated Successfully")
                return HttpResponseRedirect(reverse("termdetails"))
            except:
                messages.error(request, "Failed")
                return HttpResponseRedirect(reverse("termdetails"))

        else:
            return HttpResponse("does not exist")




def calendar(request):
    return render(request, "admin_template/calendar.html")


def admin_inv_print(request, term_id, s_id):
    try:
        term_obj = TermDetails.objects.get(id=term_id)
        termdetails = TermDetails.objects.filter(id=term_id)
        student_obj = Student.objects.get(id=s_id)
        broad = BroadSheet.objects.filter(student_id=student_obj)
        get_traits = TermTrait.objects.get(student_id=s_id, term_id=term_id)

        c_id = get_traits.student_id.classes_id.id
        get_classes = Classes.objects.get(id=c_id)
        traits = TermTrait.objects.filter(student_id=student_obj, term_id=term_obj)

        classes = Classes.objects.all()
        attendance = Attendance.objects.filter(student_id=student_obj, term_id=term_obj)

        remarks = TermRemarks.objects.filter(student_id=student_obj, term_id=term_obj)
        get_student = Student.objects.get(id=s_id)
        # data for subject scores on each total
        # Book.objects.annotate(num_authors=Count('authors')).aggregate(Avg('num_authors'))
        eng_scores = EngScores.objects.filter(student_id=student_obj, term_id=term_obj)
        dat = EngScores.objects.filter(classes_id=get_classes, term_id=term_obj).aggregate(avg=Avg("eng_total_score"),
                                                                                           max=Max("eng_total_score"),
                                                                                           min=Min("eng_total_score"))
        mth_scores = MthScores.objects.filter(student_id=student_obj, term_id=term_obj)
        dat1 = MthScores.objects.filter(classes_id=get_classes, term_id=term_obj).aggregate(avg=Avg("mth_total_score"),
                                                                                            max=Max("mth_total_score"),
                                                                                            min=Min("mth_total_score"))
        sci_scores = SciScores.objects.filter(student_id=student_obj, term_id=term_obj)
        dat2 = SciScores.objects.filter(classes_id=get_classes, term_id=term_obj).aggregate(avg=Avg("sci_total_score"),
                                                                                            max=Max("sci_total_score"),
                                                                                            min=Min("sci_total_score"))
        nv_scores = NvScores.objects.filter(student_id=student_obj, term_id=term_obj)
        dat3 = NvScores.objects.filter(classes_id=get_classes, term_id=term_obj).aggregate(avg=Avg("nv_total_score"),
                                                                                           max=Max("nv_total_score"),
                                                                                           min=Min("nv_total_score"))
        ict_scores = IctScores.objects.filter(student_id=student_obj, term_id=term_obj)
        dat4 = IctScores.objects.filter(classes_id=get_classes, term_id=term_obj).aggregate(avg=Avg("ict_total_score"),
                                                                                            max=Max("ict_total_score"),
                                                                                            min=Min("ict_total_score"))
        phe_scores = PheScores.objects.filter(student_id=student_obj, term_id=term_obj)
        dat5 = PheScores.objects.filter(classes_id=get_classes, term_id=term_obj).aggregate(avg=Avg("phe_total_score"),
                                                                                            max=Max("phe_total_score"),
                                                                                            min=Min("phe_total_score"))
        irs_scores = IrsScores.objects.filter(student_id=student_obj, term_id=term_obj)
        dat6 = IrsScores.objects.filter(classes_id=get_classes, term_id=term_obj).aggregate(avg=Avg("irs_total_score"),
                                                                                            max=Max("irs_total_score"),
                                                                                            min=Min("irs_total_score"))
        crk_scores = CrkScores.objects.filter(student_id=student_obj, term_id=term_obj)
        dat7 = CrkScores.objects.filter(classes_id=get_classes, term_id=term_obj).aggregate(avg=Avg("crk_total_score"),
                                                                                            max=Max("crk_total_score"),
                                                                                            min=Min("crk_total_score"))
        quran_scores = QuranScores.objects.filter(student_id=student_obj, term_id=term_obj)
        dat8 = QuranScores.objects.filter(classes_id=get_classes, term_id=term_obj).aggregate(
            avg=Avg("quran_total_score"),
            max=Max("quran_total_score"),
            min=Min("quran_total_score"))

        eng = 0
        count1 = 0
        for t in eng_scores:
            eng = t.eng_total_score
            count1 = 1
            print(eng)

        mth = 0
        count2 = 0
        for m in mth_scores:
            mth = m.mth_total_score
            count2 = 1
            print(mth)

        sci = 0
        count3 = 0
        for s in sci_scores:
            sci = s.sci_total_score
            count3 = 1
            print(sci)

        phe = 0
        count4 = 0
        for p in phe_scores:
            phe = p.phe_total_score
            count4 = 1

        nv = 0
        count5 = 0
        for n in nv_scores:
            count5 = 1
            nv = n.nv_total_score

        irs = 0
        count6 = 0
        for i in irs_scores:
            count6 = 1
            irs = i.irs_total_score

        crk = 0
        count7 = 0
        for c in crk_scores:
            count7 = 1
            crk = c.crk_total_score

        quran = 0
        count8 = 0
        for q in quran_scores:
            count8 = 1
            quran = q.quran_total_score

        ict = 0
        count9 = 0
        for i in ict_scores:
            count9 = 1
            ict = i.ict_total_score

        total_score = int(eng) + int(mth) + int(sci) + int(ict) + int(nv) + int(phe) + int(irs) + int(crk) + int(quran)
        counts = count1 + count2 + count3 + count4 + count5 + count6 + count7 + count8 + count9
        avg_scr = total_score / counts
        avg_score = round(avg_scr, 1)
        data = BroadSheet.objects.filter(classes_id=get_classes).aggregate(
            avg=Avg("total_score"),
            max=Max("total_score"),
            min=Min("total_score"))
        context = {"get_student": get_student, "counts": counts,
                   "total_score": total_score, "broad": broad,
                   "avg_score": avg_score, "dat": dat,
                   "remarks": remarks, "dat1": dat1, "dat2": dat2,
                   "dat3": dat3, "dat4": dat4, "dat5": dat5, "dat6": dat6,
                   "dat7": dat7, "dat8": dat8, "data": data,
                   "termdetails": termdetails, "attendance": attendance,
                   "traits": traits, "classes": classes,
                   "student_obj": student_obj, "eng_scores": eng_scores,
                   "mth_scores": mth_scores, "sci_scores": sci_scores,
                   "nv_scores": nv_scores, "ict_scores": ict_scores,
                   "irs_scores": irs_scores, "quran_scores": quran_scores,
                   "crk_scores": crk_scores, "phe_scores": phe_scores}
        if term_obj.term_name == "THIRD TERM":
            try:
                return render(request, "admin_template/invoice-print3.html", context)
            except:
                return HttpResponse("<h2>error 505</h2>"
                                    " <h4>Teacher must enter complete student details before viewing will be available</h4>")
        else:
            return render(request, "admin_template/invoice-print.html", context)
    except:
        return HttpResponse("<h2>error 506</h2>"
                           " <h4>un-available</h4>")



def admin_remarks(request, term_id):
    get_term = TermDetails.objects.get(id=term_id)
    classes = Classes.objects.all()
    classes_id = None
    for c in classes:
        classes_id = c.id

    subject = Subject.objects.filter(staff_id=request.user.id)
    session_year = SessionYearModel.object.all()
    action = request.GET.get("action")
    get_classes = None
    get_session_year = None
    student = None
    if action is not None and request.method == "POST":
        get_term = TermDetails.objects.get(id=term_id)
        classes_id = request.POST.get('classes_id')
        session_year_id = request.POST.get('session_year_id')
        get_classes = Classes.objects.get(id=classes_id)
        get_session_year = SessionYearModel.object.get(id=session_year_id)
        student = Student.objects.filter(classes_id=classes_id)
    return render(request, "admin_template/admin_remarks.html", {"get_term":get_term, "session_year":session_year, "classes":classes, "subject":subject, "get_classes":get_classes,  "get_session_year":get_session_year, "action":action, "student":student})



def admin_save_remarks(request):
    if request.method =="POST":
        student_id = request.POST.get("student_id")
        term_id = request.POST.get("term_id")
        teachers_remark = request.POST.get("teachers_remark")
        principals_remark = request.POST.get("principals_remark")
        get_student = Student.objects.get(id=student_id)
        get_term = TermDetails.objects.get(id=term_id)
        try:
            data_exists = TermRemarks.objects.filter(student_id=get_student, term_id=get_term).exists()
            if data_exists:
                termremarks = TermRemarks.objects.get(student_id=get_student, term_id=get_term)
                termremarks.principals_remark = principals_remark
                termremarks.save()
                messages.success(request, "Remarks Successfully Updated")
                return HttpResponseRedirect(reverse("admin_remarks",   kwargs={"term_id":term_id}))
            else:
                termremarks = TermRemarks(student_id=get_student,
                                          principals_remark=principals_remark,
                                          term_id=get_term)
                termremarks.save()
                messages.success(request, "Remarks Saved")
                return HttpResponseRedirect(reverse("admin_remarks",   kwargs={"term_id":term_id}))
        except:
            messages.error(request, "Failed To Add Remarks")
            return HttpResponseRedirect(reverse("admin_remarks", kwargs={"term_id": term_id}))
