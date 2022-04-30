#!/usr/local/bin/python3

import os
import sys

library_dir = '/Users/lrazo/Dropbox/IT/repo/archive_tools/library'
sys.path.append(library_dir)
import boto3

s3 = boto3.resource('s3')

s3_client = boto3.client('s3')

def bucket_exists(bucket_name):
    try:
        s3.meta.client.head_bucket(Bucket=bucket_name)
        exists=True
    except:
        exists=False

    return exists

def list_buckets():
     buckets = list(s3.buckets.all())
     for index, bucket in enumerate(buckets):
         print(index+1, ':', bucket)
     return buckets

def create_bucket(bucket_name, region=None):
    print('Creating bucket name:', bucket_name)

    name = bucket_name
    region = 'eu-west-1'

    if True: ##### TEMP, replace with a 'try' statement later
        if region:
            print('REGION:', region)
            bucket = s3.create_bucket(
                Bucket=name,
                CreateBucketConfiguration={
                    'LocationConstraint': region
                }
            )
        else:
            print('REGION:', region)
            bucket = s3.create_bucket(Bucket=name)

        bucket.wait_until_exists()

    return bucket
     
def delete_bucket(bucket_name):
    buckets=list(s3.buckets.all())
    print('S3 buckets:')
    for bucket in buckets:
        print('\t', bucket.name)
        if bucket.name == bucket_name:
            delete_me = bucket
    delete_me.delete()
    delete_me.wait_until_not_exists()
    print('Bucket %s successfully deleted.' % delete_me.name) 

def get_bucket(bucket_name):
    buckets=list(s3.buckets.all())
    for bucket in buckets:
        if bucket.name == bucket_name:
            return bucket

def put_object(bucket, object_key, data):

    put_data = open(data, 'rb')
    obj = bucket.Object(object_key)
    obj.put(Body=put_data)
    obj.wait_until_exists()
    
def delete_object(bucket, object_key):

    print('BUCKET:', bucket)
    print('OBJECT KEY:', object_key)
   
    obj = bucket.Object(object_key)
    obj.delete()
    obj.wait_until_not_exists()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', help="Bucket name")
    parser.add_argument('-d', '--dir', '--directory', nargs='*', help="Local directory name")
    parser.add_argument('-o', '--object', help="Object name")
    parser.add_argument('-a', '--action', help="Action to take e.g. create, destroy, etc")
    parser.add_argument('--list', action='store_true', help="List all buckets")
    parser.add_argument('--create', action='store_true', help="Create new bucket")
    parser.add_argument('--backup', action='store_true', help="Backup all objects in a directory to a bucket")
    parser.add_argument('--delete', action='store_true', help="Delete bucket")
    parser.add_argument('--exists', action='store_true', help="Check if named bucket exists")
    parser.add_argument('--put-obj', action='store_true', help="Put object in designated bucket")
    parser.add_argument('--del-obj', action='store_true', help="Delete object from designated bucket")
    parser.add_argument('--debug', action='store_true', help="Print debug info")
    args = parser.parse_args()

    bucket_name = args.name

    if args.list:
        buckets = list_buckets()

    if args.exists:
        if bucket_exists(bucket_name):
            print('Bucket %s exists.' % bucket_name)
        else:
            print('Bucket %s does not exist.' % bucket_name)
      
    if args.create:
        new_bucket = create_bucket(bucket_name)
        print('New bucket:', new_bucket)

    if args.delete:
        delete_bucket(bucket_name)

    if args.put_obj:
        if args.object:
            data = args.object
        else:
            data = __file__

        #object_key = 'test_folder/' + os.path.split(data)[-1]
        object_key = os.path.split(data)[-1]

        print('data:', data)
        print('object_key:', object_key)

        bucket = get_bucket(bucket_name)

        put_object(bucket, object_key, data)

    if args.del_obj:
        bucket = get_bucket(bucket_name)
        if args.object:
            object_name = args.object
        else:
            object_name = None
            print('Must specify object name to delete')
            exit()

        if object_name:
            delete_object(bucket, object_name)

    if args.backup:
        bucket = get_bucket(bucket_name)
        dir_list = []
        if args.dir:
            dir_list = args.dir
        else:
            print('Must specify local directory to backup. Exiting.')
            exit()

        file_list = []
        print('Scanning...')
        for dir_item in dir_list:
            print('Checking dir_item:', dir_item)
            if os.path.isfile(dir_item):
                file_list.append(os.path.abspath(dir_item))
            elif os.path.isdir(dir_item):
                for dirname, subdirs, filelist in os.walk(dir_item):
                    for filename in filelist:
                        file_list.append(os.path.join(dirname, filename))

            for file in file_list:
                print('Archiving:', str(file) + '...')
                object_key = os.path.relpath(file, dir_item)
                #print('\tOBJECT KEY:', object_key)
                put_object(bucket, object_key, file)

#                s3_client.upload_file(
#                    Filename = file, 
#                    Bucket = bucket, 
#                    Key = object_key,
#                    ExtraArgs = {
#                      'StorageClass': 'STANDARD_IA'
#                    }
#                )
