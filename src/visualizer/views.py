from django.shortcuts import render


def index(request):
    return render(request, "visualizer/index.html")


def visview(request, username):
    context = {'username': username}
    return render(request, "visualizer/vis.html", context)
