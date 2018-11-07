from django.shortcuts import redirect, render
from django.views.generic import TemplateView


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.user_type == 2:
            return redirect('agent:home')
        elif request.user.user_type == 1:
        	return redirect('customer:home')
        elif request.user.user_type == 3:
            return redirect('executive:home')

    return render(request, 'userAuth/home.html')
