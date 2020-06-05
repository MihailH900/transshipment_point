"""aplication urls"""

from django.conf.urls import url
from location_bot.views import index, cartGenerate, MessageView

urlpatterns = [
    url('', index, name='location_bot'),
    url('cartGenerate/', cartGenerate, name='cartGenerate'),
    url('MessageView',MessageView.as_view(), name='MessageView')
]
