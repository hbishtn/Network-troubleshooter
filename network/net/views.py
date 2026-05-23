from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse
from reportlab.pdfgen import canvas

from .ai_engine import analyze_network_problem
from .models import NetworkIssue
from .network_tools import (
    auto_fix,
    ping_test,
    dns_check,
    internet_speed,
    extract_ping_value,
    analyze_network_condition,
    scan_devices,
)

def home(request):
    response = ""

    if request.method == "POST":
        problem = request.POST.get("problem", "").strip()

        if not problem:
            response = "Please enter a network problem or question."
        else:
            problem_lower = problem.lower()

            network_keywords = [
                "slow",
                "not working",
                "disconnect",
                "high ping",
                "dns",
                "internet issue",
                "wifi",
                "network",
                "health",
                "report",
                "latency",
                "connection",
                "ping",
                "gaming",
                "game",
                "latency",
                "packet loss",
                "network health",   
                "internet",

            ]

            is_network_issue = any(
                word in problem_lower for word in network_keywords
            )

            if is_network_issue:
                ping = ping_test()
                ping_value = extract_ping_value(ping)
                dns = dns_check()
                analysis = analyze_network_condition(ping, dns, ping_value)
                fix = auto_fix(analysis["issue"])

                if "slow" in problem_lower:
                    speed = internet_speed()
                else:
                    speed = "Not required"

                response = analyze_network_problem(
                    problem,
                    analysis["issue"],
                    analysis["rating"],
                    analysis["recommendation"],
                    fix,
                )
            else:
                response = "Please ask a network-related question."

            if request.user.is_authenticated:
                NetworkIssue.objects.create(
                    user=request.user,
                    problem=problem,
                    response=response,
                )
    devices = scan_devices()
    return render(request, "home.html", {
        "response": response,
        "devices": devices
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
# for sign-up
def signup_view(request):

    if request.method == "POST":

        username = request.POST.get("username")

        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():

            return render(request, "signup.html", {
                "error": "Username already exists"
            })

        user = User.objects.create_user(
            username=username,
            password=password
        )

        login(request, user)

        return redirect("home")

    return render(request, "signup.html")
# for log-in
def login_view(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:
            login(request, user)
            return redirect("home")

        error = "Invalid username or password."

    return render(request, "login.html", {"error": error})

# for log-out
def logout_view(request):

    logout(request)

    return redirect("login")

#check user history of problems and solutions
@login_required
def history_view(request):
    issues = NetworkIssue.objects.filter(user=request.user)
    return render(request, "history.html", {"issues": issues})

def live_status(request):

    ping = ping_test()

    dns = dns_check()

    ping_value = extract_ping_value(ping)

    return JsonResponse({

        "ping": ping,

        "dns": dns,

        "ping_value": ping_value

    })

# for download report as PDF

def download_report(request):

    text = request.GET.get("text", "No Report")

    response = HttpResponse(
        content_type="application/pdf"
    )

    response[
        "Content-Disposition"
    ] = 'attachment; filename="report.pdf"'

    p = canvas.Canvas(response)

    p.drawString(
        100,
        800,
        "AI Network Troubleshooter Report"
    )

    y = 760

    for line in text.split("\n"):

        p.drawString(100, y, line)

        y -= 20

    p.save()

    return response

def more(request):
    return render(request, "more.html")