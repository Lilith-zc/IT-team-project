
from django import forms
from django.forms import fields, models
from django.template.defaultfilters import title
from rango.models import Book, Category, UserProfile
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=Category.NAME_MAX_LENGTH, help_text="Please enter the category name")
    views = forms.IntegerField(widget=forms.HiddenInput(),initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(),initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(),required=False)

    class Meta:
        model = Category
        fields = ('name',)

class BookForm(forms.ModelForm):
    title = forms.CharField(max_length=Book.TITLE_MAX_LENGTH, help_text="Please enter the title of the Book")
    url = forms.URLField(max_length=Book.URL_MAX_LENGTH, help_text="Please enter the URL of the Book.")
    view = forms.IntegerField(widget=forms.HiddenInput(),initial=0)

    class Meta:
        model = Book
        exclude = ('category','views')
    
    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url
        return cleaned_data
    
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ('picture',)