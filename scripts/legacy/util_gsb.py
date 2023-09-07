import requests
# from sensitive import GSBAPIKEY


API_MAX_URLS = 500
GSBAPIKEY = 'AIzaSyAbNQV-jcTcLbcd80W2-Gur5-RzPIWLN1I'

ANY_PLATFORM = ["ANY_PLATFORM"]
ANDROID_PLATFORM = ["ANDROID", "IOS"]


def check_urls(url_or_list, platform=ANY_PLATFORM):
    """
    Checks URLs against the Google Safe Browsing v4 lookup API
    :param url_or_list: single URL or list of up to API_MAX_URLS URLs
    :param platform:
    :return list of phishing URLs detected, list of malware URLs detected:
    """

    if not isinstance(url_or_list, list):
        url_or_list = [url_or_list]

    if len(url_or_list) > API_MAX_URLS:

        raise RuntimeError("Too many URLs supplied to GSB API")

    detected_phishing = []
    detected_malware = []

    if len(url_or_list) > 0:

        url = 'https://safebrowsing.googleapis.com/v4/threatMatches:find'
        payload = {'client': {'clientId': "research2", 'clientVersion': "0.1"},
                   'threatInfo': {'threatTypes': ["SOCIAL_ENGINEERING", "MALWARE"],
                                  'platformTypes': platform,
                                  'threatEntryTypes': ["URL"],
                                  'threatEntries': [{'url': url} for url in url_or_list]}}

        try:

            params = {'key': GSBAPIKEY}
            r = requests.post(url, params=params, json=payload)
            response = r.json()
            print(response)

            for threat in response.setdefault('matches', []):

                try:

                    if threat['threatType'] == 'SOCIAL_ENGINEERING':

                        detected_phishing.append(threat['threat']['url'])

                    elif threat['threatType'] == 'MALWARE':

                        detected_malware.append(threat['threat']['url'])

                except:

                    print('GSB response not understood ' + str(threat))

        except Exception as e:

            print('Error returned by GSB API')
            print(e)

    return detected_phishing, detected_malware


def check_urls_update(url_or_list, do_update=True):
    """
    Checks urls against the GSB update API
    :param url_or_list:
    :param do_update: refresh the local DB?
    :return: list of urls detected
    """

    from gglsbl import SafeBrowsingList

    sbl = SafeBrowsingList(GSBAPIKEY)

    if do_update:

        sbl.update_hash_prefix_cache()

    if not isinstance(url_or_list, list):
        url_or_list = [url_or_list]

    malicious = []

    for url in url_or_list:

        try:
            threat_list = sbl.lookup_url(url)

            if threat_list is not None:
                malicious.append(url)

        except:

            print("GSB update lookup: Invalid URL %s" % url)

    return malicious


if __name__ == '__main__':
    phishing, mal = check_urls('https://www.kickassfilms.com/PayPal/869cb1/en/')
