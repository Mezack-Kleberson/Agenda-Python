from contact.models import Contact
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation

class ContactForm(forms.ModelForm):
    picture = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*',
            }
        )
    )

    class Meta:
        model = Contact
        fields = 'first_name', 'last_name', 'phone', 'email', 'description', 'category', 'picture',
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Ensira o texto aqui.'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Ensira o texto aqui.'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Ensira o número aqui.'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Ensira o email aqui.'}),
            'description': forms.Textarea(attrs={'placeholder': 'Ensira a descrição aqui.'}),
        }
        help_texts  = {
            'first_name': ('Ajuda'),
        }

    def clean(self):
        cleaned_data = self.cleaned_data
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if first_name == last_name:
            msg = ValidationError(
                'Primeiro nome não pode ser igual ao segundo',
                code='invalid'
            )

            self.add_error('first_name', msg)
            self.add_error('last_name', msg)

        return super().clean()
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')

        if first_name == 'ABC':
            self.add_error(
                'first_name',
                ValidationError(
                    'veio do error',
                    code='invalid'
                ),   
            )

        return first_name

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(
        required=True,
        error_messages={
            'required': 'Campo obrigatório'
        }
    )
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email',
            'username', 'password1', 'password2',
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                ValidationError('Já existe este e-mail', code='invalid')
            )
        return email

class RegisterUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        label="Primeiro nome",
        min_length=2,
        max_length=30,
        required=True,
        error_messages={
            'min_length': 'O nome precisa conter mais de duas letrar'
        }
    )
    last_name = forms.CharField(
        label="Segundo nome",
        min_length=2,
        max_length=30,
        required=True,
        error_messages={
            'min_length': 'O nome precisa conter mais de duas letrar'
        }
    )
    email = forms.EmailField(required=True)

    password1 = forms.CharField(
        label="Senha",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-passaword"}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )

    password2 = forms.CharField(
        label="Confirmar senha",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-passaword"}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email',
            'username', 
        )
    
    def save(self, commit=True):
        password = self.cleaned_data.get('password1')
        user = super().save(commit=False)

        if password:
            user.set_password(password)
        if commit:
            user.save()
        
        return user

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                self.add_error(
                    'password2',
                    ValidationError('Senhas não batem')
                )

        return super().clean()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.email

        if current_email != email:
            if User.objects.filter(email=email).exists():
                self.add_error(
                    'email',
                    ValidationError('Já existe este e-mail', code='invalid')
                )
        return email
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if password1:
            try: 
                password_validation.validate_password(password1)
            except ValidationError as errors:
                self.add_error(
                    'password1',
                    ValidationError(errors)
                    )

        return password1