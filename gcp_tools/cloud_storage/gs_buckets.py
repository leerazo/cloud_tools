#!/usr/local/bin/python3

import os
import google.cloud
from google.oauth2 import service_account
from google.cloud import storage

# If you don't specify credentials when constructing the client, the
# client library will look for credentials in the environment.


def create_bucket_class_location(bucket_name):
    """
    Create a new bucket in the US region with the coldline storage
    class
    """
    # bucket_name = "your-new-bucket-name"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    bucket.storage_class = "COLDLINE"
    new_bucket = storage_client.create_bucket(bucket, location="us")

    print(
        "Created bucket {} in {} with storage class {}".format(
            new_bucket.name, new_bucket.location, new_bucket.storage_class
        )
    )
    return new_bucket

def list_buckets():
    storage_client = storage.Client()
    buckets = list(storage_client.list_buckets())
    print(buckets)


def bucket_metadata(bucket_name):
    """Prints out a bucket's metadata."""
    # bucket_name = 'your-bucket-name'

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    print("")
    print(f"\tID: {bucket.id}")
    print(f"\tName: {bucket.name}")
    print(f"\tStorage Class: {bucket.storage_class}")
    print(f"\tLocation: {bucket.location}")
    print(f"\tLocation Type: {bucket.location_type}")
    print(f"\tCors: {bucket.cors}")
    print(f"\tDefault Event Based Hold: {bucket.default_event_based_hold}")
    print(f"\tDefault KMS Key Name: {bucket.default_kms_key_name}")
    print(f"\tMetageneration: {bucket.metageneration}")
    print(
        f"\tPublic Access Prevention: {bucket.iam_configuration.public_access_prevention}"
    )
    print(f"\tRetention Effective Time: {bucket.retention_policy_effective_time}")
    print(f"\tRetention Period: {bucket.retention_period}")
    print(f"\tRetention Policy Locked: {bucket.retention_policy_locked}")
    print(f"\tRequester Pays: {bucket.requester_pays}")
    print(f"\tSelf Link: {bucket.self_link}")
    print(f"\tTime Created: {bucket.time_created}")
    print(f"\tVersioning Enabled: {bucket.versioning_enabled}")
    print(f"\tLabels: {bucket.labels}")
    print("")

def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""
    # bucket_name = "your-bucket-name"

    storage_client = storage.Client()

    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name)

    for blob in blobs:
        print(blob.name)

def empty_bucket(bucket_name):
    """Deletes all the blobs in the bucket."""
    # bucket_name = "your-bucket-name"

    storage_client = storage.Client()
    bucket_exists = storage_client.lookup_bucket(bucket_name)

    if bucket_exists:
        confirm = input('Are you SURE you want to delete {} (CANNOT BE UNDONE)? '.format(bucket_name))
    else:
        print("Bucket {} doesn't exist.".format(bucket_name))
        exit()

    blobs = storage_client.list_blobs(bucket_name)

    blob_list = [blob.name for blob in storage_client.list_blobs(bucket_name)]
    blob_count = len(blob_list)

    if blob_count > 0:
        for blob in blobs:
            print('Deleting:', blob.name)
            blob.delete()
    else:
        print('Bucket {} is already empty.'.format(bucket_name))


def delete_bucket(bucket_name):
    """Deletes a bucket. The bucket must be empty."""
    # bucket_name = "your-bucket-name"

    storage_client = storage.Client()
    bucket_exists = storage_client.lookup_bucket(bucket_name)

    if bucket_exists:
        confirm = input('Are you SURE you want to delete {} (CANNOT BE UNDONE)? '.format(bucket_name))
    else:
        print("Bucket {} doesn't exist.".format(bucket_name))
        exit()

    bucket = storage_client.get_bucket(bucket_name)

    blob_count = len([blob.name for blob in storage_client.list_blobs(bucket_name)])
    #blob_count = len(blob_list)

    print('')
    print('\tblob_count:', blob_count)
    print('')

    if blob_count == 0:
        bucket.delete()
        print("Bucket {} deleted".format(bucket_name))
    else:
        print('Bucket is not empty. Please empty before deleting.')


def foce_delete_bucket(bucket_name):
    """Empties and then deletes a bucket."""
    # bucket_name = "your-bucket-name"

    storage_client = storage.Client()
    bucket_exists = storage_client.lookup_bucket(bucket_name)

    if bucket_exists:
        confirm = input('Are you SURE you want to delete {} (CANNOT BE UNDONE)? '.format(bucket_name))
    else:
        print("Bucket {} doesn't exist.".format(bucket_name))
        exit()

    bucket = storage_client.get_bucket(bucket_name)
    blobs = storage_client.list_blobs(bucket_name)

    for blob in blobs:
        print('Deleting:', blob.name)
        blob.delete()

    bucket.delete()

    print("Bucket {} emptied and force deleted".format(bucket_name))


def migrate_bucket(bucket_name, dest_bucket_name):
    """Deletes all the blobs in the bucket."""
    # bucket_name = "your-bucket-name"

    storage_client = storage.Client()
    source_bucket = storage_client.get_bucket(bucket_name)

    dest_exists = storage_client.lookup_bucket(dest_bucket_name)

    if dest_exists:
        print('dest_exists:', dest_exists)
    else:
        print("Destination bucket doesn't exist, creating.")
        create_bucket_class_location(dest_bucket_name)
    dest_bucket = storage_client.get_bucket(dest_bucket_name)

    blobs = storage_client.list_blobs(bucket_name)

    for blob in blobs:
        print('Copying:', blob.name)
        source_bucket.copy_blob(blob, dest_bucket, blob.name)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--create", metavar="bucket_name", help="Create bucket")
    parser.add_argument("-d", "--delete", metavar="bucket_name", help="Delete bucket")
    parser.add_argument("-i", "--info", metavar="bucket_name", help="Delete bucket")
    parser.add_argument("-l", "--list", metavar="bucket_name", help="List bucket contents")
    parser.add_argument("-m", "--migrate", metavar="bucket_name", help="Migrate bucket contents to another bucket")
    parser.add_argument("--dest", metavar="bucket_name", help="Destination bucket name")
    parser.add_argument("--empty", metavar="bucket_name", help="Empties bucket contents")
    parser.add_argument("--force-delete", metavar="bucket_name", help="Empties and permanently deletes bucket")
    parser.add_argument("-lb", "--list-buckets", action="store_true", help="List all buckets")
    args = parser.parse_args()

    if args.create:
        bucket_name = args.create
        print('Creating bucket:', bucket_name)
        create_bucket_class_location(bucket_name)
        list_buckets()

    if args.delete:
        bucket_name = args.delete
        print('Deleting bucket:', bucket_name)
        delete_bucket(bucket_name)
        list_buckets()

    if args.info:
        bucket_name = args.info
        print('Getting info for bucket:', bucket_name)
        bucket_metadata(bucket_name)

    if args.list:
        bucket_name = args.list
        print('Listing bucket contents:')
        list_blobs(bucket_name)

    if args.list_buckets:
        print('Listing buckets:')
        list_buckets()

    if args.empty:
        bucket_name = args.empty
        empty_bucket(bucket_name)

    if args.force_delete:
        bucket_name = args.force_delete
        confirm = input('Are you SURE you want to empty ' + bucket_name + ' (CANNOT BE UNDONE)? ')
        if confirm.casefold() == 'y':
            print('Emptying bucket contents:')
            empty_bucket(bucket_name)
            print('Deleting bucket:', bucket_name)
            delete_bucket(bucket_name)
            list_buckets()

    if args.migrate and args.dest:
        bucket_name = args.migrate
        dest_bucket_name = args.dest
        migrate_bucket(bucket_name, dest_bucket_name) 

