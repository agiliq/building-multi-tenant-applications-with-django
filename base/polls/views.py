from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from .models import Poll


def polls_list(request):
    MAX_OBJECTS = 20
    polls = Poll.objects.all()[:20]
    data = {
        "results": list(
            polls.values("pk", "question", "created_by__username", "pub_date")
        )
    }
    return JsonResponse(data)


def polls_detail(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    data = {
        "results": {
            "question": poll.question,
            "created_by": poll.created_by.username,
            "pub_date": poll.pub_date,
        }
    }
    return JsonResponse(data)
