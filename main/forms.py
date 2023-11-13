from django import forms
from .models import UploadImg
from django.utils import timezone


#class UploadImgForm(forms.ModelForm):
#    class Meta:
#        model = UploadImg
#        fields = ['upload_datetime', 'patient_name', 'page', 'pics']

class UploadImgForm(forms.Form):
    upload_datetime = forms.DateTimeField(required=False)
    patient_id = forms.IntegerField(null=False)
    patient_name = forms.CharField()
    page = forms.IntegerField()
    pics = forms.ImageField(required=True)
