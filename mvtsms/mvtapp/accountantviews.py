from django.shortcuts import render


def accountanthome(request):
    return render(request, "accountant_template/home_content.html")
