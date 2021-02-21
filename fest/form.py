from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Users, Crew


DISPLAY_FONT = {
    ('horror', 'horror'),
    ('mono-spaced', 'mono-spaced'),
    ('sans-serif', 'sans-serif'),
    ('fantacy', 'fantacy'),
    ('etc...', 'etc...'),
}

class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', ]


class DashboardForm(forms.ModelForm):
    username = forms.CharField(label='name')
    email = forms.EmailField(label='email')
    avatar_img = forms.ImageField(label='avatar img')
    about = forms.CharField(label='about me')
    netnet = forms.CharField(label='profile link')
    affiliation = forms.CharField(label='school, house or crew')


    class Meta:
        model = Users
        fields = ['username', 'email', 'avatar_img', 'about', 'affiliation', 'netnet', 
                   ]

class DashboardCrewForm(forms.ModelForm):
    crew_name = forms.CharField(label='Crew name')
    tag_line = forms.CharField(label='tag line')
    profile_link = forms.CharField(label='profile link')
    display_font = forms.CharField(label='display font', widget=forms.Select(choices=DISPLAY_FONT))


    class Meta:
        model = Crew
        fields = ['crew_name', 'display_font', 'tag_line', 'profile_link',
                   ]

class UpdateProfile(forms.ModelForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
        return email

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user