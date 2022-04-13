"""hms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from hotel.views import RoomListView, BookingListView, RoomDetailView, CancelBookingView, signup, signin, signout_user

app_name = 'hotel'

urlpatterns = [
    path('', RoomListView, name='room list'),
    path('booking_list/', BookingListView.as_view(), name='booking list'),
    path('room/<category>', RoomDetailView.as_view(), name='room detail view'),
    path('booking/cancel/<pk>', CancelBookingView.as_view(), name='cancel booking'),
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='sign in'),
    path('signout/', signout_user, name='sign out'),

]
