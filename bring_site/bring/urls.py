from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path
from django.views.generic import TemplateView

from . import views
from .views import StuffCategory, SearchResultsView, UserPage, LoginUser, ShowStuff, Register, EmailVerify, LoginAjaxView, RegistrationAjaxView

app_name = "bring"



urlpatterns = [
    path('', views.index, name='index'),
    path('actions/', views.action_stuffs, name='actions'),
    path('stuff/<slug:slug>', ShowStuff.as_view(), name='stuff'),
    path('category/<slug:cat_slug>', StuffCategory.as_view(), name='category'),
    path('search/', SearchResultsView.as_view(), name='search'),

    path('user/', UserPage.as_view(), name='user-page'),
    path('user/login/', LoginUser.as_view(), name='login-page'),
    path('user/logout/', views.logout_user, name='logout-user'),
    path('user/registration/', Register.as_view(), name='registration-user'),
    path('confirm_email/', views.confirm_email, name='confirm-email'),
    path('verify_email/<uidb64>/<token>', EmailVerify.as_view(), name='verify-email'),
    path('invalid_verify/', TemplateView.as_view(template_name='bring/invalid_verify.html'), name='invalid-verify'),

    path('login_ajax/', LoginAjaxView.as_view(), name='login-ajax'),
    path('registration_ajax/', RegistrationAjaxView.as_view(), name='registration-ajax'),
    path('contacts_ajax/', TemplateView.as_view(template_name='bring/modal-contacts.html'), name='contacts-ajax'),

    path('password_reset', PasswordResetView.as_view(template_name='bring/password_reset_form.html'), name='password_reset'),
    # path('password_reset/done', PasswordResetDoneView.as_view(template_name='bring/passwort_reset_done.html'), name='password_reset_done'),
    # path('reset/<uidb64>/<token>', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('favorites/', views.favorites, name='favorites'),

    path('comments/', views.comments, name='comments'),
    path('add/stuff/<slug:slug>/comment/', views.add_stuff_comment, name='add-comment'),

    path('stuff/<int:stuff_id>/fav', views.fav_stuff, name='stuff-fan'),
]
