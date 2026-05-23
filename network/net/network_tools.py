import subprocess
import socket
import speedtest
import re
import subprocess
import socket
#for ping test
def ping_test(host="google.com"):
    try:
        result = subprocess.run(
            ["ping", "-n", "2", host],
            capture_output=True,
            text=True
        )
        return result.stdout
    except Exception as e:
        return str(e)
    
#for dns check
def dns_check(domain="google.com"):
    try:
        ip = socket.gethostbyname(domain)
        return f"DNS OK: {domain} -> {ip}"
    except Exception as e:
        return f"DNS Error: {str(e)}"
    
#for internet speed test
def internet_speed():
    try:
        st = speedtest.Speedtest()
        download = st.download() / 1_000_000
        upload = st.upload() / 1_000_000

        return f"Download: {download:.2f} Mbps\nUpload: {upload:.2f} Mbps"
    except Exception as e:
        return str(e)
def extract_ping_value(ping_result):

    match = re.search(r"time[=<](\d+)", ping_result)

    if match:

        return int(match.group(1))

    return 0

def analyze_network_condition(
    ping,
    dns,
    ping_value
):

    issue = "Network Stable"

    rating = 10

    recommendation = "No major issue detected"

    if ping_value > 200:

        issue = "High Latency"

        rating = 5

        recommendation = (
            "Restart router and reduce "
            "background downloads"
        )

    elif ping_value > 100:

        issue = "Moderate Latency"

        rating = 7

        recommendation = (
            "Check WiFi signal strength"
        )

    if "DNS ERROR" in dns:

        issue = "DNS Failure"

        rating = 4

        recommendation = (
            "Change DNS to 8.8.8.8"
        )

    if "Lost = 100%" in ping:

        issue = "Internet Disconnected"

        rating = 1

        recommendation = (
            "Check router or ISP connection"
        )

    return {

        "issue": issue,

        "rating": rating,

        "recommendation": recommendation
    }

# for auto fix
def auto_fix(issue):

    fixes = {

        "High Latency":
        "Restart router and reduce background downloads.",

        "Moderate Latency":
        "Move closer to WiFi router.",

        "DNS Failure":
        "Change DNS to 8.8.8.8 and 1.1.1.1",

        "Internet Disconnected":
        "Restart router and check ISP connection.",

        "Network Stable":
        "No fix needed. Network is working properly."
    }

    return fixes.get(
        issue,
        "Basic troubleshooting required."
    )

# for device detaction and scanning  

def scan_devices():

    output = subprocess.check_output(
        "arp -a",
        shell=True
    ).decode()

    devices = []

    lines = output.splitlines()

    for line in lines:

        if "dynamic" in line:

            parts = line.split()

            ip = parts[0]

            mac = parts[1]

            try:

                hostname = socket.gethostbyaddr(ip)[0]

            except:

                hostname = "Unknown Device"

            devices.append({

                "ip": ip,

                "mac": mac,

                "hostname": hostname
            })

    return devices