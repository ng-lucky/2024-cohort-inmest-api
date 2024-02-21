from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views import View

# Create your views here.

def json_response(request):
    return JsonResponse({"name": "Lucky"})

def http_response(request):
    return HttpResponse("<h1>Hello world!</h1>")

def say_hello(req):
    return HttpResponse("<h1>Hello Fleur</h1>")

# name: your name, email: your email, phone_number: your phone number


def user_profile(request):
    user_detail = {
        "name": "Lucky",
        "email": "lucky@email.com",
        "phone_number": "0445566777"
    }
    return JsonResponse(user_detail)

# 1. write a view function called filter_queries
# 1a. The view fuction should receive query_id through the url
# 1b. Return a JsonResponse data with the following 
# data: id, title, desicription, status, and submitted_by
# 1c. the id should be the id received through the url

def filter_queries(request, query_id):
    query = {
        "id": query_id,
        "title": "Adama wants to take mental health break",
        "description": "My girlfriend gave me broken heart",
        "status": "DECLINED",
        "submitted_by": "Adama"
    }
    return JsonResponse(query)


class QueryView(View):
    queries = [
            {"id": 1, "title": "Adama declined Val shots"},
            {"id": 2, "title": "Samson declined Val shots"}
        ]
    def get(self, request):
        
        return JsonResponse({"result": self.queries})
    
    def post(self, request):
        return JsonResponse({"status": "ok"})
    

