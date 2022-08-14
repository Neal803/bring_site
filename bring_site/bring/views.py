from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.urls import reverse_lazy
from .forms import RegisterUserForm, LoginUserForm, CommentForm
from .models import *
from .utils import send_email_for_verify
from django.core.exceptions import ValidationError
from django.contrib.auth.tokens import default_token_generator as token_generator


def index(request):
    context = {
        'stuffs': Stuff.objects.filter(is_active=True).order_by('priority'),
    }
    return render(request, template_name="bring/index.html", context=context)


def favorites(request):
    id = request.user.id
    if id:
        context = {
            'stuffs': Stuff.objects.filter(fans__id=id, is_active=True)
        }
        return render(request, template_name="bring/favorites.html", context=context)
    else:
        return redirect('bring:login-page')


def action_stuffs(request):
    context = {
        'stuffs': Stuff.objects.filter(is_active=True, is_action=True).order_by('priority'),
    }
    return render(request, template_name="bring/actions.html", context=context)


class ShowStuff(DetailView):
    model = Stuff
    template_name = 'bring/stuff.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'stuff'


def comments(request):
    context = {
        'objects': Stuff.objects.filter(is_active=True)
    }
    return render(request, template_name="bring/comments.html", context=context)


def add_stuff_comment(request, slug):
    form = CommentForm(request.POST)
    if form.is_valid() and form.data.get('comment_text') != '':
        comment_text = form.data.get('comment_text')
        rating_vote = form.data.get('rating_vote')
        if rating_vote == '':
            rating_vote = 0.0
        stuff = Stuff.objects.get(slug=slug)
        author = request.user
        new_comment = Comment(author=author, comment_text=comment_text, stuff=stuff, rating_vote=rating_vote)
        new_comment.save()
        # return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))


class StuffCategory(ListView):
    model = Stuff
    template_name = 'bring/category.html'
    context_object_name = 'stuffs'

    def get_queryset(self):
        return Stuff.objects.filter(cat__slug=self.kwargs['cat_slug'], is_active=True).order_by('priority')


class SearchResultsView(ListView):
    model = Stuff
    template_name = 'bring/search.html'

    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('search')
        if query:
            query_search = query.lower()
            stuffs_search = Stuff.objects.filter(for_search__icontains=query_search, is_active=True)
            return render(request, template_name=self.template_name, context={
                'search_list': stuffs_search,
                'search_str': query,
            })
        return redirect('bring:index')


#################################
# def ajax_add_fav(request):
#     if request.is_ajax():
#         stuff_id = int(request.POST.get('stuff_id'))
#         fan_id = int(request.POST.get('fan_id'))
#
#         data = {
#             'added': True,
#             'stuff_id': stuff_id,
#             'fan_id': fan_id
#         }


#     def add_fav_stuff(request, stuff_id):
#         stuff = Stuff.objects.get(pk=stuff_id)
#         fan = request.user
#         try:
#             if stuff not in fan.favs.all():
#                 fan.favs.add(stuff)
#                 fan.save()
#             return redirect(request.META.get('HTTP_REFERER'))
#         except:
#             return redirect('bring:login-page')

# User


class UserPage(LoginRequiredMixin, TemplateView):
    model = CustomUser
    template_name = 'bring/user_page.html'
    extra_context = {}
    login_url = reverse_lazy('bring:login-page')


class LoginAjaxView(View):

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return JsonResponse(data={}, status=201)
            return JsonResponse(
                data={'error': 'Логин и пароль невалидные'},
                status=400
            )
        return JsonResponse(
            data={'error': 'Введите логин и пароль'},
            status=400
        )


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('bring:index'))


class Register(View):
    template_name = 'bring/registration_page.html'
    # success_url = '/bring/user/'

    def get(self, request):
        context = {
            'form': RegisterUserForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = RegisterUserForm(request.POST)

        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            send_email_for_verify(request, user)
            return redirect('bring:confirm-email')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


class EmailVerify(View):
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and token_generator.check_token(user, token):
            user.email_verify = True
            user.save()
            login(request, user)
            return redirect('bring:index')
        return redirect('bring:invalid-verify')

    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,
                CustomUser.DoesNotExist, ValidationError):
            user = None
        return user


def confirm_email(request):
    context = {
        'text': 'Проверить почту',
    }
    return render(request, template_name="bring/confirm_email.html", context=context)


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'bring/login_page.html'

    def get_success_url(self):
        return reverse_lazy('bring:user-page')


def add_fav_stuff(request, stuff_id):
    stuff = Stuff.objects.get(pk=stuff_id)
    fan = request.user
    try:
        if stuff not in fan.favs.all():
            fan.favs.add(stuff)
            fan.save()
        return redirect(request.META.get('HTTP_REFERER'))
    except:
        return redirect('bring:login-page')


def del_fav_stuff(request, stuff_id):
    stuff = Stuff.objects.get(pk=stuff_id)
    fan = request.user
    if stuff in fan.favs.all():
        fan.favs.remove(stuff)
        fan.save()
    return redirect(request.META.get('HTTP_REFERER'))

# API


# class StuffListApiViews(generics.ListAPIView):
#     serializer_class = StuffListSerializer
#     queryset = Stuff.objects.filter(is_active=True).order_by('priority')
