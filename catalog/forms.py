from django import forms
from django.forms import BooleanField

from blog.models import Articles
from catalog.models import Product, Version


class StileFormMixin():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StileFormMixin, forms.ModelForm):
    bad_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

    class Meta:
        model = Product
        fields = ('name', 'description', 'category', 'price', 'photo',)

    def clean_name(self):
        cleaned_data = self.cleaned_data['name']

        for word in self.bad_words:

            if word in cleaned_data.lower():
                raise forms.ValidationError(f'Слов {self.bad_words} не должно быть в названии продукта')

        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data['description']

        for word in self.bad_words:

            if word in cleaned_data.lower():
                raise forms.ValidationError(f'Слов {self.bad_words} не должно быть в названии продукта')

        return cleaned_data


class ProductModeratorForm(StileFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ('description', 'category')



class VersionForm(StileFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'
