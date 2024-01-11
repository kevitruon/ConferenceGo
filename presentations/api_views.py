from django.http import JsonResponse

from .models import Presentation, Status
from common.json import ModelEncoder
from django.views.decorators.http import require_http_methods
from events.models import Conference
import json


@require_http_methods(["GET", "POST"])
def api_list_presentations(request, conference_id=None):
    if request.method == "GET":
        if conference_id is not None:
            presentations = Presentation.objects.filter(
                conference_id=conference_id
            )
            presentations_list = [
                PresentationListEncoder().default(pres)
                for pres in presentations
            ]
            return JsonResponse(
                {"presentations": presentations_list},
                safe=False,
            )
    else:  # POST branch
        content = json.loads(request.body)

        # Get the Conference object and put its id in the content dict
        try:
            conference = Conference.objects.get(id=conference_id)
            content["conference_id"] = conference.id
        except Conference.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid conference id"},
                status=400,
            )

        presentation = Presentation.create(**content)
        return JsonResponse(
            PresentationDetailEncoder().default(presentation),
            safe=False,
        )


class PresentationListEncoder(ModelEncoder):
    model = Presentation
    properties = ["title"]


class PresentationDetailEncoder(ModelEncoder):
    model = Presentation
    properties = [
        "presenter_name",
        "company_name",
        "presenter_email",
        "title",
        "synopsis",
        "created",
    ]


@require_http_methods(["GET", "PUT", "DELETE"])
def api_show_presentation(request, id):
    if request.method == "GET":
        presentation = Presentation.objects.get(id=id)
        return JsonResponse(
            presentation,
            encoder=PresentationDetailEncoder,
            safe=False,
        )
    elif request.method == "PUT":
        content = json.loads(request.body)
        presentation = Presentation.objects.get(id=id)
        presentation.presenter_name = content["presenter_name"]
        presentation.company_name = content["company_name"]
        presentation.presenter_email = content["presenter_email"]
        presentation.title = content["title"]
        presentation.synopsis = content["synopsis"]
        presentation.save()
        return JsonResponse(
            presentation,
            encoder=PresentationDetailEncoder,
            safe=False,
        )
    else:  # DELETE branch
        count, _ = Presentation.objects.filter(id=id).delete()
        return JsonResponse({"deleted": count > 0})
