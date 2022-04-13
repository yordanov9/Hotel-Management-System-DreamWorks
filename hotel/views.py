# Create your views here.
import password as password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect

from hotel.forms.login_form import SignInForm
from hotel.forms.signup_form import SignUpForm, ProfileForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, View, DeleteView

from hotel.forms.form import AvailabilityForm
from hotel.models import Room, Booking
from hotel.booking_functions.availability import check_availability


def RoomListView(request):
    room = Room.objects.all().first()
    room_categories = dict(room.ROOM_CATEGORIES)
    room_values = room_categories.values()

    room_list = []
    for category in room_categories:
        room = room_categories.get(category)
        room_url = reverse('hotel:room detail view', kwargs={'category': category})
        room_list.append((room, room_url))

    context = {
        'room_list': room_list,
    }
    return render(request, 'room_list.html', context)


class BookingListView(LoginRequiredMixin,ListView):
    model = Booking
    template_name = "booking_list.html"

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            booking_list = Booking.objects.all()
            return booking_list
        else:
            booking_list = Booking.objects.filter(user=self.request.user)
            return booking_list


class RoomDetailView(View):
    def get(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        form = AvailabilityForm
        room_list = Room.objects.filter(category=category)

        if len(room_list) > 0:
            room = room_list[0]
            room_category = dict(room.ROOM_CATEGORIES).get(room.category, None)
            context = {
                'room_category': room_category,
                'form': form,
            }
            return render(request, 'room_detail_view.html', context)

        else:
            return HttpResponse('Category does not exist', status=404)

    def post(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        room_list = Room.objects.filter(category=category)
        available_rooms = []
        form = AvailabilityForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

        for room in room_list:
            if check_availability(room, data['check_in'], data['check_out']):
                available_rooms.append(room)

        if len(available_rooms) > 0:
            room = available_rooms[0]
            booking = Booking.objects.create(
                user=self.request.user,
                room=room,
                check_in=data['check_in'],
                check_out=data['check_out'],
            )

            booking.save()
            return HttpResponse(booking)
        else:
            return HttpResponse('This category of rooms is booked! Try another one.')


class CancelBookingView(DeleteView):
    model = Booking
    template_name = 'booking_cancel_view.html'
    success_url = reverse_lazy('hotel:booking list')


@transaction.atomic()
def signup(request):
    if request.method == 'GET':
        context = {
            'user_form': SignUpForm(),
            'profile_form': ProfileForm(),
        }
        return render(request, 'register.html', context)
    else:
        user_form = SignUpForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("hotel:room list")

        context = {
            'user_form': SignUpForm(),
            'profile_form': ProfileForm(),
        }
        return render(request, 'register.html', context)


def signin(request):
    if request.method == 'GET':
        context = {
            'signin_form': SignInForm(),
        }
        return render(request, 'login.html', context)
    else:
        signin_form = SignInForm(request.POST)
        if signin_form.is_valid():
            username = signin_form.cleaned_data['username']
            password = signin_form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect('hotel:room list')

        context = {
            'signin_form': signin_form,
        }

        return render(request, 'login.html', context)


@login_required()
def signout_user(request):
    logout(request)
    return redirect('hotel:room list')
# class BookingView(FormView):
#     form_class = AvailabilityForm
#
#     def form_valid(self, form):
#         data = form.cleaned_data
#         room_list = Room.objects.filter(category=data['room_category'])
#         available_rooms = []
#
#         for room in room_list:
#             if check_availability(room, data['check_in'], data['check_out']):
#                 available_rooms.append(room)
#
#         if len(available_rooms) > 0:
#             room = available_rooms[0]
#             booking = Booking.objects.create(
#                 user=self.request.user,
#                 room=room,
#                 check_in=data['check_in'],
#                 check_out=data['check_out'],
#             )
#
#             booking.save()
#             return HttpResponse(booking)
#         else:
#             return HttpResponse('This category of rooms is booked! Try another one.')
