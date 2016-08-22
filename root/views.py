from django.shortcuts import render, redirect


def index(request):
    next = request.GET.get('next')
    if next and next[-1] == '/':
        next = next[:-1]
    print(next)
    if request.user.is_authenticated():
        return redirect('/recruitment')
    return render(request, 'login.html', {'next': next})
# Create your views here.
