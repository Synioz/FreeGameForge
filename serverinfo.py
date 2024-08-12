import requests as r
def Info():
    global checker
    serverinfo = r.get("https://fitgirl-repacks.site/")
    if serverinfo.status_code == 200:
        checker = 1
        return "\n[+] Server is Online. [+]\n"
    else:
        checker = 0
        return f"\n[-] Server is Offline. Error Code: {serverinfo.status_code} [-]\n"
print(Info())