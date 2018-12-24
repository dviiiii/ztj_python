from django.urls import path

import  hqdba.controller.login as login
import  hqdba.controller.hqdba as hqdba
import  hqdba.controller.book as book

urlpatterns = [
    path('login/', login.index, name='index'),
    path('test/', hqdba.test, name='test'),
    path('hqdba/addConfig', hqdba.addConfig, name='addConfig'),
    path('hqdba/queryConfig', hqdba.queryConfig, name='queryConfig'),
    path('hqdba/queryAllTables', hqdba.queryAllTables, name='queryAllTables'),
    path('hqdba/queryOneTableCol', hqdba.queryOneTableCol, name='queryOneTableCol'),
    path('hqdba/queryOneTable', hqdba.queryOneTable, name='queryOneTable'),
    path('hqdba/toMasking', hqdba.toMasking, name='toMasking'),

    path('online/book/addBook', book.addBook, name='addBook'),
    # path( '<int:question_id>/', login.detail, name='detail' ),
    # # ex: /polls/5/results/
    # path( '<int:question_id>/results/', login.results, name='results' ),
    # # ex: /polls/5/vote/
    # path( '<int:question_id>/vote/', login.vote, name='vote' ),
]