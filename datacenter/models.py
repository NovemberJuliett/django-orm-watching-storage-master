from django.db import models
from django.utils.timezone import localtime
import datetime


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )


def get_duration(visit):
    entered_at = visit.entered_at
    leaved_at = visit.leaved_at
    local_time = localtime()
    if leaved_at:
        return (leaved_at - entered_at).total_seconds()
    else:
        return (local_time - entered_at).total_seconds()


def format_duration(visit):
    duration = get_duration(visit)
    hours, remainder = divmod(duration, 3600)
    minutes, seconds = divmod(remainder, 60)
    formatted_duration = ('{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds)))
    return formatted_duration

# visit = Visit.objects.all()[0]
# print(get_duration(visit))
# print(format_duration(visit))
