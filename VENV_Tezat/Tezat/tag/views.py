from django.shortcuts import get_object_or_404,render_to_response
from django.views.generic import TemplateView,CreateView
# Create your views here.
from .models import Tag
from user.models import UserNormal



class TagPage(TemplateView):

    template_name = "tag_page.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        tag=self.request.GET.get("tag")
        if tag:
            page_tag=get_object_or_404(Tag,name=tag)
            follower =get_object_or_404(UserNormal,username=self.request.user)
            is_follow=False
            if page_tag in follower.tags.all(): #takip ediyorsa
                is_follow=True
            context['tag']=tag
            context['is_follow']=is_follow
        return context


class AddTag(CreateView):
    model = Tag
    fields = "__all__"
    template_name = "addTag.html"

    def form_valid(self, form):
        name = form.instance.name
        if Tag.objects.filter(name__iexact=name):
            return render_to_response("tag_exist.html")
        return super().form_valid(form)
