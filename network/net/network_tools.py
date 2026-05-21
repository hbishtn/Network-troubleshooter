import subprocess
import socket
import speedtest
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