import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from banquet.models import Banquet, Seat

@require_POST
@csrf_exempt
def save_seat(request, banquet_pk, seat_pk):
	banquet = get_object_or_404(Banquet, pk = banquet_pk)
	seat = get_object_or_404(Seat, table__banquet = banquet, pk = seat_pk)
	
	if not request.user: return JsonResponse({'message': 'Authentication required.'}, status = 403)
	
	data = json.loads(request.body)
	
	seat.top = data['top']
	seat.left = data['left']
	seat.save()
	
	return JsonResponse({'status': 'ok'}, status = 200)
