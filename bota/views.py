from django.shortcuts import render
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .utils import send_message, sen_query
from .functions import user_func
