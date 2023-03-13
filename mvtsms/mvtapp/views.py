from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from mvtapp.EmailBackEnd import EmailBackEnd


# Create your views here.
def showdash(request):
    return render(request, "dash.html")

def showlogin(request):
    return render(request, "login.html")

def dologin(request):
    if request.method!='POST':
        return HttpResponse("<h1>not allowed</h1>")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get("email"), password=request.POST.get("password"))
        if user != None:
            login(request, user)
            if user.user_type == "1":
                return HttpResponseRedirect("/home")
            elif user.user_type == "2":
                return HttpResponseRedirect("/staffhome")
            elif user.user_type == "3":
                return HttpResponseRedirect("/studenthome")
            elif user.user_type == "4":
                return HttpResponseRedirect("/parenthome")
            elif user.user_type == "5":
                return HttpResponseRedirect("/accountanthome")
        else:
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect("/")


def getuserdetails(request):
    if request.user != None:
        return HttpResponse("User : " + request.user.email + "usertype : " + request.user.user_type)
    else:
        return HttpResponse("Please login First")


def logoutuser(request):
    logout(request)
    return HttpResponseRedirect("/")
