from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.list_stack,name='list_stack'),
    path('check/',views.event_check,name='event_check'),
]
