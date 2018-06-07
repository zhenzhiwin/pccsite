



def processUrl(url):
    e_host = None
    e_url = None
    h_port = None

    url = url.replace("http://", "").replace("https://", "")
    if url[-2]+url[-1] == "/*":
        if url[-2]+url[-1] == "/*" and url.count("/*") == 1:
            url = url.replace("/*","")
            e_url = "/*"
            e_host = url
            if "/" in url:
                e_url = url[url.find("/"):len(url)] + e_url
                e_host = url[0:url.find("/")]
            if ":" in e_host:
                h_port = e_host.split(":")[1]
                e_host = e_host.split(":")[0]
        elif url[-2]+url[-1] == "/*" and url.count("/*") > 1:
            url = url[0:-2]
            e_url = "/*"
            if "/" in url:
                e_url = url[url.find("/"):len(url)] + e_url
                e_host = url[0:url.find("/")]
            if ":" in e_host:
                h_port = e_host.split(":")[1]
                e_host = e_host.split(":")[0]

    if ":*" in url:
        if "/" in url:
            e_url = url[url.find("/"):len(url)]
            e_host = url[0:url.find("/")]
        else:
            e_host = url

    if ":*" not in url and url[-2]+url[-1] == "/*":
        e_host = url
        if "/" in url:
            e_url = url[url.find("/"):len(url)]
            e_host = url[0:url.find("/")]
        if ":" in e_host:
            h_port = e_host.split(":")[1]
            e_host = e_host.split(":")[0]

    if e_host != None:
        if e_host[0]!= "*":
            e_host = "^" + e_host
        if e_host[-1] != "*":
            e_host = e_host + "$"
    if e_url!= None:
        if e_url[0]!= "*":
            e_url = "^" + e_url
        if e_url[-1] != "*":
            e_url = e_url + "$"

    return e_host,e_url,h_port
    #print("processUrl:+++", url)



