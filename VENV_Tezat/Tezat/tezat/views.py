from django.shortcuts import render
from django.views.generic import TemplateView

def index(request):
    return render(request,"base.html")

class Timeline(TemplateView):

    template_name="timeline.html"



