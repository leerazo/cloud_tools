#!/usr/local/bin/python3

import boto3

ec2 = boto3.resource('ec2')

for i in ec2.instances.all():
    print(i, i.state['Name'])
    if i.state['Name'] == 'stopped':
        print('Instance', i, 'is in state:', i.state['Name'])
        print('Starting instance', i)
        i.start()
        print('Instance starting.')





