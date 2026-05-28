from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from .models import StudentProfile, User


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        # """ this is the meta class of the entrepriseUserCreationform
        # whihc specifies the models and fieldsin the  form
        # it also defines coustom widgets for eaach field, like in a kind of template
        # """
        fields = {
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "role",
            "is_verified",
        }
        widgets = {
            "username": forms.TextInput(attrs={'class': 'form-control'}),
            "email": forms.EmailInput(attrs={'class': 'form-control'}),
            "first_name": forms.TextInput(attrs={'class': 'form-control'}),
            "last_name": forms.TextInput(attrs={'class': 'form-control'}),
            "phone_number": forms.TextInput(attrs={'class': 'form-control'}),
            "role": forms.Select(attrs={'class': 'form-control'}),
            "is_verified": forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class StudentCreateForm(UserCreationForm):
    roll_number = forms.CharField(max_length=30)
    course = forms.CharField(max_length=100)
    semester = forms.CharField(min_value=1, max_length=20)
    skills = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control'}), required=False)
    bio = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = User
        fields = {
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            'profile_picture',
            "password1",
            "password2",
            "roll_number",
            "course",
            "semester",
            "skills",
            "bio",

        }
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Roles.STUDENT
        if commit:
            user.save()
            StudentProfile.objects.create(
                user=user,
                roll_number=self.cleaned_data['roll_number'],
                course=self.cleaned_data['course'],
                semester=self.cleaned_data['semester'],
                skills=self.cleaned_data['skills'],
                bio=self.cleaned_data['bio']
            )
        return user

class StudentUserUpdateForm(UserChangeForm):

    class Meta:
        model = StudentProfile
        fields=(
            "roll_number",
            "course",
            "semester", 
            "skills",
            "bio",)
        widgets = {
            "skills": forms.Textarea(attrs={'class': 'form-control'}),
            "bio": forms.Textarea(attrs={'class': 'form-control'}),
        }