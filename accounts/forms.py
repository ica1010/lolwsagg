from django import forms
from .models import Account, UserProfile

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={        
        'placeholder':'Enter Password',
        'class': 'form-control',}
    ))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={ 'placeholder':'Enter Password',}
    ))
    
    class Meta:
        model = Account
        fields = ["first_name","last_name","email","phone_number","password"]

    def __init__(self, *args, **kwargs):
        super(RegistrationForm , self).__init__( *args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder']='Enter your first name'
        self.fields['last_name'].widget.attrs['placeholder']='Enter your last name'
        self.fields['phone_number'].widget.attrs['placeholder']='Enter your phone number'
        self.fields['email'].widget.attrs['placeholder']='Enter your Email Address'
        for field in self.fields:
             self.fields[field].widget.attrs['class']='p-2' 
             self.fields[field].widget.attrs['style']='  width: 100%; height: 40px; border-radius: 5px; border-color: #00000000;'     
    def clean(self):
        cleaned_data= super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password= cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError(
                'Password does not the same'
            )


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
             self.fields[field].widget.attrs['class']='p-2' 
             self.fields[field].widget.attrs['style']='  width: 100%; height: 40px; border-radius: 5px; border-color: #00000000;'     
class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ('address_line_1', 'address_line_2', 'city', 'state', 'country', 'profile_picture')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
           self.fields[field].widget.attrs['class']='p-2' 
           self.fields[field].widget.attrs['style']='  width: 100%; height: 40px; border-radius: 5px; border-color: #00000000;'    