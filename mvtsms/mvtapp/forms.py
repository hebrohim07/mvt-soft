from django import forms
#from django.forms import DateInput

from mvtapp.models import Classes, SessionYearModel

class DateInput(forms.DateInput):
    input_type = "date"


class AddStudentForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    password = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="Address",  max_length=500, widget=forms.TextInput(attrs={"class":"form-control"}))
    adm_date = forms.DateField(label="Adm_date", widget=DateInput(attrs={"class":"form-control"}))
    date_of_birth = forms.DateField(label="Date Of Birth", widget=DateInput(attrs={"class":"form-control"}))
    age = forms.CharField(label="Age", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))

    clas_list = []
    try:
        classes = Classes.objects.all()
        for clas in classes:
            single_clas = (clas.id, clas.classes_name)
            clas_list.append(single_clas)
    except:
        clas_list = []

    session_list = []
    #try:
    sessions = SessionYearModel.object.all()
    for ses in sessions:
        single_ses = (ses.id, str(ses.session_start_year)+"-"+str(ses.session_end_year))
        session_list.append(single_ses)


    gender_choices = (
        ("Male", "Male"),
        ("Female", "Female")
    )
    clas = forms.ChoiceField(label="Classes", choices=clas_list, widget=forms.Select(attrs={"class": "form-control"}))
    gender = forms.ChoiceField(label="Gender", choices=gender_choices, widget=forms.Select(attrs={"class": "form-control"}))
    session_year_id = forms.ChoiceField(label="Session Year", widget=forms.Select(attrs={"class": "form-control"}), choices=session_list,)
    profile_pic = forms.FileField(label="Profile pic", widget=forms.FileInput(attrs={"class": "form-control"}))


class EditStudentForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Address", max_length=500, widget=forms.TextInput(attrs={"class": "form-control"}))
    adm_date = forms.DateField(label="Adm_date", widget=DateInput(attrs={"class": "form-control"}))
    date_of_birth = forms.DateField(label="Date Of Birth", widget=DateInput(attrs={"class": "form-control"}))
    age = forms.CharField(label="Age", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))

    clas_list = []
    try:
        classes = Classes.objects.all()
        for clas in classes:
            single_clas = (clas.id, clas.classes_name)
            clas_list.append(single_clas)
    except:
        pass

    session_list = []
    # try:
    sessions = SessionYearModel.object.all()
    for ses in sessions:
        single_ses = (ses.id, str(ses.session_start_year) + "-" + str(ses.session_end_year))
        session_list.append(single_ses)

    gender_choices = (
        ("Male", "Male"),
        ("Female", "Female")
    )
    clas = forms.ChoiceField(label="Classes", choices=clas_list, widget=forms.Select(attrs={"class": "form-control"}))
    gender = forms.ChoiceField(label="Gender", choices=gender_choices, widget=forms.Select(attrs={"class": "form-control"}))
    session_year_id = forms.ChoiceField(label="Session Year", widget=forms.Select(attrs={"class": "form-control"}), choices=session_list)
    profile_pic = forms.FileField(label="Profile pic", widget=forms.FileInput(attrs={"class": "form-control"}))



