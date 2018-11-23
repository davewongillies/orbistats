import base64
import urllib2
import re


def statistics(username, password):
    return get('RST_statistic', username, password)


def connection_status(username, password):
    return get('RST_conn_status', username, password)


def get(url, username, password):
    request = urllib2.Request('http://orbilogin.com/{}.htm'.format(url))
    base64string = base64.encodestring('{}:{}'.format(username, password)).strip('\n')
    request.add_header("Authorization", "Basic {}".format(base64string))

    response = urllib2.urlopen(request)
    html = response.read()
    js_var_pattern = re.compile(
        r'^var (?P<name>[A-Za-z_0-9]+?)\s*?="?(?P<value>.*?)"?;$',
        flags=re.MULTILINE | re.UNICODE)
    matches = re.findall(js_var_pattern, html)

    response.close()

    return {k: v for k, v in matches}
