from .forms import ArticleForm
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic import TemplateView
# Create your views here.
from user.models import UserNormal
from .models import Article
from django.urls import reverse_lazy
from django.shortcuts import render,Http404
from django.contrib.auth.mixins import UserPassesTestMixin
from PIL import Image


class CreateArticle(CreateView):
    model = Article
    fields = ["title","image","content","tags"]
    template_name = "addArticle.html"

    def form_valid(self, form):
        form.instance.author =UserNormal.objects.get(username=self.request.user)
        return super().form_valid(form)


class UpdateArticle(UpdateView):
    model = Article
    fields = ["is_active","title", "image", "content", "tags"]
    template_name = "updateArticle.html"




class DeleteArticle(DeleteView):
    model = Article
    success_url= reverse_lazy("index")



class DetailArticle(TemplateView):

    template_name="article_detail.html"

    def get(self,request,id):
        return render(request,"article_detail.html",{'id':id})



class ListAllArticle(TemplateView):

    template_name="article_list.html"

