from django.conf.urls import url 
from . import views 

urlpatterns = [
	url('', views.index, name='location_bot'),
        url('cartGenerate/', views.cartGenerate, name='cartGenerate'),
]
