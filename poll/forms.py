from django.contrib.auth.models import User
from django import forms
from .models import UserExtraDetails, OrganizationTable

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

class UserOrganizationForm(forms.ModelForm):
	organizationName = forms.ModelChoiceField(queryset=OrganizationTable.objects.all().values('organizationName'))

	class Meta:
		model = UserExtraDetails
		fields = ('organizationName',)	        