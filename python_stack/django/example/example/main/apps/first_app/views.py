from django.shortcuts import render, HTTpResponse

def index(request):
    response = "Hello, I am your first request!"
    return HTTpResponse(response)
