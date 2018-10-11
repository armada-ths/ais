from django.contrib import admin
from .models import Banquet, Participant, Invitation, Table, Seat


admin.site.register(Banquet)
admin.site.register(Participant)
admin.site.register(Invitation)
admin.site.register(Table)
admin.site.register(Seat)
