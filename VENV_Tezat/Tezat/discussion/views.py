from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
# Create your views here.
from .models import Discussion
from user.models import UserNormal

def deneme(request):
    return render(request,"commenttest.html")





class DetailDiscussion(TemplateView):

    template_name="discussion_detail.html"

    def get(self,request,id):
        return render(request,"discussion_detail.html",{'id':id})

class ListAllDiscussions(TemplateView):

    template_name="discussion_list.html"



class AddDiscussion(CreateView):

    model = Discussion
    fields = ["text","image","video_url","tags"]
    template_name = "discussion_add.html"

    def form_valid(self, form):
        form.instance.author =UserNormal.objects.get(username=self.request.user)
        return super().form_valid(form)
