from django.core.paginator import Paginator
from django.core.signing import BadSignature

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q

from django.urls import reverse_lazy
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, CreateView

from .forms import ChangeUserInfoForm, RegisterUserForm, SearchForm
from .models import AdvUser, SubRubric, Ads
from .utilities import signer


# Create your views here.
class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'main/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('main:profile')
    success_message = 'User data changed'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class BBLoginView(LoginView):
    template_name = 'main/login.html'


class BBPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('main:profile')
    success_message = 'User password changed'


class BBPasswordResetView(SuccessMessageMixin, PasswordResetView):
    template_name = 'main/password_reset.html'
    success_url = reverse_lazy('main:password_reset_done')
    success_message = 'Reset link sent to your email'


class BBPasswordResetDoneView(TemplateView):
    template_name = 'main/password_reset_done.html'


class BBLogoutView(LoginRequiredMixin, LoginView):
    template_name = 'main/logout.html'


class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'main/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('main:register_done')


class RegisterDoneView(TemplateView):
    template_name = 'main/register_done.html'


@login_required
def profile(request):
    return render(request, 'main/profile.html')


def index(request):
    ads = Ads.objects.filter(is_active=True)[:10]
    context = {'ads': ads}
    return render(request, 'main/index.html', context)


def other_page(request, page):
    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/bad_signature.html')
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = 'main/user_is_activated.html'
    else:
        template = 'main/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)


def by_rubric(request, pk):
    rubric = get_object_or_404(SubRubric, pk=pk)
    bbs = Ads.objects.filter(is_active=True, rubric=pk)
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q = Q(title_icontains=keyword) | Q(content_icontains=keyword)
        ads = Ads.filter(q)
    else:
        keyword = ''
    form = SearchForm(initial={'keyword': keyword})
    pagination = Paginator
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = pagination.get_page(page_num)
    context = {'rubric': rubric, 'page': page, 'ads': page.object_list, 'form': form}
    return render(request, 'main/by_rubric.html', context)


def detail(request, rubric_pk, pk):
    ad = get_object_or_404(Ads, pk=pk)
    ais = ad.additionalimage_set.all()
    context = {'ad': ad, 'ais': ais}
    return render(request, 'main/detail.html', context)
