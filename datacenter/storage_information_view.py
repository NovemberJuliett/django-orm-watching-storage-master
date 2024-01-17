from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from datacenter.models import format_duration


def storage_information_view(request):
    not_leaved = Visit.objects.filter(leaved_at__isnull=True)
    non_closed_visits = []

    for person in not_leaved:
        name = person.passcard
        entered_at = person.entered_at
        duration = format_duration(person)
        print(duration)

        non_closed_visits.append({
            'who_entered': name,
            'entered_at': entered_at,
            'duration': duration,
        })

    context = {
        'non_closed_visits': non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
