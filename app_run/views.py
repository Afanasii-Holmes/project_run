from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def company_details(request):
    return Response({'company_name': 'Лососи и барабаны',
                     'slogan':'Табуретки навсегда',
                     'contacts': 'Тел. 222-232-3222'})