from django import forms
from .models import Account,UserProfile
from django.forms import fields



class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : "Enter Password"
    }))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Password'

    }))
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']
#css
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder']='Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder']='Enter Last Name'
        self.fields['email'].widget.attrs['placeholder']='Enter Your Email'
        self.fields['phone_number'].widget.attrs['placeholder']='Enter Phone Number'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    #password confirmation
    def clean(self):
        cleaned_data=super(UserRegistrationForm,self).clean()
        password=cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')

        if password !=confirm_password:
            raise forms.ValidationError(
                'password doesnot match!'
            )
        
#create Profile
class CreateProfileForm(forms.ModelForm):
    profile_picture=forms.ImageField(required=False,error_messages={'invalid':("image files only")},widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields=('address_line_1','address_line_2','city','state','country','profile_picture')



#Edit Profile
class UserForm(forms.ModelForm):
    class Meta:
        model =Account
        fields=('first_name','last_name','phone_number')
        #if we dont use css we can use it form any forms to style properly
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class UserProfileForm(forms.ModelForm):
    profile_picture=forms.ImageField(required=False,error_messages={'invalid':("image files only")},widget=forms.FileInput)
    class Meta:
        model=UserProfile
        fields=('address_line_1','address_line_2','city','state','country','profile_picture')
        #if we dont use css we can use it form any forms to style properly
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

