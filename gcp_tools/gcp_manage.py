#!/usr/local/bin/python3

import os
import google.cloud
from google.oauth2 import service_account

print("Hello there")

# Imports the Google Cloud client library
from google.cloud import storage

# Instantiates a client
#storage_client = storage.Client()

# The name for the new bucket
bucket_name = "my-new-bucket"

# Creates the new bucket
#bucket = storage_client.create_bucket(bucket_name)

#print("Bucket {} created.".format(bucket.name))

print('')
print("bucket_name:", bucket_name)
print('')
print("os.environ['GOOGLE_APPLICATION_CREDENTIALS']:", os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
