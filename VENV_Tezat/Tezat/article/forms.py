from django import forms
from .models import Article
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget

class ArticleForm(forms.Form):

    title=forms.CharField(label="Başlık",max_length=200)
    image=forms.ImageField(label="Yazı Resmi",required=False)
    content=forms.CharField(label="İçerik",widget=CKEditorWidget())
    tags=forms.CharField(label="Etiketler",widget=forms.Textarea,required=False)

    def clean_title(self):
        title=self.cleaned_data['title']
        if title is None:
            raise forms.ValidationError('Başlık alanı boş geçilemez!')
        if len(title)>200:
            raise  forms.ValidationError('Başlık maksimum 200 karakter olabilir!')
        return title

    def clean_content(self):
        content=self.cleaned_data['content']
        if content is None:
            raise forms.ValidationError('İçerik alanı boş geçilemez!')

        return content



