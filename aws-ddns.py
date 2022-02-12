#!/usr/bin/env python3

import requests
import boto3
import argparse

def get_aws_record_ip(hosted_zone_id, record_name):
    aws_records = boto3.client('route53').list_resource_record_sets(HostedZoneId=hosted_zone_id)

    for record in aws_records['ResourceRecordSets']:
        if record['Name'] == record_name:
            aws_record_ip = record['ResourceRecords'][0]['Value']
            return(aws_record_ip)
    raise SystemExit(f"Unable to find record {repr(record_name)} in hosted zone {hosted_zone_id}")

parser = argparse.ArgumentParser(description="AWS DDNS record updater")
parser.add_argument('-r', '--record',  metavar='record_name', required=True, help="AWS record name")
parser.add_argument('-z', '--hosted-zone-id', metavar='hosted_zone_id', required=True, help="AWS hosted zone id")
args = parser.parse_args()

record_name = args.record
hosted_zone_id = args.hosted_zone_id

r = requests.get('https://checkip.amazonaws.com')
if r.status_code != 200:
    raise SystemExit("Unable to retrieve public IP")
public_ip = r.text.strip('\n')

change_batch = {
    'Comment': f'{record_name} DDNS record update',
    'Changes': [
        {
            'Action': 'UPSERT',
            'ResourceRecordSet': {
                'Name': record_name,
                'Type': 'A',
                'TTL': 300,
                'ResourceRecords': [
                    {
                        'Value': public_ip
                    }
                ]
            }
        }
    ]
}

aws_record_ip = get_aws_record_ip(hosted_zone_id, record_name)
if aws_record_ip != public_ip:
    print(f"{repr(record_name)} record IP ({aws_record_ip}) and public IP ({public_ip}) do not match, updating...")
    boto3.client('route53').change_resource_record_sets(HostedZoneId=hosted_zone_id, ChangeBatch=change_batch)

    aws_record_ip = get_aws_record_ip(hosted_zone_id, record_name)
    if aws_record_ip == public_ip:
        print(f"{repr(record_name)} successfully updated to {aws_record_ip}")
    else:
        raise SystemExit("Record update failed")
