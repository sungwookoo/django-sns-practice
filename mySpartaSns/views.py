from django.http import HttpResponse  # HttpResponse(str) : str 전달
from django.shortcuts import render


def base_response(request):
    return HttpResponse("안녕하세요! 장고의 시작입니다!")


def first_view(request):
    return render(request, 'my_test.html')
