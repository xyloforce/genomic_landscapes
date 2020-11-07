## some functions who can't go anywhere else

def get_request(baseURL, payload):
    """
    function to make a correct request
    """
    retry = True
    while retry:  # RETRY UNTIL SUCCES U SONOFAGUN
        time.sleep(1)
        try:
            # request add to the baseURL the params passed as dict
            request = requests.get(baseURL, params=payload)
        except (requests.ConnectionError, requests.HTTPError, requests.Timeout):
            print("Error : connection failed. Retrying...")
        else:
            retry = False
    print("Requested " + request.url)
    return request


def get_data(baseURL, payload):
    retry = True
    while retry:  # RETRY UNTIL SUCCES U SONOFAGUN
        try:
            request = get_request(baseURL, payload)
            data = request.json()["data"]
        except (ValueError, simplejson.errors.JSONDecodeError):
            print("Error : JSON invalid. Retrying...")
        else:
            retry = False
    return data

def get_xml(baseURL, payload):
    retry = True
    while retry:  # RETRY UNTIL SUCCES U SONOFAGUN
        try:
            request = get_request(baseURL, payload)
            data = xml.etree.ElementTree.parse(request.text())
        except (ValueError, simplejson.errors.JSONDecodeError):
            print("Error : XML invalid. Retrying...")
        else:
            retry = False
    return data

def query_xpath(xml, xpath):
    return xml.tree.findall(xpath)
