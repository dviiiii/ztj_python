from django.urls import path

import  hqdba.controller.login as login
import  hqdba.controller.hqdba as hqdba
urlpatterns = [
    path('login/', login.index, name='index'),
    path('hqdba/addConfig', hqdba.addConfig, name='addConfig'),
    path('hqdba/queryConfig', hqdba.queryConfig, name='queryConfig'),

    # path( '<int:question_id>/', login.detail, name='detail' ),
    # # ex: /polls/5/results/
    # path( '<int:question_id>/results/', login.results, name='results' ),
    # # ex: /polls/5/vote/
    # path( '<int:question_id>/vote/', login.vote, name='vote' ),
]