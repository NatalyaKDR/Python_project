from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import Group

from app_users.forms import CommentForm
from app_users.models import Item, UserComment


# Create your views here.
def index(request):
    return render(request,'app_users/index.html')


def main(request):
    items=Item.objects.all()
    context={'items':items}
    return render(request,'app_users/main.html',context)

def get_test(request, test):
    if test=="1":
        return render(request, 'app_users/test_1.html',{'test':test})
    elif test == "2":
        return render(request, 'app_users/test_2.html', {'test':test})
    elif test == "3":
        return render(request, 'app_users/test_3.html', {'test':test})
    else:
        return HttpResponseNotFound("Тест находится в разработке")

def item_details(request, pk):
    item = Item.objects.get(id=pk)
    comments = item.usercomments_item.order_by('-id')
#пагинация
    paginator = Paginator(comments, 3)
    page_number = request.GET.get('page')
    page_obj=paginator.get_page((page_number))

    context = {'item': item, 'comments': comments, 'page_obj': page_obj}
    return render(request, 'app_users/item_details.html', context)

#CRUD
def add(request, id_item):
    if not request.user.has_perm('app_users.add_usercomment'):
        return redirect('/login/')
    item=get_object_or_404(Item, pk=id_item)
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user  # чтобы user автоматически подставлялся
            form.instance.item = item
            form.save()
            return redirect(f'/items/{item.pk}')
    form=CommentForm()
    context={'form': form, 'item':item}
    return render(request, 'app_users/add.html', context)


def update(request,pk):
    if not request.user.has_perm('app_users.change_usercomment'):
        raise PermissionDenied()
    comment = UserComment.objects.get(id=pk)
    form=CommentForm(instance=comment)

    pk = comment.item.pk
    item = get_object_or_404(Item, pk=pk)

    if request.method == 'POST':
        form=CommentForm(request.POST, instance=comment)
        if request.user.username == "admin" or comment.author == request.user:
            if form.is_valid():
                form.instance.author = request.user  # чтобы user автоматически подставлялся
                form.instance.item=item
                form.save()
            return redirect(f'/items/{pk}')
        else:
            raise PermissionDenied()
    context={'form':form, 'item':item}
    return render(request, 'app_users/update.html', context)


def delete(request, pk):
    if not request.user.has_perm('app_users.delete_usercomment'):
        raise PermissionDenied()
    comment =UserComment.objects.get(id=pk)
    pk=comment.item.pk
    if request.method=="POST":
        if request.user.username == "admin" or comment.author == request.user:
            comment.delete()
            return redirect(f'/items/{pk}')
        else:
            raise PermissionDenied()
    context = {'comment': comment, 'pk': pk}
    return render(request, 'app_users/delete.html', context)


#Пользовательская часть
class MyLoginView(LoginView): #страничка аутентификации
    template_name= 'app_users/login.html'
    redirect_authenticated_user = True

def MyRegisterView(request): #страничка регистрации
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            user = form.save(commit=False)

            user.save()

            user_group = Group.objects.get(name='Registrated_users') #автоматически добавит в группу

            user.groups.add(user_group)

            username=form.cleaned_data.get('username')
            raw_password=form.cleaned_data.get('password1')
            user=authenticate(username=username, password=raw_password)
            login(request,user)
            return redirect('/main')
    else:
        form=UserCreationForm()
    return render(request,'app_users/register.html',{'form':form})

class MyLogoutView(LogoutView): #logout c переходом на главную
    next_page='/'

