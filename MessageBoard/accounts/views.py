from django.contrib.auth.models import User, Group
from django.shortcuts import render

from accounts.forms import VerifyCodeForm
from accounts.models import *

# Create your views here.
def register_confirm(request, pk):
    cong = ''
    if User.objects.filter(pk=pk).exists():
        author = User.objects.get(pk=pk)
        code = author.v_user.code
    else:
        author = None
    if request.method == 'POST':
        form = VerifyCodeForm(request.POST)
        if form.is_valid():

            if code == form.cleaned_data['code']:
                authorized_users = Group.objects.get(name="authorized_users")
                author.groups.add(authorized_users)
                cong = "Поздравляем с успешной регистрацией на сайте"
                # return redirect(to=reverse_lazy("login"))
            else:
                form.add_error('code', 'Некорректный код подтверждения')
    #         ('Некорректный код подтверждения')
    else:
        form = VerifyCodeForm
    data = {'title': 'Завершите регистрацию',
            'header1': 'Для завершения регистрации введите код подтверждения, направленный на адрес, указанный при регистрации',
            'cong': cong,
            'author': author,
            'form': form,
            }

    return render(request, 'registration/register_confirm.html', context=data)