from django.shortcuts import render,Http404,HttpResponse,redirect,get_object_or_404
from django.contrib import messages
from .forms import *
from .models import UserNormal
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes,force_text
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from .tokens import account_activation_token
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from .models import UserStatistics


def loginprocess(request):
        next=request.GET.get('next')
        form=LoginForm(request.POST or None)
        context={
            'title':'Giriş Yap',
            'form':form
        }
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user =authenticate(username=username,password=password)
            if user is None:#Kullanıcı var mı ve bilgileri doğru mu?
                messages.info(request,"Kullanıcı adı ya da şifre hatalı")
                return render(request,"login.html",context)
            else:#kullanıcı varsa giriş yap
                if user.is_active:
                    messages.info(request,"Giriş işlemi başarılı")
                    login(request,user)
              #      send_mail("Giriş Yapıldı","Tezat.net web sayfasına giriş işlemi gerçekleştirildi","umt9735@gmail.com",['umt9735@gmail.com'])
                    if next:
                        return redirect(next)
                    else:
                        return redirect("index")
                else:
                    messages.error(request,u"Üyeliğiniz aktif değil,lütfen mail adresinize gelen bağlantıya tıklayarak üyeliğinizi aktifleştiriniz!")
        else:
            return render(request,"login.html",context)



def logoutprocess(request):
    logout(request)
    return redirect("index")


class Registration(FormView):
    template_name = 'register.html'
    form_class    = UserRegisterForm
    success_url = 'login'

    def form_valid(self, form):
        user = UserNormal()
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.username = form.cleaned_data['username']
        user.email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.photo = form.cleaned_data['photo']
        user.about = form.cleaned_data['about']
        user.is_active = False
        # user.birthday='00-00-0000'
        current_site = get_current_site(self.request)
        user.save()
        mail_subject = u'Hesabınızı aktifleştirin'
        message = render_to_string('user_activate_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
     #   email = EmailMessage(mail_subject, message, to=[user.email])
     #   email.send()
     #   messages.success(self.request,"Kayıt işlemi başarılı,lütfen emailinize gelen bağlantı ile hesabınızı aktifleştiriniz!")
        return super().form_valid(form)

"""
def register(request):
    if request.POST:
        form= UserRegisterForm(request.POST,request.FILES or None)
        if form.is_valid():
            user=UserNormal()
            user.first_name=form.cleaned_data['first_name']
            user.last_name=form.cleaned_data['last_name']
            user.username=form.cleaned_data['username']
            user.email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            user.set_password(password)
            user.photo=form.cleaned_data['photo']
            user.about=form.cleaned_data['about']
            user.is_active=False
            #user.birthday='00-00-0000'
            current_site=get_current_site(request)
            user.save()
            mail_subject = u'Hesabınızı aktifleştirin'
            message = render_to_string('user_activate_email.html',{
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            email= EmailMessage(mail_subject,message,to=[user.email])
            email.send()

            context={'title':'Kayıt Ol',
                     'form':form
                     }
            messages.success(request,"Kayıt işlemi başarılı,lütfen emailinize gelen bağlantı ile hesabınızı aktifleştiriniz!")
            return render(request,"register.html",context)
        else:
            context = {
                'title': 'Kayıt Ol',
                'form': form
            }
            return render(request, "register.html", context)
    else:
        form=UserRegisterForm(request.FILES or None)
        context={
            'title':'Kayıt',
            'form':form
        }
        return render(request,"register.html",context)


@login_required()
def girisTest(request):
    return render_to_response("girisyapildi.html")
"""


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # return redirect('home')
        return HttpResponse('Üyelik aktifleştirm işlemi başarılı')
    else:
        return HttpResponse('Geçersiz aktivayon linki')



class Profile(TemplateView):
    # I used TemplateView instead of ListView because If I use ListView Context contain object_List and articles
    # but it is both the same  and I need to request.username for Article's author

    template_name= "user_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = UserNormal.objects.get(username=self.request.user)
        context['user_articles'] = user.articles.all().order_by("-created_date")
        context['user_article_count'] = user.articles.count()
        context['user_discuss_count'] = user.discussions.count()
        context['user_follower_count'] = 0 # add later
        context['user_follow_count'] = 0 # add later
        context['header_text']= user.about
        return context


class UserPage(TemplateView):

    template_name = "user_page.html"



    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        username=self.request.GET.get("user")
        if username:
            page_user=get_object_or_404(UserNormal,username=username)
            follower =get_object_or_404(UserNormal,username=self.request.user)
            is_follow=False
            if page_user in follower.following.all():
                is_follow=True
            context['username']=username
            context['is_follow']=is_follow
        return context




