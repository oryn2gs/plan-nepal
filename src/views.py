from django.shortcuts import render

def custom_404(request, exception):
    return render(request, "main/404.html", status=404)