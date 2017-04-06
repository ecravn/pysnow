# -*- coding: utf-8 -*-

import requests
from pysnow import request
from pysnow.exceptions import InvalidUsage


class Client(object):
    def __init__(self, instance, user, password, raise_on_empty=True, default_payload=None):
        """Sets configuration and creates a session object used in `Request` later on

        :param instance: instance name, used to resolve FQDN in `Request`
        :param user: username
        :param password: password
        :param raise_on_empty: whether or not to raise an exception on 404 (no matching records)
        :param default_payload: default payload to send with all requests, set i.e. 'sysparm_limit' here
        """
        # Connection properties
        self.instance = instance
        self._user = user
        self._password = password
        self.raise_on_empty = raise_on_empty
        self.default_payload = default_payload or dict()

        # Sets default payload for all requests, i.e. sysparm_limit, sysparm_offset etc
        if not isinstance(self.default_payload, dict):
            raise InvalidUsage("Payload must be of type dict")

        # Create new session object
        self.session = self._create_session()

    def _create_session(self):
        """Creates and returns a new session object with the credentials passed to the constructor

        :return: session object
        """
        s = requests.Session()
        s.auth = requests.auth.HTTPBasicAuth(self._user, self._password)
        s.headers.update({'content-type': 'application/json', 'accept': 'application/json'})
        return s

    def _request(self, method, table, **kwargs):
        """Creates and returns a new `Request` object, takes some basic settings from the `Client` object and
        passes along to the `Request` constructor

        :param method: HTTP method
        :param table: Table to operate on
        :param kwargs: Keyword arguments passed along to `Request`
        :return: `Request` object
        """
        return request.Request(method,
                       table,
                       default_payload=self.default_payload,
                       raise_on_empty=self.raise_on_empty,
                       session=self.session,
                       instance=self.instance,
                       **kwargs)

    def query(self, table, **kwargs):
        """Query wrapper method.

        :param table: table to perform query on
        :param kwargs: Keyword arguments passed along to `Request`
        :return: `Request` object
        """
        return self._request('GET', table, **kwargs)

    def insert(self, table, payload, **kwargs):
        """Creates a new `Request` object and calls insert()

        :param table: table to insert on
        :param payload: update payload (dict)
        :param kwargs: Keyword arguments passed along to `Request`
        :return: New record content
        """
        r = self._request('POST', table, **kwargs)
        return r.insert(payload)

