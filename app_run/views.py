from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from .models import Run
from .serializers import RunSerializer, UserSerializer
from django.contrib.auth.models import User


@api_view(['GET'])
def company_details(request):
    return Response({'company_name': 'Лососи и барабаны',
                     'slogan':'Табуретки навсегда',
                     'contacts': 'Тел. 222-232-3222'})


class RunPagination(PageNumberPagination):
    page_size = 6  # Количество объектов на странице по умолчанию
    page_size_query_param = 'size'
    max_page_size = 12


class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.select_related('athlete').all()
    serializer_class = RunSerializer
    pagination_class = RunPagination

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_superuser=False)
    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name']

    def get_queryset(self):
        qs = self.queryset
        user_type = self.request.query_params.get('type')
        if user_type and user_type=='coach':
            qs = qs.filter(is_staff=True)
        if user_type and user_type=='athlete':
            qs = qs.filter(is_staff=False)
        return qs


class StatusStartView(APIView):
    def post(self, request, run_id):
        run = get_object_or_404(Run, id=run_id)
        if run.status == 'init':
            run.status = 'in_progress'
            run.save()
            return Response({'message': 'Все ништяк'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Этот забег стартовать нельзя, он уже стартовал'},
                            status=status.HTTP_400_BAD_REQUEST)


class StatusStopView(APIView):
    def post(self, request, run_id):
        run = get_object_or_404(Run, id=run_id)
        if run.status == 'in_progress':
            run.status = 'finished'
            run.save()
            return Response({'message': 'Все ништяк'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Этот забег финишировать нельзя, он еще не стартовал или уже завершен'},
                            status=status.HTTP_400_BAD_REQUEST)

