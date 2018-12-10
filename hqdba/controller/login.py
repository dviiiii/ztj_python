from django.shortcuts import render

from django.http import HttpResponse
from ..model.model_user import User


def index(request):
    user_list = User.objects.order_by( '-ts' )[:5]
    output = ', '.join( [q.username for q in user_list] )
    return HttpResponse( output )