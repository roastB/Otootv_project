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





class main_logo_pageView(TemplateView):
    template_name = 'main_logo_page.html'
class signup_1View(TemplateView):
    template_name = 'signup_1.html'
class signup_2View(TemplateView):
    template_name = 'signup_2.html'
class login_1View(TemplateView):
    template_name = 'login_1.html'
class login_2View(TemplateView):
    template_name = 'login_2.html'
class subscribe_1View(TemplateView):
    template_name = 'subscribe_1.html'
class subscribe_2View(TemplateView):
    template_name = 'subscribe_2.html'
class subscribe_3View(TemplateView):
    template_name = 'subscribe_3.html'

class mainView(TemplateView):
    template_name = 'main.html'

class creatorView(TemplateView):
    template_name = 'creator.html'

class channelView(TemplateView):
    template_name = 'channel.html'

class videoView(TemplateView):
    template_name = 'video.html'

class noticeView(TemplateView):
    template_name = 'notice.html'

class helpView(TemplateView):
    template_name = 'help.html'

class accountView(TemplateView):
    template_name = 'account.html'

from main.forms import PostForm
def inquiry_newView(request):
    form = PostForm()
    return render(request, 'inquiry_new.html', {'form': form})

class inquiryView(TemplateView):
    template_name = 'inquiry.html'

class inquiry_detailView(TemplateView):
    template_name = 'inquiry_detail.html'
