from django.shortcuts import render


from django.http import HttpResponse
from .models import Question
from .models import User


def index(request):
    user_list = User.objects.order_by( '-ts' )[:5]
    output = ', '.join( [q.username for q in user_list] )
    return HttpResponse( output )

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)