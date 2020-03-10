from django.http import JsonResponse

from .subject_model import Subject
from ..standpoint.standpoint_model import Standpoint


def get_subjects(request):
    subjects = Subject.objects.values()
    subject_list = list(subjects)
    return JsonResponse(subject_list, safe=False)


# Get all the subject standpoints
def get_subject_standpoints(request, subject):
    subject_standpoints = Standpoint.objects.filter(subject__id=subject).values()
    standpoint_list = list(subject_standpoints)
    return JsonResponse(standpoint_list, safe=False)


def get_party_subject_standpoints(request, subject, party):
    party_standpoints = Standpoint.objects.filter(subject__id=subject, party__abbreviation=party).values()
    standpoint_list = list(party_standpoints)
    return JsonResponse(standpoint_list, safe=False)
