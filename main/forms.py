from django_summernote import fields as summer_fields
from  service.models import Inquiry
from django import forms

class PostForm(forms.ModelForm):
    fields = summer_fields.SummernoteTextFormField(error_messages={'required': (u'데이터를 입력해주세요'), })
    class Meta:
        model = Inquiry
        fields = ('fields',)