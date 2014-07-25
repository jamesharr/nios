#!/usr/bin/python
# coding: utf-8

"""Module docs.

"""
import getpass
import sys
import urllib
import urllib2
import base64
import json


def _get_method(rv):
    """Produce a lambda that returns the value passed in.

    This makes pyflakes happy.
    """
    def _lambda():
        return rv
    return _get_method


class NIOS (object):
    def __init__(self, nios_url, nios_username=None, nios_password=None):
        self.nios_url = nios_url
        self.nios_username = nios_username
        self.nios_password = nios_password

    def prompt_nios_credentials(self):
        nios_user = prompt_input("NIOS username", getpass.getuser())
        nios_pass = getpass.getpass()
        self.set_nios_credentials(nios_user, nios_pass)
        if not self.test_nios_credentials():
            print " - Login to NIOS failed"
        else:
            break

    def set_nios_credentials(self, username, password):
        self.nios_username = username
        self.nios_password = password

    def test_nios_credentials(self):
        try:
            self.get('record:host', _max_results=1)
        except urllib2.HTTPError, e:
            if e.getcode() == 401:
                return False
            else:
                raise e
        return True

    def get(self, obj, **params):
        default_params = {
            '_return_type': 'json-pretty'
        }
        full_params = dict()
        full_params.update(default_params)
        full_params.update(params)
        query_string = urllib.urlencode(full_params)

        request = urllib2.Request(self.nios_url + "wapi/v1.4/" + obj + "?" + query_string)
        request.get_method = _get_method("GET")
        # request.add_header('Content-Type', 'application/json')
        base64string = base64.standard_b64encode('%s:%s' % (self.nios_username, self.nios_password))
        request.add_header("Authorization", "Basic %s" % base64string)

        opener = urllib2.build_opener(urllib2.HTTPHandler)
        result = opener.open(request)
        json_text = result.read()

        return json.loads(json_text)


def prompt_input(prompt, default=""):
    if default != "":
        prompt += " [%s]" % default
    print "%s:" % prompt,
    input = sys.stdin.readline()
    input = input.rstrip()
    if input == "":
        input = default
    return input
