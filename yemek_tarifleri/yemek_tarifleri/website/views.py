from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime



def welcome(request):
    return HttpResponse("Yemek Tarifleri Projesine Hoşgeldiniz!")
