import os
import urllib
import requests
from IPython import embed

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

    def getAllFilingsByProceeding(self, proceeding, **kwargs):
        firstResponse = self.getFilingsByProceeding(proceeding, **kwargs)
        firstFilings = firstResponse.json()['filings']
        resultsCount = self._getResultsCountFromResponse(firstResponse, proceeding)
        if resultsCount < len(firstFilings):
            pass
        else:
            return firstFilings

    # private methods
    def _getResultsCountFromResponse(self, response, proceeding):
        aggregations = response.json()['aggregations']
        proceedingInfo = aggregations['proceedings_name']
        buckets = proceedingInfo['buckets']
        resultsCount = list(filter(lambda x: x['key'] == proceeding, buckets))[0]['doc_count']
        return resultsCount


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
