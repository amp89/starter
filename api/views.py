from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from rest_framework.response import Response
from .serializers import NoteSerializer
from .models import Note
from rest_framework import status
from django.http import QueryDict
from view_classes import APIAuthView

class ExampleAuthView(APIAuthView):
    def get(self, request, *args, **kwargs):
        # Payload is @ request.data
        if note_id:
            note = Note.objects.get(id=note_id, user=request.user)
            res =  NoteSerializer(note).data
            return Response(res)
        else:
            notes = Note.objects.filter(user=request.user)
            res = NoteSerializer(notes, many=True).data
            return Response(res)

class ExampleNoAuthView(APIView):
    def get(self, request, *args, **kwargs):
        # Payload is @ request.data
        if note_id:
            note = Note.objects.get(id=note_id, user=request.user)
            res =  NoteSerializer(note).data
            return Response(res)
        else:
            notes = Note.objects.filter(user=request.user)
            res = NoteSerializer(notes, many=True).data
            return Response(res)
