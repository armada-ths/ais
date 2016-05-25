from django.http import JsonResponse

def root(request):
    return JsonResponse({'message':'Welcome to the Armada API!'})

