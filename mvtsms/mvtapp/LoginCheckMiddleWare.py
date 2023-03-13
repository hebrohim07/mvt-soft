from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginCheckMiddleWare(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        print(modulename)
        user = request.user
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "mvtapp.adminviews":
                    pass
                elif modulename == "mvtapp.views" or modulename == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("admin_home"))
            elif user.user_type == "2":
                if modulename == "mvtapp.staffviews":
                    pass
                elif modulename == "mvtapp.views" or modulename == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("staffhome"))
            elif user.user_type == "3":
                if modulename == "mvtapp.studentviews":
                    pass
                elif modulename == "mvtapp.views" or modulename == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("studenthome"))
            elif user.user_type == "4":
                if modulename == "mvtapp.parentviews":
                    pass
                elif modulename == "mvtapp.views"or modulename == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("parenthome"))
            elif user.user_type == "5":
                if modulename == "mvtapp.accountantviews":
                    pass
                elif modulename == "mvtapp.views" or modulename == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("accountanthome"))
            else:
                return HttpResponseRedirect(reverse("loginpage"))

        else:
            if request.path == reverse("loginpage") or request.path == reverse("dologin") or modulename == "django.contrib.auth.views":
                pass
            else:
                return HttpResponseRedirect(reverse("loginpage"))