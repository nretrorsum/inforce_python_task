
from django.urls import path
from .views import VoteCreateView, TodayMenuResultsView

urlpatterns = [

    path('vote/', VoteCreateView.as_view(), name='vote-create'),
    path('results/', TodayMenuResultsView.as_view(), name='today-menu-results'),
]
