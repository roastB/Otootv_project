from django.utils import translation
from django.shortcuts import render
from notice.models import Notice
from django.views.generic import ListView


def main(request):
    if translation.LANGUAGE_SESSION_KEY in request.session:
        del request.session[translation.LANGUAGE_SESSION_KEY]

    userLanguage = 'en'
    translation.activate(userLanguage)
    request.session[translation.LANGUAGE_SESSION_KEY] = userLanguage
    context ={}
    return render(request,'main.html', context)


class noticeview(ListView):
    model = Notice
