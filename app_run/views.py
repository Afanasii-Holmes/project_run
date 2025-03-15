from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Run
from .serializers import RunSerializer


@api_view(['GET'])
def company_details(request):
    return Response({'company_name': 'Лососи и барабаны',
                     'slogan':'Табуретки навсегда',
                     'contacts': 'Тел. 222-232-3222'})

class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.all()
    serializer_class = RunSerializer