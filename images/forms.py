from django import forms


class CreateImageForm(forms.Form):
    #image_name = forms.CharField()
    image_proj = forms.CharField(required=True)
    repo_path = forms.CharField(required=True)
    image_desc = forms.CharField(required=False)
