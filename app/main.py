import os
from ecfs_client import ECFSClient

client = ECFSClient(apiKey=os.getenv('DATA_API_KEY'))

response = client.getFilingsByProceeding('12-375', limit=1000)

filings = response.json()['filings']

print(len(filings))
import pdb; pdb.set_trace()
