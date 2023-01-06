from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Wcapi
from .serializers import WcapiSerializer

class WcapiAPIView(APIView):
    def get(self,request):
        lst = Wcapi.objects.all().values()
        return Response({'users': list(lst)})

    def put(self,request):
        data = Wcapi.objects.get(user_id=request.data['user_id'],number=request.data['number'])
        data.is_parser, data.is_online, data.last_online = \
            request.data['is_parser'],request.data['is_online'], request.data['last_online'],
        data.save()
        return Response({request.data['user_id']: 'edit'})

    def post(self,request):
        post_new = Wcapi.objects.create(
            user_id=request.data['user_id'],
            number=request.data['number'],
            is_parser=request.data['is_parser'],
            is_online=request.data['is_online'],
        )
        return Response({'user': model_to_dict(post_new)})



class WcapiAPIViewDelete(APIView):
    def post(self,request):
        Wcapi.objects.filter(user_id=request.data['user_id'],number=request.data['number']).delete()

        return Response({request.data['user_id']: 'delete'})

