from django.http import HttpResponse

def hello(request):
    return HttpResponse("Hello, world !")

class test_print():
    print("Hello, World ! From NewStyle Class")