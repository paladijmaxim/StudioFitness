from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Avg, Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Event, Club, Trainer, Tariff, UserMembership, Class, Booking
from .forms import EventForm

def index(request):
    latest_events = Event.objects.filter(status='scheduled').order_by('start_at')[:5]
    clubs = Club.objects.all()[:5]
    trainers = Trainer.objects.all()[:6]

    active_tariffs = Tariff.objects.filter(is_active=True).annotate(
        active_memberships_count=Count(
            'memberships',
            filter=Q(memberships__status='active')
        )
    )[:4]

    popular_categories = Class.objects.annotate(
        event_count=Count('events'),
        avg_duration=Avg('duration_minutes'),
        avg_level=Avg('level')
    ).filter(event_count__gt=0).order_by('-event_count')[:4]
    total_members = UserMembership.objects.filter(status='active').count()
    total_trainers = Trainer.objects.count()
    total_classes = Event.objects.filter(status='completed').count()
    clubs_count = Club.objects.count()

    context = {
        'latest_events': latest_events,
        'clubs': clubs,
        'trainers': trainers,
        'active_tariffs': active_tariffs,
        'popular_categories': popular_categories,
        'total_members': total_members,
        'total_trainers': total_trainers,
        'total_classes': total_classes,
        'clubs_count': clubs_count,
    }
    return render(request, 'FitnessStudio/index.html', context)


def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'FitnessStudio/event_detail.html', {'event': event})


def trainer_detail(request, trainer_id):
    trainer = get_object_or_404(Trainer, pk=trainer_id)
    return render(request, 'FitnessStudio/trainer_detail.html', {'trainer': trainer})


@login_required
def event_list(request):
    """Просмотр списка всех событий"""
    events = Event.objects.all().order_by('-start_at')
    return render(request, 'FitnessStudio/event_list.html', {'events': events})


@login_required
def event_create(request):
    """Создание нового события"""
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            messages.success(request, 'Событие успешно создано!')
            return redirect('event_list')
    else:
        form = EventForm()

    return render(request, 'FitnessStudio/event_form.html', {
        'form': form,
        'title': 'Создание нового события'
    })


@login_required
def event_edit(request, event_id):
    """Редактирование события"""
    event = get_object_or_404(Event, pk=event_id)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Событие успешно обновлено!')
            return redirect('event_list')
    else:
        form = EventForm(instance=event)

    return render(request, 'FitnessStudio/event_form.html', {
        'form': form,
        'title': 'Редактирование события',
        'event': event
    })


@login_required
def event_delete(request, event_id):
    """Удаление события"""
    event = get_object_or_404(Event, pk=event_id)

    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Событие успешно удалено!')
        return redirect('event_list')

    return render(request, 'FitnessStudio/event_confirm_delete.html', {
        'event': event
    })
