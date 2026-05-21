from django.shortcuts import render
from .ai_engine import analyze_network_problem
from .models import Problem
from .network_tools import ping_test, dns_check, internet_speed

def home(request):
    response = ""

    if request.method == "POST":
        problem = request.POST.get("problem")

        ping = ping_test()
        dns = dns_check()
        speed = internet_speed()

        response = analyze_network_problem(problem, ping, dns, speed)

    return render(request, "home.html", {
        "response": response
    })

    

def tools(request):

    ping = ping_test()
    dns = dns_check()
    speed = internet_speed()

    return render(request, "tools.html", {
        "ping": ping,
        "dns": dns,
        "speed": speed
    })   