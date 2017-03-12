import os
import urllib
import requests

class ECFSClient(object):
    def __init__(self, **kwargs):
        self._apiKey = kwargs.get('apiKey')
        self._baseUrl = kwargs.get('baseUrl', 'https://publicapi.fcc.gov/ecfs')

    def get(self, path, params={}, decodeUrl=False):
        params['api_key'] = self._apiKey
        url = self._baseUrl + path
        preparedRequest = self._preparedRequest('GET', url, params, decodeUrl)
        session = requests.Session()
        response = session.send(preparedRequest)
        return response

    def getFilingsByProceeding(self, proceeding, **kwargs):
        params = self._getFilingsByProceedingParams(proceeding, **kwargs)
        path = '/filings'
        response = self.get(path, params=params, decodeUrl=True)
        return response

    # private methods
    def _preparedRequest(self, method, url, params, decodeUrl):
        request = requests.Request(method, url, params=params)
        preparedRequest = request.prepare()
        if decodeUrl:
            preparedRequest.url = urllib.parse.unquote(preparedRequest.url)
        return preparedRequest

    def _getFilingsByProceedingParams(self, proceeding, **kwargs):
        limit = kwargs.get('limit', 25)
        params = {
            'limit': limit,
            'q': '(proceedings.name:(({}*))+OR+proceedings.description:(({}*)))'.format(proceeding, proceeding),
            'sort': 'date_disseminated,DESC',
        }
        offset = kwargs.get('offset', None)
        if offset is not None:
            params['offset'] = offset

        return params
