from django.contrib import messages
from django.db.models import Sum, Min, Avg, Count, Max
from django.http import HttpResponse
from django.shortcuts import render

from mvtapp.models import Student,BroadSheet, Parent, CustomUser, TermRemarks, EngScores,\
    TermTrait, Classes, Attendance, TermDetails, NvScores,SciScores,IctScores, IrsScores,\
    QuranScores,CrkScores,PheScores,MthScores


def parenthome(request):
    parent = Parent.objects.get(admin=request.user.id)
    term = TermDetails.objects.all()
    return render(request, "parent_template/home_content.html", {"term":term, "parent":parent})

def email_details(request, term_id):
    get_term = TermDetails.objects.get(id=term_id)
    return render(request, "parent_template/email_details.html",{"get_term":get_term})


def checkresults(request):
    try:
        email_id = request.POST.get('email_id')
        student_user = CustomUser.objects.get(email=email_id)
        student = Student.objects.get(admin=student_user)
        student_list = Student.objects.filter(admin=student_user)
        term_id = request.POST.get('term_id')
        get_term = TermDetails.objects.get(id=term_id)

        c_id = student.classes_id.id
        remarks = TermRemarks.objects.filter(student_id=student, term_id=get_term)
        broad = BroadSheet.objects.filter(student_id=c_id)

        traits = TermTrait.objects.filter(student_id=student, term_id=get_term)

        attendance = Attendance.objects.filter(student_id=student, term_id=get_term)
        termdetails = TermDetails.objects.filter(id=term_id)

        eng_scores = EngScores.objects.filter(student_id=student, term_id=get_term)
        dat = EngScores.objects.filter(classes_id=c_id, term_id=get_term).aggregate(avg=Avg("eng_total_score"),
                                                                                    max=Max("eng_total_score"),
                                                                                    min=Min("eng_total_score"))
        mth_scores = MthScores.objects.filter(student_id=student, term_id=get_term)
        dat1 = MthScores.objects.filter(classes_id=c_id, term_id=get_term).aggregate(avg=Avg("mth_total_score"),
                                                                                     max=Max("mth_total_score"),
                                                                                     min=Min("mth_total_score"))
        nv_scores = NvScores.objects.filter(student_id=student, term_id=get_term)
        dat3 = NvScores.objects.filter(classes_id=c_id, term_id=get_term).aggregate(avg=Avg("nv_total_score"),
                                                                                    max=Max("nv_total_score"),
                                                                                    min=Min("nv_total_score"))
        ict_scores = IctScores.objects.filter(student_id=student, term_id=get_term)
        dat4 = IctScores.objects.filter(classes_id=c_id, term_id=get_term).aggregate(avg=Avg("ict_total_score"),
                                                                                     max=Max("ict_total_score"),
                                                                                     min=Min("ict_total_score"))
        phe_scores = PheScores.objects.filter(student_id=student, term_id=get_term)
        dat5 = PheScores.objects.filter(classes_id=c_id, term_id=get_term).aggregate(avg=Avg("phe_total_score"),
                                                                                     max=Max("phe_total_score"),
                                                                                     min=Min("phe_total_score"))
        sci_scores = SciScores.objects.filter(student_id=student, term_id=get_term)
        dat2 = SciScores.objects.filter(classes_id=c_id, term_id=get_term).aggregate(avg=Avg("sci_total_score"),
                                                                                     max=Max("sci_total_score"),
                                                                                     min=Min("sci_total_score"))
        irs_scores = IrsScores.objects.filter(student_id=student, term_id=get_term)
        dat6 = IrsScores.objects.filter(classes_id=c_id, term_id=get_term).aggregate(avg=Avg("irs_total_score"),
                                                                                     max=Max("irs_total_score"),
                                                                                     min=Min("irs_total_score"))
        crk_scores = CrkScores.objects.filter(student_id=student, term_id=get_term)
        dat7 = CrkScores.objects.filter(classes_id=c_id, term_id=get_term).aggregate(avg=Avg("crk_total_score"),
                                                                                     max=Max("crk_total_score"),
                                                                                     min=Min("crk_total_score"))
        quran_scores = QuranScores.objects.filter(student_id=student, term_id=get_term)
        dat8 = QuranScores.objects.filter(classes_id=c_id, term_id=get_term).aggregate(avg=Avg("quran_total_score"),
                                                                                       max=Max("quran_total_score"),
                                                                                       min=Min("quran_total_score"))

        eng = 0
        count1 = 0
        for t in eng_scores:
            eng = t.eng_total_score
            count1 = 1


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

        email_id = request.POST.get('email_id')
        data_exists = CustomUser.objects.filter(email=email_id).exists()
        if data_exists:
            context = {"counts": counts, "student_list":student_list,
                       "total_score": total_score, "get_term":get_term,
                       "avg_score": avg_score, "dat": dat,
                       "remarks": remarks, "dat1": dat1, "dat2": dat2,
                       "dat3": dat3, "dat4": dat4, "dat5": dat5, "dat6": dat6,
                       "dat7": dat7, "dat8": dat8,
                       "termdetails": termdetails, "attendance": attendance,
                       "traits": traits, "broad":broad,
                       "student": student, "eng_scores": eng_scores,
                       "mth_scores": mth_scores, "sci_scores": sci_scores,
                       "nv_scores": nv_scores, "ict_scores": ict_scores,
                       "irs_scores": irs_scores, "quran_scores": quran_scores,
                       "crk_scores": crk_scores, "phe_scores": phe_scores}
            if get_term.term_name == "THIRD TERM":
                try:
                    return render(request, "parent_template/check_results3.html", context)
                except:
                    return HttpResponse("<h2>error 5050</h2>"
                                        " <h4>Teacher must enter complete student details before viewing will be available</h4>")
            else:
                try:
                    return render(request, "parent_template/check_results.html", context)
                except:
                    return HttpResponse("<h2>error 506</h2>"
                                        " <h4>Teacher must enter complete student details before viewing will be available</h4>")

    except:
        return HttpResponse("<h2>input error</h2>")


def parents_invoice_print(request, s_id, term_id):
    try:
        student = Student.objects.get(id=s_id)
        stud = Student.objects.filter(id=s_id)
        get_term = TermDetails.objects.get(id=term_id)

        c_id = student.classes_id.id
        remarks = TermRemarks.objects.filter(student_id=student, term_id=get_term)
        broad = BroadSheet.objects.filter(student_id=c_id)

        traits = TermTrait.objects.filter(student_id=student, term_id=get_term)

        attendance = Attendance.objects.filter(student_id=student, term_id=get_term)
        termdetails = TermDetails.objects.filter(id=term_id)

        eng_scores = EngScores.objects.filter(student_id=student, term_id=get_term)
        dat = EngScores.objects.filter(classes_id=c_id, term_id=get_term).aggregate(avg=Avg("eng_total_score"),
                                                                                    max=Max("eng_total_score"),
                                                                                    min=Min("eng_total_score"))
        mth_scores = MthScores.objects.filter(student_id=student, term_id=get_term)
        dat1 = MthScores.objects.filter(classes_id=c_id, term_id=get_term).aggregate(avg=Avg("mth_total_score"),
                                                                                     max=Max("mth_total_score"),
                                                                                     min=Min("mth_total_score"))
        nv_scores = NvScores.objects.filter(student_id=student, term_id=get_term)
        dat3 = NvScores.objects.filter(classes_id=c_id, term_id=get_term).aggregate(avg=Avg("nv_total_score"),
                                                                                    max=Max("nv_total_score"),
                                                                                    min=Min("nv_total_score"))
        ict_scores = IctScores.objects.filter(student_id=student, term_id=get_term)
        dat4 = IctScores.objects.filter(classes_id=c_id, term_id=get_term).aggregate(avg=Avg("ict_total_score"),
                                                                                     max=Max("ict_total_score"),
                                                                                     min=Min("ict_total_score"))
        phe_scores = PheScores.objects.filter(student_id=student, term_id=get_term)
        dat5 = PheScores.objects.filter(classes_id=c_id, term_id=get_term).aggregate(avg=Avg("phe_total_score"),
                                                                                     max=Max("phe_total_score"),
                                                                                     min=Min("phe_total_score"))
        sci_scores = SciScores.objects.filter(student_id=student, term_id=get_term)
        dat2 = SciScores.objects.filter(classes_id=c_id, term_id=get_term).aggregate(avg=Avg("sci_total_score"),
                                                                                     max=Max("sci_total_score"),
                                                                                     min=Min("sci_total_score"))
        irs_scores = IrsScores.objects.filter(student_id=student, term_id=get_term)
        dat6 = IrsScores.objects.filter(classes_id=c_id, term_id=get_term).aggregate(avg=Avg("irs_total_score"),
                                                                                     max=Max("irs_total_score"),
                                                                                     min=Min("irs_total_score"))
        crk_scores = CrkScores.objects.filter(student_id=student, term_id=get_term)
        dat7 = CrkScores.objects.filter(classes_id=c_id, term_id=get_term).aggregate(avg=Avg("crk_total_score"),
                                                                                     max=Max("crk_total_score"),
                                                                                     min=Min("crk_total_score"))
        quran_scores = QuranScores.objects.filter(student_id=student, term_id=get_term)
        dat8 = QuranScores.objects.filter(classes_id=c_id, term_id=get_term).aggregate(avg=Avg("quran_total_score"),
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

        email_id = request.POST.get('email_id')
        #get_email = CustomUser.objects.get(email=email_id)

        data_exists = Student.objects.filter(id=s_id).exists()
        if data_exists:

            context = {"counts": counts,
                       "total_score": total_score,
                       "avg_score": avg_score, "dat": dat,
                       "remarks": remarks, "dat1": dat1, "dat2": dat2,
                       "dat3": dat3, "dat4": dat4, "dat5": dat5, "dat6": dat6,
                       "dat7": dat7, "dat8": dat8,"stud":stud,
                       "termdetails": termdetails, "attendance": attendance,
                       "traits": traits, "broad":broad,
                       "student": student, "eng_scores": eng_scores,
                       "mth_scores": mth_scores, "sci_scores": sci_scores,
                       "nv_scores": nv_scores, "ict_scores": ict_scores,
                       "irs_scores": irs_scores, "quran_scores": quran_scores,
                       "crk_scores": crk_scores, "phe_scores": phe_scores}
            if get_term.term_name == "THIRD TERM":
                try:
                    return render(request, "parent_template/invoice-print3.html", context)
                except:
                    return HttpResponse("<h2>error 505</h2>"
                                       " <h4>Teacher must enter complete student details before viewing will be available</h4>")
            else:
                try:
                    return render(request, "parent_template/invoice-print.html", context)
                except:
                    return HttpResponse("<h2>error 505</h2>"
                                        " <h4>Teacher must enter complete student details before viewing will be available</h4>")

    except:
        return HttpResponse("<h2>input error</h2>")
