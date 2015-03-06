from django import forms


class CreateImageForm(forms.Form):
    #image_name = forms.CharField()
    project_id = forms.CharField(required=True)
    repos_id = forms.CharField(required=True)
    repo_branch = forms.CharField(required=True)
    image_desc = forms.CharField(required=False)
