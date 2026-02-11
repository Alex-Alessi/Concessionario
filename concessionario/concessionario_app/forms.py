from django import forms
from .models import METODO_CHOICES, CATEGORIA_CHOICES, CONDIZIONI_CHOICES, ALIMENTAZIONE_CHOICES ,Auto, FotoAuto, RichiestaInfo
from django.forms import inlineformset_factory

class AcquistoForm(forms.Form):
    metodo_pagamento = forms.ChoiceField(choices=METODO_CHOICES)
    indirizzo_consegna = forms.CharField(max_length=100)

class AutoForm(forms.ModelForm):
    class Meta:
        model = Auto
        fields = '__all__'
        exclude = ['created_by', 'created_at']

class FiltriCatalogoForm(forms.Form):
    marca = forms.CharField(required=False, max_length=50, label="Cerca marca", widget=forms.TextInput(attrs={'placeholder': 'Inserisci la marca'}))
    categoria = forms.ChoiceField(required=False, choices=[('', 'Categoria')] + CATEGORIA_CHOICES, label="Categoria" )
    alimentazione = forms.ChoiceField(required=False, choices=[('', 'Alimentazione')] + ALIMENTAZIONE_CHOICES, label="Alimentazione" )
    condizioni = forms.ChoiceField(required=False, choices=[('', 'Condizione')] + CONDIZIONI_CHOICES, label="Condizione")
    prezzo_min = forms.IntegerField(required=False, label="Prezzo minimo", widget=forms.NumberInput(attrs={'placeholder': '€ min', 'min':'1'}))
    prezzo_max = forms.IntegerField(required=False, label="Prezzo massimo", widget=forms.NumberInput(attrs={'placeholder': '€ max'}))

    def clean(self):
        cleaned_data = super().clean()
        prezzo_min = cleaned_data.get("prezzo_min")
        prezzo_max = cleaned_data.get("prezzo_max")

        if prezzo_min is not None and prezzo_max is not None:
            if prezzo_max < prezzo_min:
                self.add_error("prezzo_max",
                    "Il prezzo massimo non può essere inferiore al prezzo minimo."
                )

        return cleaned_data

# GESTISCE PIU' OGGETTI FIGLI COLLEGATI AD UN OGGETTO PADRE
FotoAutoFormSet = inlineformset_factory(
    Auto,
    FotoAuto,
    fields=('foto', 'is_principale', 'ordine'),
    extra=5,
    can_delete=True
)

class RichiestaInfoForm(forms.ModelForm):
    class Meta:
        model = RichiestaInfo
        fields = ['nome', 'email', 'messaggio']
        widgets = {
            'messaggio': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Sono interessato a questa auto...'
            })
        }