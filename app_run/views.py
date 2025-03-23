from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from django_filters.rest_framework import DjangoFilterBackend

from .models import Run, AthleteInfo, Challenge, Position
from .serializers import RunSerializer, UserSerializer, ChallengeSerializer, PositionSerializer
from django.contrib.auth.models import User


@api_view(['GET'])
def company_details(request):
    return Response({'company_name': 'Лососи и барабаны',
                     'slogan':'Табуретки навсегда',
                     'contacts': 'Тел. 222-232-3222'})


class MyPagination(PageNumberPagination):
    page_size_query_param = 'size'


class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.select_related('athlete').all()
    serializer_class = RunSerializer
    pagination_class = MyPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'athlete']
    ordering_fields = ['created_at']


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    pagination_class = MyPagination
    queryset = User.objects.filter(is_superuser=False)
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['id']

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
            # -------------------------------------------
            if Run.objects.filter(status='finished', athlete=run.athlete).count() >= 10:
                challenge, created = Challenge.objects.get_or_create(full_name='Сделай 10 Забегов!',
                                                                     athlete=run.athlete)
            # -------------------------------------------
            return Response({'message': 'Все ништяк'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Этот забег финишировать нельзя, он еще не стартовал или уже завершен'},
                            status=status.HTTP_400_BAD_REQUEST)


class AthleteInfoView(APIView):

    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        athlete_info, created = AthleteInfo.objects.get_or_create(user=user)
        return Response({'weight': athlete_info.weight,
                         'goals': athlete_info.goals,
                         'user_id': athlete_info.user.id

        })

    def put(self, request, user_id):
        goals = request.data.get('goals')
        weight = request.data.get('weight')

        if not str(weight).isdigit() or int(weight) <= 0 or int(weight) >= 900:
            return Response({'message': 'weight должен быть числом больше 0 и меньше 900'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(id=user_id).exists():
            user = User.objects.get(id=user_id)
        else:
            return Response({'message':'Такого User не существует'}, status=status.HTTP_404_NOT_FOUND)

        athlete_info, created = AthleteInfo.objects.update_or_create(
            user = user,
            defaults = {'goals':goals, 'weight':weight}
        )

        return Response({'message': 'Создано/изменено'}, status=status.HTTP_201_CREATED)


class ChallengeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer