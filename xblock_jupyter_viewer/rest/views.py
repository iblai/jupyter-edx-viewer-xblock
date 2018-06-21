import logging
import traceback
import sys

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from django.http import HttpResponse

from xblock_jupyter_viewer.jupyter_utils import process_nb
from xblock_jupyter_viewer.rest.serializers import NotebookViewSerializer

log = logging.getLogger(__name__)

class NotebookViewer(APIView):
    """Fetches noteboook at url and returns HTML to be used in iframe"""

    renderer_classes = (JSONRenderer, )

    def get(self, request):
        nb_data = NotebookViewSerializer(data=request.query_params)
        # Query Param Validation
        if not nb_data.is_valid():
            return Response(data=nb_data.errors, status=400)

        try:
            html = process_nb(**nb_data.validated_data)

        # Thrown when nbformat fails - caution, other errors could throw this
        except ValueError as e:
            log.exception(e)
            error = "An error occurred while converting {}. Please see the "\
                    "LMS/CMS logs for more details"\
                    .format(nb_data.validated_data['url'])
            return HttpResponse(error, status=400)

        # Handle other exceptions nicely
        except Exception as e:
            log.exception(e)
            msg = "{} -- Check lms/cms logs for more information".format(e)
            return HttpResponse(msg, status=500)

        return HttpResponse(html, status=200)

