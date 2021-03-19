from django import forms

class MailForm(forms.Form):

    mail_to = forms.CharField(label="E-mail",help_text='Use ", " to input more than 1 email', widget=forms.TextInput(attrs={"class": "form-control"}))
    subject = forms.CharField(label="Тема", widget=forms.TextInput(attrs={"class": "form-control"}))
    content = forms.CharField(label="Текст", widget=forms.Textarea(attrs={"class": "form-control", "rows": 5}))