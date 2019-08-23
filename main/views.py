from django.utils import translation
from django.shortcuts import render
from notice.models import Notice
from django.views.generic import ListView
from django.views.generic.base import TemplateView


def transferview1(request):
    if translation.LANGUAGE_SESSION_KEY in request.session:
        del request.session[translation.LANGUAGE_SESSION_KEY]

    userLanguage = 'en'
    translation.activate(userLanguage)
    request.session[translation.LANGUAGE_SESSION_KEY] = userLanguage
    context ={}
    return render(request,'transfer.html', context)


class transferview2(ListView):
    model = Notice

class mainView(TemplateView):
    template_name = 'main.html'

class creatorView(TemplateView):
    template_name = 'creator.html'

class channelView(TemplateView):
    template_name = 'channel.html'

class videoView(TemplateView):
    template_name = 'video.html'