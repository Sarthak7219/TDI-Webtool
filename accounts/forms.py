from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.contrib.auth.forms import UserChangeForm

class ProfileCreationForm(UserCreationForm):
    phone_number = forms.IntegerField(required=True)
    email = forms.EmailField(required=True)
    profile_pic = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2', 'profile_pic']

    def save(self, commit=True):
        profile = super().save(commit=False)

        # Handle the profile picture
        if 'profile_pic' in self.cleaned_data:
            profile.profile_pic = self.cleaned_data['profile_pic']

        if commit:
            profile.save()

        return profile
    

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'profile_pic']

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        # Pre-fill the form with the current data from the instance
        if self.instance:
            self.initial['first_name'] = self.instance.first_name
            self.initial['last_name'] = self.instance.last_name
            self.initial['email'] = self.instance.email
            self.initial['phone_number'] = self.instance.phone_number