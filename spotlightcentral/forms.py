from django import forms

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, label='Your Name')
    email = forms.EmailField(label='Your Email')
    to = forms.EmailField(label='Recipient Email')
    comments = forms.CharField(required=False, widget=forms.Textarea, label='Comments')
