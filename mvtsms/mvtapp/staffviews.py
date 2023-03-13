import json

from mysql import connector as con
from django.contrib import messages
from django.contrib.postgres import serializers
from django.db.models import Sum, Max, Min, Avg,Count

from django.urls import reverse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect

from mvtapp.models import CustomUser,BroadSheet, TermDetails, MthScores, EngScores, NvScores, IctScores, PheScores, IrsScores, SciScores, CrkScores, QuranScores, TermRemarks, TermTrait, Attendance, Classes, SessionYearModel, Student, Staff, Subject, StaffLeave



def staffhome(request):
    staff = Staff.objects.get(admin=request.user.id)
    student = Student.objects.filter(classes_id=request.user.id).count()
    student_m_gender = Student.objects.filter(gender="male").count()
    term = TermDetails.objects.all()
    return render(request, "staff_template/home_content.html", {"term":term, "staff":staff, "student":student, "student_m_gender":student_m_gender})


def takeattendance(request,term_id):
    session_year_id = SessionYearModel.object.all()
    classes = Classes.objects.filter(staff_id=request.user.id)
    classes_id = Classes.objects.get(staff_id=request.user.id)
    student = Student.objects.filter(classes_id=classes_id)
    term_ = TermDetails.objects.get(id=term_id)
    return render(request, "staff_template/take_attendance.html", {"term_":term_, "session_year_id": session_year_id, "classes":classes, "student": student})


def saveattendance(request):
    if request.method == "POST":
        classes_id = request.POST.get('classes_id')
        student_id = request.POST.get("student_id")
        term_id = request.POST.get("term_id")
        times_absent = request.POST.get("times_abs_id")
        times_open = request.POST.get("times_open")
        times_present = int(times_open) - int(times_absent)
        get_student = Student.objects.get(admin=student_id)
        session_year_id = request.POST.get("session_year_id")
        get_session_year = SessionYearModel.object.get(id=session_year_id)
        get_classes = Classes.objects.get(id=classes_id)
        get_term = TermDetails.objects.get(id=term_id)
        try:
            data_exists = Attendance.objects.filter(term_id=get_term, student_id=get_student, classes_id=get_classes, session_year_id=get_session_year).exists()
            if data_exists:
                attendance = Attendance.objects.get(
                    student_id=get_student,
                    classes_id=get_classes,
                    session_year_id=get_session_year,
                    term_id=get_term,
                )
                attendance.times_absent = times_absent
                attendance.times_open = times_open
                attendance.times_present = times_present
                attendance.save()
                messages.success(request, "You Have Successfully Updated Attendance")
                return HttpResponseRedirect(reverse("takeattendance", kwargs={"term_id":term_id}))


            else:
                attendance = Attendance(
                    student_id=get_student,
                    classes_id=get_classes,
                    session_year_id=get_session_year,
                    term_id=get_term,
                    times_absent=times_absent,
                    times_open=times_open,
                    times_present=times_present,
                )
                attendance.save()
                messages.success(request, "You Have Successfully Added Attendance")
                return HttpResponseRedirect(reverse("takeattendance", kwargs={"term_id":term_id}))
        except:
            messages.error(request, "Failed To Take Attendance")
            return HttpResponseRedirect(reverse("takeattendance", kwargs={"term_id": term_id}))
    else:
        return HttpResponse("error 505")


def view_attendance(request, id):
    staff = Staff.objects.get(admin=request.user.id)
    classes_id = Classes.objects.get(staff_id=request.user.id)
    attendance = Attendance.objects.filter(classes_id=classes_id, term_id=id)
    get_term = TermDetails.objects.get(id=id)
    return render(request, "staff_template/view_attendance.html", {"get_term":get_term, "attendance": attendance, "staff": staff})


def staffleave(request):
    staff = CustomUser.objects.filter(user_type=2)
    return render(request, "staff_template/staff_leave.html", {"staff":staff})

def staffleave_save(request):
    if request.method == "POST":
        leave_date = request.POST.get("leave_date")
        leave_message = request.POST.get("leave_message")
        staff = Staff.objects.get(admin=request.user.id)
        try:
            staffleave = StaffLeave(staff_id = staff,leave_date=leave_date, leave_message=leave_message, leave_status=False)
            staffleave.save()
            messages.success(request, "You Have Successfully Applied For Leave")
            return HttpResponseRedirect("/staffleave")
        except:
            messages.error(request, " Leave Application Failed")
            return HttpResponseRedirect("/staffleave")

def leavehistory(request):
    staff = Staff.objects.get(admin=request.user.id)
    staff_id = Staff.objects.get(admin=request.user.id)
    staffleave = StaffLeave.objects.filter(staff_id=staff_id)
    return render(request, "staff_template/leave_history.html", {"staffleave":staffleave, "staff":staff})

def addresult(request):
    session_year = SessionYearModel.object.all()
    subject = None
    student = None
    staff = Staff.objects.get(admin=request.user.id)
    classes = Classes.objects.filter(staff_id=request.user.id)
    get_classes = None
    get_term = None
    action = request.GET.get("action")
    term = TermDetails.objects.all()
    if action is not None and request.method == "POST":
        classes_id = request.POST.get('classes_id')
        session_year_id = request.POST.get('session_year_id')
        term_id = request.POST.get('term_id')
        get_term =TermDetails.objects.get(id=term_id)
        get_classes = Classes.objects.get(id=classes_id)
        get_session_year = SessionYearModel.object.get(id=session_year_id)
        #classes = Classes.objects.get(staff_id=request.user.id)
        student_id = request.POST.get('student_id')
        student = Student.objects.filter(classes_id=classes_id)
        subject = Subject.objects.filter(classes_id=classes_id)
    return render(request, "staff_template/add_result.html", {"get_term":get_term, "term":term, "get_classes":get_classes, "student":student, "session_year":session_year, "classes":classes, "subject":subject, "action":action,"staff":staff })


def saveresult_term1(request):
    if request.method == "POST":
        student_id = request.POST.get('student_id')
        classes_id = request.POST.get('classes_id')
        subject_id = request.POST.get('subject_id')
        term_id = request.POST.get('term_id')
        get_term = TermDetails.objects.all()

        #ENGLISH
        eng_score1 = request.POST.get('score1')
        eng_score2 = request.POST.get('score2')
        eng_score3 = request.POST.get('score3')
        eng_project_score = request.POST.get('project')
        eng_exam_score = request.POST.get('exam')
        eng_remarks = request.POST.get('remarks')
        eng_total_score = int(eng_score1) + int(eng_score2) + int(eng_score3) + int(eng_project_score) + int(eng_exam_score)

         #MATH
        mth_score1 = request.POST.get('score1')
        mth_score2 = request.POST.get('score2')
        mth_score3 = request.POST.get('score3')
        mth_project_score = request.POST.get('project')
        mth_exam_score = request.POST.get('exam')
        mth_remarks = request.POST.get('remarks')
        mth_total_score = int(mth_score1) + int(mth_score2) + int(mth_score3) + int(mth_project_score) + int(mth_exam_score)


        #SCI
        sci_score1 = request.POST.get('score1')
        sci_score2 = request.POST.get('score2')
        sci_score3 = request.POST.get('score3')
        sci_project_score = request.POST.get('project')
        sci_exam_score = request.POST.get('exam')
        sci_remarks = request.POST.get('remarks')
        sci_total_score = int(sci_score1) + int(sci_score2) + int(sci_score3) + int(sci_project_score) + int(sci_exam_score)

        # ICT
        ict_score1 = request.POST.get('score1')
        ict_score2 = request.POST.get('score2')
        ict_score3 = request.POST.get('score3')
        ict_project_score = request.POST.get('project')
        ict_exam_score = request.POST.get('exam')
        ict_remarks = request.POST.get('remarks')
        ict_total_score = int(ict_score1) + int(ict_score2) + int(ict_score3) + int(ict_project_score) + int(
            ict_exam_score)

        # NV
        nv_score1 = request.POST.get('score1')
        nv_score2 = request.POST.get('score2')
        nv_score3 = request.POST.get('score3')
        nv_project_score = request.POST.get('project')
        nv_exam_score = request.POST.get('exam')
        nv_remarks = request.POST.get('remarks')
        nv_total_score = int(nv_score1) + int(nv_score2) + int(nv_score3) + int(nv_project_score) + int(
            nv_exam_score)

        # PHE
        phe_score1 = request.POST.get('score1')
        phe_score2 = request.POST.get('score2')
        phe_score3 = request.POST.get('score3')
        phe_project_score = request.POST.get('project')
        phe_exam_score = request.POST.get('exam')
        phe_remarks = request.POST.get('remarks')
        phe_total_score = int(phe_score1) + int(phe_score2) + int(phe_score3) + int(phe_project_score) + int(
            phe_exam_score)

        # IRS
        irs_score1 = request.POST.get('score1')
        irs_score2 = request.POST.get('score2')
        irs_score3 = request.POST.get('score3')
        irs_project_score = request.POST.get('project')
        irs_exam_score = request.POST.get('exam')
        irs_remarks = request.POST.get('remarks')
        irs_total_score = int(irs_score1) + int(irs_score2) + int(irs_score3) + int(irs_project_score) + int(
            irs_exam_score)

        # CRK
        crk_score1 = request.POST.get('score1')
        crk_score2 = request.POST.get('score2')
        crk_score3 = request.POST.get('score3')
        crk_project_score = request.POST.get('project')
        crk_exam_score = request.POST.get('exam')
        crk_remarks = request.POST.get('remarks')
        crk_total_score = int(crk_score1) + int(crk_score2) + int(crk_score3) + int(crk_project_score) + int(
            crk_exam_score)

        # QURAN
        quran_score1 = request.POST.get('score1')
        quran_score2 = request.POST.get('score2')
        quran_score3 = request.POST.get('score3')
        quran_project_score = request.POST.get('project')
        quran_exam_score = request.POST.get('exam')
        quran_remarks = request.POST.get('remarks')
        quran_total_score = int(quran_score1) + int(quran_score2) + int(quran_score3) + int(quran_project_score) + int(
            quran_exam_score)

        get_student = Student.objects.get(admin=student_id)
        get_subject = Subject.objects.get(id=subject_id)
        get_classes = Classes.objects.get(id=classes_id)
        subject = Subject.objects.get(classes_id=get_classes, id=subject_id)
        get_term = TermDetails.objects.get(id=term_id)

        try:
            eng_exists = EngScores.objects.filter(student_id=get_student, classes_id=get_classes,
                                                        subject_id=get_subject, term_id=get_term).exists()
            mth_exists = MthScores.objects.filter(student_id=get_student, classes_id=get_classes,
                                                       subject_id=get_subject, term_id=get_term).exists()
            sci_exists = SciScores.objects.filter(student_id=get_student, classes_id=get_classes,
                                                       subject_id=get_subject, term_id=get_term).exists()
            nv_exists = NvScores.objects.filter(student_id=get_student, classes_id=get_classes,
                                                  subject_id=get_subject, term_id=get_term).exists()
            ict_exists = IctScores.objects.filter(student_id=get_student, classes_id=get_classes,
                                                  subject_id=get_subject, term_id=get_term).exists()
            phe_exists = PheScores.objects.filter(student_id=get_student, classes_id=get_classes,
                                                  subject_id=get_subject, term_id=get_term).exists()
            irs_exists = IrsScores.objects.filter(student_id=get_student, classes_id=get_classes,
                                                  subject_id=get_subject, term_id=get_term).exists()
            crk_exists = CrkScores.objects.filter(student_id=get_student, classes_id=get_classes,
                                                  subject_id=get_subject, term_id=get_term).exists()
            quran_exists = QuranScores.objects.filter(student_id=get_student, classes_id=get_classes,
                                                  subject_id=get_subject, term_id=get_term).exists()
            if eng_exists:
                eng_score = EngScores.objects.get(
                    student_id=get_student,
                    classes_id=get_classes,
                    subject_id=get_subject,
                    term_id=get_term,
                )
                eng_score.eng_score1 = eng_score1
                eng_score.eng_score2 = eng_score2
                eng_score.eng_score3 = eng_score3
                eng_score.eng_project_score = eng_project_score
                eng_score.eng_exam_score = eng_exam_score
                eng_score.eng_remarks = eng_remarks
                eng_score.eng_total_score = eng_total_score
                # firsttermscore.first_term_avg = first_term_avg
                eng_score.save()
                if get_term.term_name == "First Term 2022/2023":
                    try:
                        eng_bs = BroadSheet.objects.get(
                            student_id=get_student,
                            classes_id=get_classes,
                            subject_id=get_subject,

                        )
                        eng_bs.term1_bs_score = eng_total_score
                        eng_bs.save()
                        messages.success(request, "You Have Successfully Updated First Term English Results")
                        return HttpResponseRedirect(reverse("addresult"))
                    except:
                        return HttpResponse("not first term")

                elif get_term.term_name == "Second Term 2022/2023":
                    try:
                        eng_bs = BroadSheet.objects.get(
                            student_id=get_student,
                            classes_id=get_classes,
                            subject_id=get_subject,

                        )
                        eng_bs.term2_bs_score = eng_total_score
                        eng_bs.save()
                        messages.success(request, "You Have Successfully Updated Second Term English Results")
                        return HttpResponseRedirect(reverse("addresult"))
                    except:
                        return HttpResponse("not sec term")

                else:
                    try:
                        eng_bs = BroadSheet.objects.get(
                            student_id=get_student,
                            classes_id=get_classes,
                            subject_id=get_subject,

                        )
                        eng_bs.score1 = eng_score1,
                        eng_bs.score2 = eng_score2,
                        eng_bs.score3 = eng_score3,
                        eng_bs.project_score = eng_project_score,
                        eng_bs.exam_score = eng_exam_score,
                        eng_bs.total_score = eng_total_score,
                        #eng_bs.grand_total_score = int(eng_bs.eng_bs_score) + int(eng_bs.eng_bs_score2) + int(eng_total_score)
                        eng_bs.save()
                        messages.success(request, "You Have Successfully Updated Third Term English Results")
                        return HttpResponseRedirect(reverse("addresult"))
                    except:
                        return HttpResponse("not third term")

            elif mth_exists:
                mth_score = MthScores.objects.get(
                    student_id=get_student,
                    classes_id=get_classes,
                    subject_id=get_subject,
                    term_id=get_term,
                )
                mth_score.first_mth_score1 = mth_score1
                mth_score.first_mth_score2 = mth_score2
                mth_score.first_mth_score3 = mth_score3
                mth_score.first_mth_project_score = mth_project_score
                mth_score.first_mth_exam_score = mth_exam_score
                mth_score.first_mth_remarks = mth_remarks
                mth_score.first_mth_total_score = mth_total_score
                # firsttermscore.first_term_avg = first_term_avg
                mth_score.save()

                if get_term.term_name == "First Term 2022/2023":
                    try:
                        mth_bs = BroadSheet.objects.get(
                            student_id=get_student,
                            classes_id=get_classes,
                            subject_id=get_subject,

                        )
                        mth_bs.term1_bs_score = mth_total_score
                        mth_bs.save()
                        messages.success(request, "You Have Successfully Updated First Term Maths Results")
                        return HttpResponseRedirect(reverse("addresult"))
                    except:
                        return HttpResponse("not first term")

                elif get_term.term_name == "Second Term 2022/2023":
                    try:
                        mth_bs = BroadSheet.objects.get(
                            student_id=get_student,
                            classes_id=get_classes,
                            subject_id=get_subject,

                        )
                        mth_bs.term2_bs_score = mth_total_score
                        mth_bs.save()
                        messages.success(request, "You Have Successfully Updated Second Term Maths Results")
                        return HttpResponseRedirect(reverse("addresult"))
                    except:
                        return HttpResponse("not sec term")

                else:
                    try:
                        mth_bs = BroadSheet.objects.get(
                            student_id=get_student,
                            classes_id=get_classes,
                            subject_id=get_subject,

                        )
                        mth_bs.score1 = mth_score1,
                        mth_bs.score2 = mth_score2,
                        mth_bs.score3 = mth_score3,
                        mth_bs.project_score = mth_project_score,
                        mth_bs.exam_score = mth_exam_score,
                        mth_bs.total_score = mth_total_score,
                        # eng_bs.grand_total_score = int(eng_bs.eng_bs_score) + int(eng_bs.eng_bs_score2) + int(eng_total_score)
                        mth_bs.save()
                        messages.success(request, "You Have Successfully Updated Third Term Maths Results")
                        return HttpResponseRedirect(reverse("addresult"))
                    except:
                        return HttpResponse("not third term")
            elif sci_exists:
                sci_score = SciScores.objects.get(
                    student_id=get_student,
                    classes_id=get_classes,
                    subject_id=get_subject,
                    term_id=get_term,
                )

                sci_score.sci_score1 = sci_score1
                sci_score.sci_score2 = sci_score2
                sci_score.sci_score3 = sci_score3
                sci_score.sci_project_score = sci_project_score
                sci_score.sci_exam_score = sci_exam_score
                sci_score.sci_remarks = sci_remarks
                sci_score.sci_total_score = sci_total_score
                # firsttermscore.first_term_avg = first_term_avg
                sci_score.save()

                if get_term.term_name == "First Term 2022/2023":
                    try:
                        sc_bs = BroadSheet.objects.get(
                            student_id=get_student,
                            classes_id=get_classes,
                            subject_id=get_subject,

                        )
                        sc_bs.term1_bs_score = sci_total_score
                        sc_bs.save()
                        messages.success(request, "You Have Successfully Updated First Term Science Results")
                        return HttpResponseRedirect(reverse("addresult"))
                    except:
                        return HttpResponse("not first term")
                elif get_term.term_name == "Second Term 2022/2023":
                    try:
                        sc_bs = BroadSheet.objects.get(
                            student_id=get_student,
                            classes_id=get_classes,
                            subject_id=get_subject,

                        )
                        sc_bs.term2_bs_score = sci_total_score
                        sc_bs.save()
                        messages.success(request, "You Have Successfully Updated Second Term Science Results")
                        return HttpResponseRedirect(reverse("addresult"))
                    except:
                        return HttpResponse("not sec term")

                else:
                    try:
                        sc_bs = BroadSheet.objects.get(
                            student_id=get_student,
                            classes_id=get_classes,
                            subject_id=get_subject,

                        )
                        sc_bs.score1 = sci_score1,
                        sc_bs.score2 = sci_score2,
                        sc_bs.score3 = sci_score3,
                        sc_bs.project_score = sci_project_score,
                        sc_bs.exam_score = sci_exam_score,
                        sc_bs.total_score = sci_total_score,
                        # eng_bs.grand_total_score = int(eng_bs.eng_bs_score) + int(eng_bs.eng_bs_score2) + int(eng_total_score)
                        sc_bs.save()
                        messages.success(request, "You Have Successfully Updated Third Term Science Results")
                        return HttpResponseRedirect(reverse("addresult"))
                    except:
                        return HttpResponse("not third term")

            elif nv_exists:
                nv_score = NvScores.objects.get(
                    student_id=get_student,
                    classes_id=get_classes,
                    subject_id=get_subject,
                    term_id=get_term,
                )

                nv_score.nv_score1 = nv_score1
                nv_score.nv_score2 = nv_score2
                nv_score.nv_score3 = nv_score3
                nv_score.nv_project_score = nv_project_score
                nv_score.nv_exam_score = nv_exam_score
                nv_score.nv_remarks = nv_remarks
                nv_score.nv_total_score = nv_total_score
                # firsttermscore.first_term_avg = first_term_avg
                nv_score.save()

                if get_term.term_name == "First Term 2022/2023":
                    try:
                        nv_bs = BroadSheet.objects.get(
                            student_id=get_student,
                            classes_id=get_classes,
                            subject_id=get_subject,

                        )
                        nv_bs.term1_bs_score = nv_total_score
                        nv_bs.save()
                        messages.success(request, "You Have Successfully Updated First Term Nat Values Results")
                        return HttpResponseRedirect(reverse("addresult"))
                    except:
                        return HttpResponse("not first term")
                elif get_term.term_name == "Second Term 2022/2023":
                    try:
                        nv_bs = BroadSheet.objects.get(
                            student_id=get_student,
                            classes_id=get_classes,
                            subject_id=get_subject,

                        )
                        nv_bs.term2_bs_score = nv_total_score
                        nv_bs.save()
                        messages.success(request, "You Have Successfully Updated Second Term Nat Values Results")
                        return HttpResponseRedirect(reverse("addresult"))
                    except:
                        return HttpResponse("not sec term")

                else:
                    try:
                        nv_bs = BroadSheet.objects.get(
                            student_id=get_student,
                            classes_id=get_classes,
                            subject_id=get_subject,

                        )
                        nv_bs.score1 = nv_score1,
                        nv_bs.score2 = nv_score2,
                        nv_bs.score3 = nv_score3,
                        nv_bs.project_score = nv_project_score,
                        nv_bs.exam_score = nv_exam_score,
                        nv_bs.total_score = nv_total_score,
                        # eng_bs.grand_total_score = int(eng_bs.eng_bs_score) + int(eng_bs.eng_bs_score2) + int(eng_total_score)
                        nv_bs.save()
                        messages.success(request, "You Have Successfully Updated Third Term Nat Values  Results")
                        return HttpResponseRedirect(reverse("addresult"))
                    except:
                        return HttpResponse("not third term")
            elif ict_exists:
                ict_score = IctScores.objects.get(
                    student_id=get_student,
                    classes_id=get_classes,
                    subject_id=get_subject,
                    term_id=get_term,
                )

                ict_score.ict_score1 = ict_score1
                ict_score.ict_score2 = ict_score2
                ict_score.ict_score3 = ict_score3
                ict_score.ict_project_score = ict_project_score
                ict_score.ict_exam_score = ict_exam_score
                ict_score.ict_remarks = ict_remarks
                ict_score.ict_total_score = ict_total_score
                # firsttermscore.first_term_avg = first_term_avg
                ict_score.save()

                if get_term.term_name == "First Term 2022/2023":
                    try:
                        ict_bs = BroadSheet.objects.get(
                            student_id=get_student,
                            classes_id=get_classes,
                            subject_id=get_subject,

                        )
                        ict_bs.term1_bs_score = ict_total_score
                        ict_bs.save()
                        messages.success(request, "You Have Successfully Updated First Term Ict Results")
                        return HttpResponseRedirect(reverse("addresult"))
                    except:
                        return HttpResponse("not first term")
                elif get_term.term_name == "Second Term 2022/2023":
                    try:
                        ict_bs = BroadSheet.objects.get(
                            student_id=get_student,
                            classes_id=get_classes,
                            subject_id=get_subject,

                        )
                        ict_bs.term2_bs_score = ict_total_score
                        ict_bs.save()
                        messages.success(request, "You Have Successfully Updated Second Term Ict Results")
                        return HttpResponseRedirect(reverse("addresult"))
                    except:
                        return HttpResponse("not sec term")

                else:
                    try:
                        ict_bs = BroadSheet.objects.get(
                            student_id=get_student,
                            classes_id=get_classes,
                            subject_id=get_subject,

                        )
                        ict_bs.score1 = ict_score1,
                        ict_bs.score2 = ict_score2,
                        ict_bs.score3 = ict_score3,
                        ict_bs.project_score = ict_project_score,
                        ict_bs.exam_score = ict_exam_score,
                        ict_bs.total_score = ict_total_score,
                        # eng_bs.grand_total_score = int(eng_bs.eng_bs_score) + int(eng_bs.eng_bs_score2) + int(eng_total_score)
                        ict_bs.save()
                        messages.success(request, "You Have Successfully Updated Third Term Ict Results")
                        return HttpResponseRedirect(reverse("addresult"))
                    except:
                        return HttpResponse("not third term")
            elif phe_exists:
                phe_score = PheScores.objects.get(
                    student_id=get_student,
                    classes_id=get_classes,
                    subject_id=get_subject,
                    term_id=get_term,
                )

                phe_score.phe_score1 = phe_score1
                phe_score.phe_score2 = phe_score2
                phe_score.phe_score3 = phe_score3
                phe_score.phe_project_score = phe_project_score
                phe_score.phe_exam_score = phe_exam_score
                phe_score.phe_remarks = phe_remarks
                phe_score.phe_total_score = phe_total_score
                # firsttermscore.first_term_avg = first_term_avg
                phe_score.save()

                if get_term.term_name == "First Term 2022/2023":
                    try:
                        phe_bs = BroadSheet.objects.get(
                            student_id=get_student,
                            classes_id=get_classes,
                            subject_id=get_subject,

                        )
                        phe_bs.term1_bs_score = phe_total_score
                        phe_bs.save()
                        messages.success(request, "You Have Successfully Updated First Term Phe Results")
                        return HttpResponseRedirect(reverse("addresult"))
                    except:
                        return HttpResponse("not first term")
                elif get_term.term_name == "Second Term 2022/2023":
                    try:
                        phe_bs = BroadSheet.objects.get(
                            student_id=get_student,
                            classes_id=get_classes,
                            subject_id=get_subject,

                        )
                        phe_bs.term2_bs_score = phe_total_score
                        phe_bs.save()
                        messages.success(request, "You Have Successfully Updated Second Term Phe Results")
                        return HttpResponseRedirect(reverse("addresult"))
                    except:
                        return HttpResponse("not sec term")

                else:
                    try:
                        phe_bs = BroadSheet.objects.get(
                            student_id=get_student,
                            classes_id=get_classes,
                            subject_id=get_subject,

                        )
                        phe_bs.score1 = phe_score1,
                        phe_bs.score2 = phe_score2,
                        phe_bs.score3 = phe_score3,
                        phe_bs.project_score = phe_project_score,
                        phe_bs.exam_score = phe_exam_score,
                        phe_bs.total_score = phe_total_score,
                        # eng_bs.grand_total_score = int(eng_bs.eng_bs_score) + int(eng_bs.eng_bs_score2) + int(eng_total_score)
                        phe_bs.save()
                        messages.success(request, "You Have Successfully Updated Third Term Phe Results")
                        return HttpResponseRedirect(reverse("addresult"))
                    except:
                        return HttpResponse("not third term")
            elif irs_exists:
                irs_score = IrsScores.objects.get(
                    student_id=get_student,
                    classes_id=get_classes,
                    subject_id=get_subject,
                    term_id=get_term,
                )

                irs_score.irs_score1 = irs_score1
                irs_score.irs_score2 = irs_score2
                irs_score.irs_score3 = irs_score3
                irs_score.irs_project_score = irs_project_score
                irs_score.irs_exam_score = irs_exam_score
                irs_score.irs_remarks = irs_remarks
                irs_score.irs_total_score = irs_total_score
                # firsttermscore.first_term_avg = first_term_avg
                irs_score.save()

                if get_term.term_name == "First Term 2022/2023":
                    try:
                        irs_bs = BroadSheet.objects.get(
                            student_id=get_student,
                            classes_id=get_classes,
                            subject_id=get_subject,

                        )
                        irs_bs.term1_bs_score = irs_total_score
                        irs_bs.save()
                        messages.success(request, "You Have Successfully Updated First Term Irs Results")
                        return HttpResponseRedirect(reverse("addresult"))
                    except:
                        return HttpResponse("not first term")
                elif get_term.term_name == "Second Term 2022/2023":
                    try:
                        irs_bs = BroadSheet.objects.get(
                            student_id=get_student,
                            classes_id=get_classes,
                            subject_id=get_subject,

                        )
                        irs_bs.term2_bs_score = irs_total_score
                        irs_bs.save()
                        messages.success(request, "You Have Successfully Updated Second Term Irs Results")
                        return HttpResponseRedirect(reverse("addresult"))
                    except:
                        return HttpResponse("ENTER COMPLETE DETAILS")

                else:
                    try:
                        irs_bs = BroadSheet.objects.get(
                            student_id=get_student,
                            classes_id=get_classes,
                            subject_id=get_subject,

                        )
                        irs_bs.score1 = irs_score1,
                        irs_bs.score2 = irs_score2,
                        irs_bs.score3 = irs_score3,
                        irs_bs.project_score = irs_project_score,
                        irs_bs.exam_score = irs_exam_score,
                        irs_bs.total_score = irs_total_score,
                        # eng_bs.grand_total_score = int(eng_bs.eng_bs_score) + int(eng_bs.eng_bs_score2) + int(eng_total_score)
                        irs_bs.save()
                        messages.success(request, "You Have Successfully Updated Third Term Irs Results")
                        return HttpResponseRedirect(reverse("addresult"))
                    except:
                        return HttpResponse("ENTER COMPLETE DETAILS")
            elif crk_exists:
                crk_score = CrkScores.objects.get(
                    student_id=get_student,
                    classes_id=get_classes,
                    subject_id=get_subject,
                    term_id=get_term,
                )

                crk_score.crk_score1 = crk_score1
                crk_score.crk_score2 = crk_score2
                crk_score.crk_score3 = crk_score3
                crk_score.crk_project_score = crk_project_score
                crk_score.crk_exam_score = crk_exam_score
                crk_score.crk_remarks = crk_remarks
                crk_score.crk_total_score = crk_total_score
                # firsttermscore.first_term_avg = first_term_avg
                crk_score.save()

                if get_term.term_name == "First Term 2022/2023":
                    try:
                        crk_bs = BroadSheet.objects.get(
                            student_id=get_student,
                            classes_id=get_classes,
                            subject_id=get_subject,

                        )
                        crk_bs.term1_bs_score = crk_total_score
                        crk_bs.save()
                        messages.success(request, "You Have Successfully Updated First Term Crk Results")
                        return HttpResponseRedirect(reverse("addresult"))
                    except:
                        return HttpResponse("not first term")
                elif get_term.term_name == "Second Term 2022/2023":
                    try:
                        crk_bs = BroadSheet.objects.get(
                            student_id=get_student,
                            classes_id=get_classes,
                            subject_id=get_subject,
                        )
                        crk_bs.term2_bs_score = crk_total_score
                        crk_bs.save()
                        messages.success(request, "You Have Successfully Updated Second Term Crk Results")
                        return HttpResponseRedirect(reverse("addresult"))
                    except:
                        return HttpResponse("ENTER COMPLETE DETAILS")

                else:
                    try:
                        crk_bs = BroadSheet.objects.get(
                            student_id=get_student,
                            classes_id=get_classes,
                            subject_id=get_subject,

                        )
                        crk_bs.score1 = crk_score1,
                        crk_bs.score2 = crk_score2,
                        crk_bs.score3 = crk_score3,
                        crk_bs.project_score = crk_project_score,
                        crk_bs.exam_score = crk_exam_score,
                        crk_bs.total_score = crk_total_score,
                        # eng_bs.grand_total_score = int(eng_bs.eng_bs_score) + int(eng_bs.eng_bs_score2) + int(eng_total_score)
                        crk_bs.save()
                        messages.success(request, "You Have Successfully Updated Third Term Crk Results")
                        return HttpResponseRedirect(reverse("addresult"))
                    except:
                        return HttpResponse("ENTER COMPLETE DETAILS")
            elif quran_exists:
                quran_score = QuranScores.objects.get(
                    student_id=get_student,
                    classes_id=get_classes,
                    subject_id=get_subject,
                    term_id=get_term,
                )

                quran_score.quran_score1 = quran_score1
                quran_score.quran_score2 = quran_score2
                quran_score.quran_score3 = quran_score3
                quran_score.quran_project_score = quran_project_score
                quran_score.quran_exam_score = quran_exam_score
                quran_score.quran_remarks = quran_remarks
                quran_score.quran_total_score = quran_total_score
                # firsttermscore.first_term_avg = first_term_avg
                quran_score.save()

                if get_term.term_name == "First Term 2022/2023":
                    try:
                        quran_bs = BroadSheet.objects.get(
                            student_id=get_student,
                            classes_id=get_classes,
                            subject_id=get_subject,

                        )
                        quran_bs.term1_bs_score = quran_total_score
                        quran_bs.save()
                        messages.success(request, "You Have Successfully Updated First Term Quran Results")
                        return HttpResponseRedirect(reverse("addresult"))
                    except:
                        return HttpResponse("not first term")
                elif get_term.term_name == "Second Term 2022/2023":
                    try:
                        quran_bs = BroadSheet.objects.get(
                            student_id=get_student,
                            classes_id=get_classes,
                            subject_id=get_subject,

                        )
                        quran_bs.term2_bs_score = quran_total_score
                        quran_bs.save()
                        messages.success(request, "You Have Successfully Updated Second Term Quran Results")
                        return HttpResponseRedirect(reverse("addresult"))
                    except:
                        return HttpResponse("ENTER COMPLETE DETAILS")

                else:
                    try:
                        quran_bs = BroadSheet.objects.get(
                            student_id=get_student,
                            classes_id=get_classes,
                            subject_id=get_subject,

                        )
                        quran_bs.score1 = quran_score1,
                        quran_bs.score2 = quran_score2,
                        quran_bs.score3 = quran_score3,
                        quran_bs.project_score = quran_project_score,
                        quran_bs.exam_score = quran_exam_score,
                        quran_bs.total_score = quran_total_score,
                        # eng_bs.grand_total_score = int(eng_bs.eng_bs_score) + int(eng_bs.eng_bs_score2) + int(eng_total_score)
                        quran_bs.save()
                        messages.success(request, "You Have Successfully Updated Third Term Quran Results")
                        return HttpResponseRedirect(reverse("addresult"))
                    except:
                        return HttpResponse("ENTER COMPLETE DETAILS")

            elif not eng_exists and subject.subject_name =="ENGLISH LANGUAGE":
                eng_score = EngScores(
                    student_id=get_student,
                    classes_id=get_classes,
                    subject_id=get_subject,
                    term_id=get_term,
                    eng_score1=eng_score1,
                    eng_score2=eng_score2,
                    eng_score3=eng_score3,
                    eng_project_score=eng_project_score,
                    eng_exam_score=eng_exam_score,
                    eng_remarks=eng_remarks,
                    eng_total_score=eng_total_score,
                    # first_term_avg=first_term_avg,
                )
                eng_score.save()
                if get_term.term_name == "First Term 2022/2023":
                    eng_bs = BroadSheet(
                        student_id=get_student,
                        classes_id=get_classes,
                        subject_id=get_subject,
                        term1_bs_score=eng_total_score,

                    )
                    eng_bs.save()
                    messages.success(request, "You Have Successfully Added First Term English Results")
                    return HttpResponseRedirect(reverse("addresult"))
                elif get_term.term_name == "Second Term 2022/2023":
                    eng_bs = BroadSheet.objects.get(
                        student_id=get_student,
                        classes_id=get_classes,
                        subject_id=get_subject,
                    )
                    eng_bs.term2_bs_score = eng_total_score
                    eng_bs.save()
                    messages.success(request, "You Have Successfully Added Second Term English Results")
                    return HttpResponseRedirect(reverse("addresult"))
                else:
                    eng_bs = BroadSheet.objects.get(
                        student_id=get_student,
                        classes_id=get_classes,
                        subject_id=get_subject,
                    )
                    eng_bs.score1 = eng_score1
                    eng_bs.score2 = eng_score2
                    eng_bs.score3 = eng_score3
                    eng_bs.project_score = eng_project_score
                    eng_bs.exam_score = eng_exam_score
                    eng_bs.total_score = eng_total_score
                    eng_bs.save()
                    messages.success(request, "You Have Successfully Added Third Term English Results")
                    return HttpResponseRedirect(reverse("addresult"))


            elif not mth_exists and subject.subject_name =="MATHEMATICS":
                mth_score = MthScores(
                    student_id=get_student,
                    classes_id=get_classes,
                    subject_id=get_subject,
                    term_id=get_term,
                    mth_score1=mth_score1,
                    mth_score2=mth_score2,
                    mth_score3=mth_score3,
                    mth_project_score=mth_project_score,
                    mth_exam_score=mth_exam_score,
                    mth_remarks=mth_remarks,
                    mth_total_score=mth_total_score,
                    #first_term_avg=first_term_avg,
                )
                mth_score.save()

                if get_term.term_name == "First Term 2022/2023":
                    mth_bs = BroadSheet(
                        student_id=get_student,
                        classes_id=get_classes,
                        subject_id=get_subject,
                        term1_bs_score=mth_total_score,
                    )
                    mth_bs.save()
                    messages.success(request, "You Have Successfully Added First Term Maths Results")
                    return HttpResponseRedirect(reverse("addresult"))

                elif get_term.term_name == "Second Term 2022/2023":
                    mth_bs = BroadSheet.objects.get(
                        student_id=get_student,
                        classes_id=get_classes,
                        subject_id=get_subject,
                    )
                    mth_bs.term2_bs_score = mth_total_score
                    mth_bs.save()
                    messages.success(request, "You Have Successfully Added Second Term Maths Results")
                    return HttpResponseRedirect(reverse("addresult"))
                else:
                    mth_bs = BroadSheet.objects.get(
                        student_id=get_student,
                        classes_id=get_classes,
                        subject_id=get_subject,
                    )
                    mth_bs.score1 = mth_score1
                    mth_bs.score2 = mth_score2
                    mth_bs.score3 = mth_score3
                    mth_bs.project_score = mth_project_score
                    mth_bs.exam_score = mth_exam_score
                    mth_bs.total_score = mth_total_score
                    mth_bs.save()
                    messages.success(request, "You Have Successfully Added Third Term Maths Results")
                    return HttpResponseRedirect(reverse("addresult"))


            elif not sci_exists and subject.subject_name =="SCIENCE":
                sci_score = SciScores(
                    student_id=get_student,
                    classes_id=get_classes,
                    subject_id=get_subject,
                    term_id=get_term,
                    sci_score1=sci_score1,
                    sci_score2=sci_score2,
                    sci_score3=sci_score3,
                    sci_project_score=sci_project_score,
                    sci_exam_score=sci_exam_score,
                    sci_remarks=sci_remarks,
                    sci_total_score=sci_total_score,
                    #first_term_avg=first_term_avg,
                )
                sci_score.save()

                if get_term.term_name == "First Term 2022/2023":
                    sci_bs = BroadSheet(
                        student_id=get_student,
                        classes_id=get_classes,
                        subject_id=get_subject,
                        term1_bs_score=sci_total_score,
                    )
                    sci_bs.save()
                    messages.success(request, "You Have Successfully Added First Term Science Results")
                    return HttpResponseRedirect(reverse("addresult"))
                elif get_term.term_name == "Second Term 2022/2023":
                    sci_bs = BroadSheet.objects.get(
                        student_id=get_student,
                        classes_id=get_classes,
                        subject_id=get_subject,
                    )
                    sci_bs.term2_bs_score = sci_total_score
                    sci_bs.save()
                    messages.success(request, "You Have Successfully Added Second Term Science Results")
                    return HttpResponseRedirect(reverse("addresult"))
                else:
                    sci_bs = BroadSheet.objects.get(
                        student_id=get_student,
                        classes_id=get_classes,
                        subject_id=get_subject,
                    )
                    sci_bs.score1 = sci_score1
                    sci_bs.score2 = sci_score2
                    sci_bs.score3 = sci_score3
                    sci_bs.project_score = sci_project_score
                    sci_bs.exam_score = sci_exam_score
                    sci_bs.total_score = sci_total_score
                    sci_bs.save()
                    messages.success(request, "You Have Successfully Added Third Term Science Results")
                    return HttpResponseRedirect(reverse("addresult"))

            elif not ict_exists and subject.subject_name =="ICT":
                ict_score =  SciScores(
                    student_id=get_student,
                    classes_id=get_classes,
                    subject_id=get_subject,
                    term_id=get_term,
                    ict_score1=ict_score1,
                    ict_score2=ict_score2,
                    ict_score3=ict_score3,
                    ict_project_score=ict_project_score,
                    ict_exam_score=ict_exam_score,
                    ict_remarks=ict_remarks,
                    ict_total_score=ict_total_score,
                    #first_term_avg=first_term_avg,
                )
                ict_score.save()

                if get_term.term_name == "First Term 2022/2023":
                    ict_bs = BroadSheet(
                        student_id=get_student,
                        classes_id=get_classes,
                        subject_id=get_subject,
                        term1_bs_score=ict_total_score,
                    )
                    ict_bs.save()
                    messages.success(request, "You Have Successfully Added First Term Ict Results")
                    return HttpResponseRedirect(reverse("addresult"))
                elif get_term.term_name == "Second Term 2022/2023":
                    ict_bs = BroadSheet.objects.get(
                        student_id=get_student,
                        classes_id=get_classes,
                        subject_id=get_subject,
                    )
                    ict_bs.term2_bs_score = ict_total_score
                    ict_bs.save()
                    messages.success(request, "You Have Successfully Added Second Term Ict Results")
                    return HttpResponseRedirect(reverse("addresult"))
                else:
                    ict_bs = BroadSheet.objects.get(
                        student_id=get_student,
                        classes_id=get_classes,
                        subject_id=get_subject,
                    )
                    ict_bs.score1 = ict_score1
                    ict_bs.score2 = ict_score2
                    ict_bs.score3 = ict_score3
                    ict_bs.project_score = ict_project_score
                    ict_bs.exam_score = ict_exam_score
                    ict_bs.total_score = ict_total_score
                    ict_bs.save()
                    messages.success(request, "You Have Successfully Added Third Term Ict Results")
                    return HttpResponseRedirect(reverse("addresult"))

            elif not phe_exists and subject.subject_name =="PHE":
                phe_score = PheScores(
                    student_id=get_student,
                    classes_id=get_classes,
                    subject_id=get_subject,
                    term_id=get_term,
                    phe_score1=phe_score1,
                    phe_score2=phe_score2,
                    phe_score3=phe_score3,
                    phe_project_score=phe_project_score,
                    phe_exam_score=phe_exam_score,
                    phe_remarks=phe_remarks,
                    phe_total_score=phe_total_score,
                    #first_term_avg=first_term_avg,
                )
                phe_score.save()

                if get_term.term_name == "First Term 2022/2023":
                    phe_bs = BroadSheet(
                        student_id=get_student,
                        classes_id=get_classes,
                        subject_id=get_subject,
                        term1_bs_score=phe_total_score,
                    )
                    phe_bs.save()
                    messages.success(request, "You Have Successfully Added First Term Phe Results")
                    return HttpResponseRedirect(reverse("addresult"))
                elif get_term.term_name == "Second Term 2022/2023":
                    phe_bs = BroadSheet.objects.get(
                        student_id=get_student,
                        classes_id=get_classes,
                        subject_id=get_subject,
                    )
                    phe_bs.term2_bs_score = phe_total_score
                    phe_bs.save()
                    messages.success(request, "You Have Successfully Added Second Term Phe Results")
                    return HttpResponseRedirect(reverse("addresult"))
                else:
                    phe_bs = BroadSheet.objects.get(
                        student_id=get_student,
                        classes_id=get_classes,
                        subject_id=get_subject,
                    )
                    phe_bs.score1 = phe_score1
                    phe_bs.score2 = phe_score2
                    phe_bs.score3 = phe_score3
                    phe_bs.project_score = phe_project_score
                    phe_bs.exam_score = phe_exam_score
                    phe_bs.total_score = phe_total_score
                    phe_bs.save()
                    messages.success(request, "You Have Successfully Added Third Term Phe Results")
                    return HttpResponseRedirect(reverse("addresult"))

            elif not irs_exists and subject.subject_name =="IRS":
                irs_score = IrsScores(
                    student_id=get_student,
                    classes_id=get_classes,
                    subject_id=get_subject,
                    term_id=get_term,
                    irs_score1=irs_score1,
                    irs_score2=irs_score2,
                    irs_score3=irs_score3,
                    irs_project_score=irs_project_score,
                    irs_exam_score=irs_exam_score,
                    irs_remarks=irs_remarks,
                    irs_total_score=irs_total_score,
                    #first_term_avg=first_term_avg,
                )
                irs_score.save()

                if get_term.term_name == "First Term 2022/2023":
                    irs_bs = BroadSheet(
                        student_id=get_student,
                        classes_id=get_classes,
                        subject_id=get_subject,
                        term1_bs_score=irs_total_score,
                    )
                    irs_bs.save()
                    messages.success(request, "You Have Successfully Added First Term Irs Results")
                    return HttpResponseRedirect(reverse("addresult"))
                elif get_term.term_name == "Second Term 2022/2023":
                    irs_bs = BroadSheet.objects.get(
                        student_id=get_student,
                        classes_id=get_classes,
                        subject_id=get_subject,
                    )
                    irs_bs.term2_bs_score = irs_total_score
                    irs_bs.save()
                    messages.success(request, "You Have Successfully Added Second Term Irs Results")
                    return HttpResponseRedirect(reverse("addresult"))
                else:
                    irs_bs = BroadSheet.objects.get(
                        student_id=get_student,
                        classes_id=get_classes,
                        subject_id=get_subject,
                    )
                    irs_bs.score1 = irs_score1
                    irs_bs.score2 = irs_score2
                    irs_bs.score3 = irs_score3
                    irs_bs.project_score = irs_project_score
                    irs_bs.exam_score = irs_exam_score
                    irs_bs.total_score = irs_total_score
                    irs_bs.save()
                    messages.success(request, "You Have Successfully Added Third Term Irs Results")
                    return HttpResponseRedirect(reverse("addresult"))

            elif not crk_exists and subject.subject_name =="CRK":
                crk_score = CrkScores(
                    student_id=get_student,
                    classes_id=get_classes,
                    subject_id=get_subject,
                    term_id=get_term,
                    crk_score1=crk_score1,
                    crk_score2=crk_score2,
                    crk_score3=crk_score3,
                    crk_project_score=crk_project_score,
                    crk_exam_score=crk_exam_score,
                    crk_remarks=crk_remarks,
                    crk_total_score=crk_total_score,
                    #first_term_avg=first_term_avg,
                )
                crk_score.save()

                if get_term.term_name == "First Term 2022/2023":
                    crk_bs = BroadSheet(
                        student_id=get_student,
                        classes_id=get_classes,
                        subject_id=get_subject,
                        term1_bs_score=crk_total_score,
                    )
                    crk_bs.save()
                    messages.success(request, "You Have Successfully Added First Term Crk Results")
                    return HttpResponseRedirect(reverse("addresult"))
                elif get_term.term_name == "Second Term 2022/2023":
                    crk_bs = BroadSheet.objects.get(
                        student_id=get_student,
                        classes_id=get_classes,
                        subject_id=get_subject,
                    )
                    crk_bs.term2_bs_score = crk_total_score
                    crk_bs.save()
                    messages.success(request, "You Have Successfully Added Second Term Crk Results")
                    return HttpResponseRedirect(reverse("addresult"))
                else:
                    crk_bs = BroadSheet.objects.get(
                        student_id=get_student,
                        classes_id=get_classes,
                        subject_id=get_subject,
                    )
                    crk_bs.score1 = crk_score1
                    crk_bs.score2 = crk_score2
                    crk_bs.score3 = crk_score3
                    crk_bs.project_score = crk_project_score
                    crk_bs.exam_score = crk_exam_score
                    crk_bs.total_score = crk_total_score
                    crk_bs.save()
                    messages.success(request, "You Have Successfully Added Third Term Crk Results")
                    return HttpResponseRedirect(reverse("addresult"))

            elif not nv_exists and subject.subject_name =="NATIONAL VALUES":
                nv_score = NvScores(
                    student_id=get_student,
                    classes_id=get_classes,
                    subject_id=get_subject,
                    term_id=get_term,
                    nv_score1=nv_score1,
                    nv_score2=nv_score2,
                    nv_score3=nv_score3,
                    nv_project_score=nv_project_score,
                    nv_exam_score=nv_exam_score,
                    nv_remarks=nv_remarks,
                    nv_total_score=nv_total_score,
                    #first_term_avg=first_term_avg,
                )
                nv_score.save()

                if get_term.term_name == "First Term 2022/2023":
                    nv_bs = BroadSheet(
                        student_id=get_student,
                        classes_id=get_classes,
                        subject_id=get_subject,
                        term1_bs_score=nv_total_score,
                    )
                    nv_bs.save()
                    messages.success(request, "You Have Successfully Added First Term Nat Values Results")
                    return HttpResponseRedirect(reverse("addresult"))
                elif get_term.term_name == "Second Term 2022/2023":
                    nv_bs = BroadSheet.objects.get(
                        student_id=get_student,
                        classes_id=get_classes,
                        subject_id=get_subject,
                    )
                    nv_bs.term2_bs_score = nv_total_score
                    nv_bs.save()
                    messages.success(request, "You Have Successfully Added Second Term Nat values Results")
                    return HttpResponseRedirect(reverse("addresult"))
                else:
                    nv_bs = BroadSheet.objects.get(
                        student_id=get_student,
                        classes_id=get_classes,
                        subject_id=get_subject,
                    )
                    nv_bs.score1 = nv_score1
                    nv_bs.score2 = nv_score2
                    nv_bs.score3 = nv_score3
                    nv_bs.project_score = nv_project_score
                    nv_bs.exam_score = nv_exam_score
                    nv_bs.total_score = nv_total_score
                    nv_bs.save()
                    messages.success(request, "You Have Successfully Added Third Term Nat Values Results")
                    return HttpResponseRedirect(reverse("addresult"))

            elif not quran_exists and subject.subject_name =="QURAN STUDIES":
                quran_score = QuranScores(
                    student_id=get_student,
                    classes_id=get_classes,
                    subject_id=get_subject,
                    term_id=get_term,
                    quran_score1=quran_score1,
                    quran_score2=quran_score2,
                    quran_score3=quran_score3,
                    quran_project_score=quran_project_score,
                    quran_exam_score=quran_exam_score,
                    quran_remarks=quran_remarks,
                    quran_total_score=quran_total_score,
                    #first_term_avg=first_term_avg,
                )
                quran_score.save()

                if get_term.term_name == "First Term 2022/2023":
                    quran_bs = BroadSheet(
                        student_id=get_student,
                        classes_id=get_classes,
                        subject_id=get_subject,
                        term1_bs_score=quran_total_score,
                    )
                    quran_bs.save()
                    messages.success(request, "You Have Successfully Added First Term Quran Results")
                    return HttpResponseRedirect(reverse("addresult"))
                elif get_term.term_name == "Second Term 2022/2023":
                    quran_bs = BroadSheet.objects.get(
                        student_id=get_student,
                        classes_id=get_classes,
                        subject_id=get_subject,
                    )
                    quran_bs.term2_bs_score = quran_total_score
                    quran_bs.save()
                    messages.success(request, "You Have Successfully Added Second Term Quran Results")
                    return HttpResponseRedirect(reverse("addresult"))
                else:
                    quran_bs = BroadSheet.objects.get(
                        student_id=get_student,
                        classes_id=get_classes,
                        subject_id=get_subject,
                    )
                    quran_bs.score1 = quran_score1
                    quran_bs.score2 = quran_score2
                    quran_bs.score3 = quran_score3
                    quran_bs.project_score = quran_project_score
                    quran_bs.exam_score = quran_exam_score
                    quran_bs.total_score = quran_total_score
                    quran_bs.save()
                    messages.success(request, "You Have Successfully Added Third Term Quran Results")
                    return HttpResponseRedirect(reverse("addresult"))
            else:
                messages.success(request, "caught no subject")
                return HttpResponseRedirect(reverse("addresult"))

        except ValueError as v:
            messages.error(request, v)
            return HttpResponseRedirect("/addresult")
        except con.Error as c:
            messages.error(request, c)
            return HttpResponseRedirect("/addresult")
        except TypeError as t:
            messages.error(request, t)
            return HttpResponseRedirect("/addresult")
        except NameError as n:
            messages.error(request, n)
            return HttpResponseRedirect("/addresult")
        except Exception as e:
            messages.error(request, e)
            return HttpResponseRedirect("/addresult")
        except:
            messages.error(request, " Result Addition Failed")
            return HttpResponseRedirect(reverse("addresult"))
    else:
        return HttpResponse("error 505")


def viewresults(request):
    total = None
    data = None
    data2 = None
    classes = Classes.objects.filter(staff_id=request.user.id)
    staff = Staff.objects.get(admin=request.user.id)
    subject = Subject.objects.filter(staff_id=request.user.id)
    session_year = SessionYearModel.object.all()
    action = request.GET.get("action")
    classes_id = Classes.objects.get(staff_id=request.user.id)
    student = Student.objects.filter(classes_id=classes_id)
    get_classes = None
    get_session_year = None

    traits = None
    attendance = None
    dat = None
    dat1 = None
    dat2 = None
    dat3 = None
    dat4 = None
    dat5 = None
    dat6 = None
    dat7 = None
    dat8 = None

    get_term = TermDetails.objects.all()
    eng_scores = None
    mth_scores = None
    sci_scores = None
    nv_scores = None
    ict_scores = None
    irs_scores = None
    phe_scores = None
    quran_scores = None
    crk_scores = None

    if action is not None and request.method == "POST":
        term_id = request.POST.get('term_id')
        get_term = TermDetails.objects.get(id=term_id)
        classes_id = request.POST.get('classes_id')
        session_year_id = request.POST.get('session_year_id')
        get_classes = Classes.objects.get(id=classes_id)
        get_session_year = SessionYearModel.object.get(id=session_year_id)
        classes = Classes.objects.get(staff_id=request.user.id)
        student_id = request.POST.get('student_id')
        student_obj = Student.objects.get(id=student_id)


        traits = TermTrait.objects.filter(student_id=student_obj, term_id=get_term )
        attendance = Attendance.objects.filter(student_id=student_obj, term_id=get_term)

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


        data = EngScores.objects.all().aggregate(sum=Sum("eng_total_score"), max=Max("eng_total_score"),
                                                      min=Min("eng_total_score"), avg=Avg("eng_total_score"))
        data2 = EngScores.objects.all().count()


    return render(request, "staff_template/view_results.html", {"get_term":get_term, "dat":dat, "dat1":dat1, "dat2":dat2, "dat3":dat3, "dat4":dat4, "attendance":attendance,
                                                                "dat5":dat5, "dat6":dat6, "dat7":dat7, "dat8":dat8, "traits":traits, "total":total, "data2":data2,
                                                                "data":data, "session_year":session_year,
                                                                "classes":classes, "subject":subject,
                                                                "get_classes":get_classes,
                                                                "get_session_year":get_session_year, "action":action,
                                                                "student":student, "staff":staff,
                                                                "mth_scores":mth_scores,
                                                                "nv_scores":nv_scores,
                                                                "phe_scores":phe_scores,
                                                                "irs_scores":irs_scores,
                                                                "crk_scores":crk_scores,
                                                                "quran_scores":quran_scores,
                                                                "ict_scores":ict_scores,
                                                                "eng_scores":eng_scores,
                                                                "sci_scores":sci_scores})



def invoice(request):
    classes = Classes.objects.get(staff_id=request.user.id)
    student_id = Student.objects.get(classes_id=classes)
    term1 = EngScores.objects.filter(student_id=student_id)
    return render(request, "staff_template/invoice-print.html", {"term1":term1})


def traits(request, term_id):
    classes = Classes.objects.filter(staff_id=request.user.id)
    session_year = SessionYearModel.object.all()
    classes_id = Classes.objects.get(staff_id=request.user.id)
    student = Student.objects.filter(classes_id=classes_id)
    get_term = TermDetails.objects.get(id=term_id)
    return render(request, "staff_template/traits.html", {"get_term":get_term, "classes":classes,  "session_year":session_year, "student":student})


def savetraits(request):
    if request.method == "POST":
        student_id = request.POST.get('student_id')
        term_id = request.POST.get('term_id')
        punctuality = request.POST.get('Punctuality')
        reliability = request.POST.get('Reliability')
        neatness = request.POST.get('Neatness')
        honesty = request.POST.get('Honesty')
        leadership = request.POST.get('Leadership')
        politeness = request.POST.get('Politeness')
        relationship = request.POST.get('Relationship')
        attentiveness = request.POST.get('Attentiveness')
        self_discipline = request.POST.get('Self-discipline')
        perseverance = request.POST.get('Perseverance')
        handwriting = request.POST.get('Handwriting')
        sports = request.POST.get('Sports')
        drawing = request.POST.get('Drawing')
        craft = request.POST.get('Craft')
        musical = request.POST.get('Music')
        get_student = Student.objects.get(admin=student_id)
        get_term = TermDetails.objects.get(id=term_id)
        try:
            data_exists = TermTrait.objects.filter(student_id=get_student, term_id=get_term).exists()
            if data_exists:
                firsttermtrait = TermTrait.objects.get(
                    student_id=get_student,
                    term_id=get_term,
                )
                firsttermtrait.punctuality = punctuality
                firsttermtrait.reliability = reliability
                firsttermtrait.neatness = neatness
                firsttermtrait.honesty = honesty
                firsttermtrait.leadership = leadership
                firsttermtrait.politeness = politeness
                firsttermtrait.relationship = relationship
                firsttermtrait.attentiveness = attentiveness
                firsttermtrait.self_discipline = self_discipline
                firsttermtrait.perseverance = perseverance
                firsttermtrait.handwriting = handwriting
                firsttermtrait.drawing = drawing
                firsttermtrait.craft = craft
                firsttermtrait.musical = musical
                firsttermtrait.sports = sports
                firsttermtrait.save()
                messages.success(request, "You Have Successfully Updated Learners Traits")
                return HttpResponseRedirect(reverse("traits", kwargs={"term_id": term_id}))

            else:
                firsttermtrait = TermTrait(
                    student_id=get_student,
                    term_id=get_term,
                    punctuality=punctuality,
                    reliability=reliability,
                    neatness=neatness,
                    honesty=honesty,
                    leadership=leadership,
                    politeness=politeness,
                    relationship=relationship,
                    attentiveness=attentiveness,
                    self_discipline=self_discipline,
                    perseverance=perseverance,
                    handwriting=handwriting,
                    drawing=drawing,
                    craft=craft,
                    musical=musical,
                    sports=sports,
                )
                firsttermtrait.save()
                messages.success(request, "You Have Successfully Added A Learner Traits")
                return HttpResponseRedirect(reverse("traits", kwargs={"term_id": term_id}))
        except:
            messages.error(request, " Traits Addition Failed")
            return HttpResponseRedirect(reverse("traits", kwargs={"term_id": term_id}))
    else:
        return HttpResponse("error 505")

def staff_remarks(request):
    classes_id = Classes.objects.get(staff_id=request.user.id)
    student = Student.objects.filter(classes_id = classes_id)
    terms = TermDetails.objects.all()
    session_year = SessionYearModel.object.all()
    action = request.GET.get("action")
    classes_id = Classes.objects.get(staff_id=request.user.id)
    action = request.GET.get("action")
    get_session_year = None
    student =None
    if action is not None and request.method == "POST":
        term_id = request.POST.get('term_id')
        session_year_id = request.POST.get('session_year_id')
        terms = TermDetails.objects.get(id=term_id)
        get_session_year = SessionYearModel.object.get(id=session_year_id)
        student = Student.objects.filter(classes_id=classes_id)
    classes = Classes.objects.filter(staff_id=request.user.id)
    session_year = SessionYearModel.object.all()

    return render(request, "staff_template/staff_remarks.html",
                  {"terms":terms, "session_year": session_year, "classes": classes,
                   "get_session_year": get_session_year, "action": action,"student":student})


def staff_save_remarks(request):
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
                termremarks.teachers_remark = teachers_remark
                termremarks.save()
                messages.success(request, "Remarks Successfully Updated")
                return HttpResponseRedirect(reverse("staff_remarks"))
            else:
                termremarks = TermRemarks(student_id=get_student, teachers_remark=teachers_remark, term_id=get_term )
                termremarks.save()
                messages.success(request, "Remarks Saved")
                return HttpResponseRedirect(reverse("staff_remarks"))
        except:
            messages.error(request, "Failed To Add Remarks")
            return HttpResponseRedirect(reverse("staff_remarks"))



