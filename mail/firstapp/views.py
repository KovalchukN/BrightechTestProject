from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from django.core.mail import send_mail
from .forms import MailForm

def index(request):

    userform = MailForm(request.POST)
    if userform.is_valid():
        mail_to = request.POST.get('mail_to').split(", ")
        subject = userform.cleaned_data['subject']
        content = userform.cleaned_data['content']
        if send_mail(subject, content, "Python script", mail_to , fail_silently=True):
            return redirect('index')
    else:
        userform = MailForm()

    return render(request, 'index.html', {"form": userform})
