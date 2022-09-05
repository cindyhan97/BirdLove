from distutils.command.clean import clean
from tkinter import Widget
from django import forms
from .models import *
from django.contrib.auth.forms import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from django.utils.safestring import mark_safe
from image_uploader_widget.widgets import ImageUploaderWidget


class userAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('userame', 'password')

class userRealNameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'email')
    def __init__(self,*args, **kwargs ):
        super(userRealNameForm,self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout =Layout(
            Row(
                Column('last_name'),
                Column('first_name'),
                css_class='form-row'
            ),
            'email'
    )

class donationForm(forms.ModelForm):
    class Meta:
        model = userDonationRecord
        fields = ('amount', )


class username_update(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'password')

class userPasswordChanging(PasswordChangeForm):
    class Meta:
        model = User
        fields = ('password')

class addressForm(forms.ModelForm):
    class Meta:
        model = address
        fields = '__all__'
    def __init__(self,*args, **kwargs ):
        super(addressForm,self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)    
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'phoneNumber',
            Row(
                Column('postalCode', css_class='form-group '),
                Column('area', css_class='form-group'),
                css_class='form-row'
            ),
            'address1',
            'address2'
        )
class userprofileForm(forms.ModelForm):
    class Meta:
        model = userprofile
        fields = ('nickname', 'avatar')
    def __init__(self,*args, **kwargs ):
        super(userprofileForm,self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout =Layout(
            'avatar',
            'nickname',
    )


class userCreate(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email', 'first_name', 'last_name','password1', 'password2')

class userRegis(forms.ModelForm):
    username = models.CharField(max_length=100)
    password=forms.CharField(widget=forms.PasswordInput())
    confirm_Your_Password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=User
        fields=('username','email', 'first_name', 'last_name','password')

    def clean(self):
        cleaned_data = super(userRegis, self).clean()
        password = cleaned_data.get("password")
        confirm_Your_Password = cleaned_data.get("confirm_Your_Password")
        username_check = cleaned_data.get("username")
        if password and confirm_Your_Password and username_check:
            username_filter = User.objects.filter(username = username_check).first() 
            if password != confirm_Your_Password:
                print("password not the same")
                self.add_error('confirm_Your_Password', 'Please enter the same password')
            if username_filter:
                self.add_error('username', 'The username has been used.')
        return cleaned_data

class anoUserInfoForm(forms.ModelForm):
    class Meta:
        model = anonymousProfile
        fields = ('nickname',)
    def __init__(self, *args, **kwargs):
        super(anoUserInfoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('nickname', css_class='form-group col-md-2'),
                css_class='row'
            )
        )

class rescueRequestForm(forms.ModelForm):
    class Meta:
        model = rescueRequest
        fields = ('resuceDescription',)
    def __init__(self, *args, **kwargs):
        super(rescueRequestForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

class rescueBirdPictureForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(rescueBirdPictureForm, self).__init__(*args, **kwargs)
        self.fields['pict'].label = False
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        
    class Meta:
        model = rescueBirdPicture
        fields = ('pict',)

class anonymousRequestForm(forms.ModelForm):
    class Meta:
        model = anonymousRequest
        fields = ('resuceDescription',)
    def __init__(self, *args, **kwargs):
        super(anonymousRequestForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.form_tag = False

class birdForm(forms.ModelForm):
    class Meta:
        model = bird
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(birdForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('name'),
            ),
            Row(
                Column('species', css_class='form-group'),
                Column('age', css_class='form-group'),
                css_class='row'
            ),
            Row(
                Column('adoptDescription'),
            )
        )