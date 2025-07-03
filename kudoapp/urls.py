from django.urls import path
from .api import UserAPI, GiveKudoAPI, ReceivedKudosAPI, RemainingKudosAPI

urlpatterns = [
    path('users/', UserAPI.as_view(), name='user-list'),
    path('give/', GiveKudoAPI.as_view(), name='give-kudo'),
    path('received/', ReceivedKudosAPI.as_view(), name='received-kudos'),
    path('remaining/', RemainingKudosAPI.as_view(), name='remaining-kudos'),
]
