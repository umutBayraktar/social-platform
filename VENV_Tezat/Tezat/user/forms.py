from django.forms import ModelForm
from .models import UserNormal
from django import forms
from django.contrib.auth.models import User
from nocaptcha_recaptcha.fields import NoReCaptchaField
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(forms.Form):
    first_name = forms.CharField(max_length=50,label="İsim:")
    last_name  = forms.CharField(max_length=50,label="Soyisim:")
    username   = forms.CharField(label="Kullanıcı Adı:")
    email      = forms.EmailField(label="Email")
    password   = forms.CharField(label="Şifre",widget=forms.PasswordInput,required=False)
    confirm    = forms.CharField(label="Şifre Tekrar",widget=forms.PasswordInput,required=False)
    photo      = forms.ImageField(label="Profil Fotoğrafı",required=False)
    about      = forms.CharField(label="Hakkımda",widget=forms.Textarea,required=False)
   # captcha    = NoReCaptchaField(label="")

    def clean(self):
        #first_name validation
        name=self.cleaned_data['first_name']
        if not name:
            raise forms.ValidationError("İsim boş geçilemez")
        if len(name)>50:
            raise forms.ValidationError("Çok uzun isim girişi")


        # last_name validation
        surname=self.cleaned_data['last_name']
        if not surname:
            raise forms.ValidationError("Soyisim boş geçilemez")
        if len(surname)>50:
            raise forms.ValidationError("Çok uzun soyisim girişi")


        #username validation
        username=self.cleaned_data['username']
        if not username:
            raise forms.ValidationError("Kullanıcı adı boş geçilemez")

        if User.objects.filter(username__iexact=username):
            raise forms.ValidationError("Bu kullanıcı adı başka bir kullanıcı tarafından kullanılmakta")

        #email validation
        email=self.cleaned_data['email']
        if not email:
            raise forms.ValidationError("E mail boş geçilemez")
        # mail test için yoruma aldım yorum satırını kaldır
        if User.objects.filter(email__iexact=email):
            raise forms.ValidationError("Girilen e-posta adresi başka bir kullanıcı tarafından kullanılmakta")

        #password validation

        password = self.cleaned_data['password']
        confirm = self.cleaned_data['confirm']

        if (not password) or password == "": #herhengi biri girilmezse 0 olacak not olunca doğru olacak
            raise forms.ValidationError('Şifre alanları boş geçilemez')
        if (not confirm) or confirm == "":
            raise forms.ValidationError("Şifre alanları boş geçilemez")
        if password != confirm:
            raise forms.ValidationError('Şifreler uyuşmuyor')

        #photo validation
        photo=self.cleaned_data['photo']

        #about validation
        about=self.cleaned_data['about']

        values={
            'first_name':name,
            'last_name':surname,
            'username':username,
            'email':email,
            'password':password,
            'photo':photo,
            'about':about,
        }
        return values




class LoginForm(forms.Form):
    username = forms.CharField(label="Kullanıcı Adı:")
    password = forms.CharField(label="Şifre", widget=forms.PasswordInput, required=False)

