#!/usr/local/bin/python3

import os
import google.cloud
from google.oauth2 import service_account
from google.cloud import storage

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )

def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The ID of your GCS object
    # source_blob_name = "storage-object-name"

    # The path to which the file should be downloaded
    # destination_file_name = "local/path/to/file"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    # Construct a client side representation of a blob.
    # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
    # any content from Google Cloud Storage. As we don't need additional data,
    # using `Bucket.blob` is preferred here.
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print(
        "Downloaded storage object {} from bucket {} to local file {}.".format(
            source_blob_name, bucket_name, destination_file_name
        )
    )

def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    # bucket_name = "your-bucket-name"
    # blob_name = "your-object-name"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()

    print("Blob {} deleted.".format(blob_name))


def rename_blob(bucket_name, blob_name, new_name):
    """Renames a blob."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The ID of the GCS object to rename
    # blob_name = "your-object-name"
    # The new ID of the GCS object
    # new_name = "new-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    new_blob = bucket.rename_blob(blob, new_name)

    print("Blob {} has been renamed to {}".format(blob.name, new_blob.name))


def copy_blob(
    bucket_name, blob_name, destination_bucket_name, destination_blob_name
):
    """Copies a blob from one bucket to another with a new name."""
    # bucket_name = "your-bucket-name"
    # blob_name = "your-object-name"
    # destination_bucket_name = "destination-bucket-name"
    # destination_blob_name = "destination-object-name"

    storage_client = storage.Client()

    source_bucket = storage_client.bucket(bucket_name)
    source_blob = source_bucket.blob(blob_name)
    destination_bucket = storage_client.bucket(destination_bucket_name)

    blob_copy = source_bucket.copy_blob(
        source_blob, destination_bucket, destination_blob_name
    )

    print(
        "Blob {} in bucket {} copied to blob {} in bucket {}.".format(
            source_blob.name,
            source_bucket.name,
            blob_copy.name,
            destination_bucket.name,
        )
    )


def move_blob(bucket_name, blob_name, destination_bucket_name, destination_blob_name):
    """Moves a blob from one bucket to another with a new name."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The ID of your GCS object
    # blob_name = "your-object-name"
    # The ID of the bucket to move the object to
    # destination_bucket_name = "destination-bucket-name"
    # The ID of your new GCS object (optional)
    # destination_blob_name = "destination-object-name"

    storage_client = storage.Client()

    source_bucket = storage_client.bucket(bucket_name)
    source_blob = source_bucket.blob(blob_name)
    destination_bucket = storage_client.bucket(destination_bucket_name)

    blob_copy = source_bucket.copy_blob(
        source_blob, destination_bucket, destination_blob_name
    )
    source_bucket.delete_blob(blob_name)

    print(
        "Blob {} in bucket {} moved to blob {} in bucket {}.".format(
            source_blob.name,
            source_bucket.name,
            blob_copy.name,
            destination_bucket.name,
        )
    )


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--upload", metavar="object_name", help="Upload object")
    parser.add_argument("-d", "--download", metavar="object_name", help="Download object")
    parser.add_argument("-r", "--rename", metavar="object_name", help="Rename object")
    parser.add_argument("-n", "--newname", metavar="object_name", help="New name for object")
    parser.add_argument("-c", "--copy", metavar="object_name", help="Copy object")
    parser.add_argument("-m", "--move", metavar="object_name", help="Move object")
    parser.add_argument("--dest", metavar="bucket_name", help="Destination bucket")
    parser.add_argument("--delete", metavar="object_name", help="Delete object")
    parser.add_argument("-b", "--bucket", metavar="bucket_name", help="Bucket name")
    args = parser.parse_args()

    if args.upload and args.bucket:
        source_file_name = args.upload
        bucket_name = args.bucket
        if args.newname:
            destination_blob_name = args.newname
        else:
            destination_blob_name = args.upload
        upload_blob(bucket_name, source_file_name, destination_blob_name)

    if args.download and args.bucket:
        source_blob_name = args.download
        destination_file_name = args.download
        bucket_name = args.bucket
        download_blob(bucket_name, source_blob_name, destination_file_name)

    if args.delete and args.bucket:
        blob_name = args.delete
        bucket_name = args.bucket
        delete_blob(bucket_name, blob_name)

    if args.rename and args.bucket:
        bucket_name = args.bucket
        blob_name = args.rename
        if args.newname:
            new_blob_name = args.newname
        else:
            new_blob_name = input("Enter new name for object: ")

        rename_blob(bucket_name, blob_name, new_blob_name)

    if args.copy and args.bucket:
        bucket_name = args.bucket
        blob_name = args.copy

        print('bucket_name:', bucket_name)
        print('blob_name:', blob_name)

        if args.dest:
            destination_bucket_name = args.dest
        else:
            destination_bucket_name = args.bucket

        print('destination_bucket_name:', destination_bucket_name)

        if args.newname:
            destination_blob_name = args.newname
            print('destination_blob_name:', destination_blob_name)
        elif bucket_name == destination_bucket_name:
            print('Source object and destination object are identical')
            exit()
        else:
            destination_blob_name = blob_name
            print('destination_blob_name:', destination_blob_name)

        copy_blob(bucket_name, blob_name, destination_bucket_name, destination_blob_name)
