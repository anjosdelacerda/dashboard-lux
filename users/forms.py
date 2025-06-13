from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model 

class UserRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "first_name", "email",)
    
    def save(self, commit=True):
        user = super().save(commit=False)
        
        user.is_staff = True
        user.is_superuser = True
        
        if not user.password:
            user.set_password(self.cleaned_data["password"])
            
        if commit:
            user.save()
           
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Nome de Usuário'
        self.fields['first_name'].label = 'Nome Completo'
        self.fields['email'].label = 'Email'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'vTextField'
            if isinstance(field.widget, forms.PasswordInput):
                field.widget.attrs['class'] = 'vPasswordField'