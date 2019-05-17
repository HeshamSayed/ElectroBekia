from django.shortcuts import render, redirect
from .forms import SignupForm
from django.views import View
from django.http import HttpResponseRedirect
from .models import User
from django.contrib.auth import login


class Signup(View):
  def get(self, request):
    if request.user.is_authenticated:
      return redirect('/')
    form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})

  def post(self, request):
    if request.user.is_authenticated:
      return redirect('/')
    form = SignupForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      user.save()
      return redirect('accounts:login')
    else:
      return render(request, 'accounts/signup.html', {'form': form})


def user_login(request):
  if request.user.is_authenticated:
    return redirect('/')
  if request.method == 'POST':
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
      user = User.objects.get(email__iexact=email) or User.objects.get(phone__iexact=email)
    except User.DoesNotExist:
      context = {
        'form': {
          'errors': 'رقم الهاتف او البريد الالكترونى خطا من فضلك اعد المحاوله'
        },
      }
      return render(request, 'accounts/login.html', context)

    if user.check_password(password):
      login(request, user)
      next = request.POST.get('next', '/') or '/'
      return HttpResponseRedirect(next)
    else:
      context = {
        'form': {
          'errors': 'حدث خطا فى الرقم السري من فضلك اعد المحاوله'
        },
      }
      return render(request, 'accounts/login.html', context)
  else:
    return render(request, 'accounts/login.html', {})

