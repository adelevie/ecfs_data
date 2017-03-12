import os
from app.ecfs_client import ECFSClient
import requests
import responses

def apiKey():
    return os.environ.get('DATA_API_KEY')

def test_init():
    client = ECFSClient(apiKey='fakeApiKey')

@responses.activate
def test_get():
    mockResponseBody = open('test/fixtures/filings.json').read()

    responses.add(responses.GET,
                  'https://publicapi.fcc.gov/ecfs/filings',
                  body=mockResponseBody,
                  status=200,
                  content_type='application/json')

    client = ECFSClient(apiKey=apiKey())
    response = client.get('/filings')

    assert response.ok

@responses.activate
def test_getFilingsByProceeding():
    mockResponseBody = open('test/fixtures/filings-12-375.json').read()

    responses.add(responses.GET,
                  'https://publicapi.fcc.gov/ecfs/filings',
                  body=mockResponseBody,
                  status=200,
                  content_type='application/json')

    client = ECFSClient(apiKey=apiKey())

    response = client.getFilingsByProceeding('12-375')
    assert response.ok

    filings = response.json()['filings']
    for filing in filings:
        proceedingNames = []
        for proceeding in filing['proceedings']:
            proceedingNames.append(proceeding['name'])

        assert '12-375' in proceedingNames
