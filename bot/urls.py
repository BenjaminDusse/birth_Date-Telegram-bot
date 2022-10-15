from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from bot.bot import UpdateBot


urlpatterns = [
    path('bot/', csrf_exempt(UpdateBot.as_view())),
]

