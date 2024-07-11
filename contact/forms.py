from contact.models import Contact
from django import forms
from django.core.exceptions import ValidationError

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = 'first_name', 'last_name', 'phone', 'email', 'description', 'category',
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