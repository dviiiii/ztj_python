from django.urls import path

import  hqdba.controller.login as login
import  hqdba.controller.hqdba as hqdba
import  hqdba.controller.book as book
import  hqdba.controller.source_bk as source_bk

urlpatterns = [
    path('login/', login.index, name='index'),
    path('userinfo/', login.userinfo, name='userinfo'),
    # path('source_bk_test/', source_bk.source_bk_test, name='source_bk_test'),
    path('test/', hqdba.test, name='test'),
    path('hqdba/addConfig', hqdba.addConfig, name='addConfig'),
    path('hqdba/queryConfig', hqdba.queryConfig, name='queryConfig'),
    path('hqdba/removeConfig', hqdba.removeConfig, name='removeConfig'),
    path('hqdba/queryAllTables', hqdba.queryAllTables, name='queryAllTables'),
    path('hqdba/queryOneTableCol', hqdba.queryOneTableCol, name='queryOneTableCol'),
    path('hqdba/queryOneTable', hqdba.queryOneTable, name='queryOneTable'),

    path('hqdba/toMasking', hqdba.toMasking, name='toMasking'),
    path('hqdba/mask_01_queryNum', hqdba.mask_01_queryNum, name='mask_01_queryNum'),
    path('hqdba/mask_01_toMasking', hqdba.mask_01_toMasking, name='mask_01_toMasking'),

    path('book/addbook', book.addBook, name='addBook'),
    path('book/booklist', book.getBookList, name='getBookList'),
    path('book/getreviewinfo', book.getReviewInfo, name='getReviewInfo'),
    path('book/deletebook', book.deleteBook, name='deleteBook'),
    path('book/addreadinfo', book.addReadInfo, name='addReadInfo'),
    # path( '<int:question_id>/', login.detail, name='detail' ),
    # # ex: /polls/5/results/
    # path( '<int:question_id>/results/', login.results, name='results' ),
    # # ex: /polls/5/vote/
    # path( '<int:question_id>/vote/', login.vote, name='vote' ),
]