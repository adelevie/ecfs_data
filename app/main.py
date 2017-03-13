import os
from ecfs_client import ECFSClient
from IPython import embed

client = ECFSClient(apiKey=os.getenv('DATA_API_KEY'))

response = client.getAllFilingsByProceeding('12-375')
