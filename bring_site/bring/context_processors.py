from .forms import AuthenticationAjaxForm
from .models import Category


def category_global(request):
    return {'categories_list_global': Category.objects.filter(is_active=True).order_by('priority')}


def modal_login(request):
    context = {
        'login_ajax': AuthenticationAjaxForm()
    }
    return context
