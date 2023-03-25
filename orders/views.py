from fair.models import Fair
from .models import Product
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from fair.models import Fair
from django.contrib.auth.decorators import permission_required
