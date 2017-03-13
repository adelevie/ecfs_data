import os
from app.ecfs_client import ECFSClient
import requests
import responses
import mock
import json
from IPython import embed

def apiKey():
    return os.environ.get('DATA_API_KEY')

def test_init():
    client = ECFSClient(apiKey='fakeApiKey')




@mock.patch('app.ecfs_client.requests.Session.send')
def test_get(mockGet):
    expectedJson = json.loads(open('test/fixtures/filings.json').read())

    def mySideEffect(*args, **kwargs):
        mockResponse = mock.Mock()
        mockResponse.json.return_value = expectedJson
        return mockResponse

    mockGet.side_effect = mySideEffect

    client = ECFSClient(apiKey=apiKey())
    response = client.get('/filings')

    assert response.json() == expectedJson

@mock.patch('app.ecfs_client.requests.Session.send')
def test_getFilingsByProceeding(mockGet):
    expectedJson = json.loads(open('test/fixtures/filings-12-375.json').read())

    def mySideEffect(*args, **kwargs):
        mockResponse = mock.Mock()
        mockResponse.json.return_value = expectedJson
        mockResponse.ok = True
        return mockResponse

    mockGet.side_effect = mySideEffect

    client = ECFSClient(apiKey=apiKey())

    response = client.getFilingsByProceeding('12-375')

    assert response.ok

    filings = response.json()['filings']
    for filing in filings:
        proceedingNames = []
        for proceeding in filing['proceedings']:
            proceedingNames.append(proceeding['name'])

        assert '12-375' in proceedingNames

def test_getAllFilingsByProceeding():
    client = ECFSClient(apiKey=apiKey())

    filings = client.getFilingsByProceeding('12-375')
