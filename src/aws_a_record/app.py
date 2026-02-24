'''
boto3 CLI app for adding/updating Route53 A records
'''
import argparse
import boto3


def get_zone_id(client, zone_name):
    '''Look up a hosted zone ID by name'''
    if not zone_name.endswith('.'):
        zone_name += '.'
    paginator = client.get_paginator('list_hosted_zones')
    for page in paginator.paginate():
        for zone in page['HostedZones']:
            if zone['Name'] == zone_name:
                return zone['Id'].split('/')[-1]
    raise ValueError(f'Hosted zone not found: {zone_name}')


def upsert_a_record(
        zone_id,
        name,
        values,
        action='UPSERT',
        client=None):
    '''Create or update an A record in a Route53 hosted zone'''
    ttl = 300
    if client is None:
        client = boto3.client('route53')

    if not name.endswith('.'):
        name += '.'

    resource_records = [{'Value': v} for v in values]

    response = client.change_resource_record_sets(
        HostedZoneId=zone_id,
        ChangeBatch={
            'Changes': [
                {
                    'Action': action,
                    'ResourceRecordSet': {
                        'Name': name,
                        'Type': 'A',
                        'TTL': ttl,
                        'ResourceRecords': resource_records,
                    },
                }
            ]
        },
    )
    return response


def parse_args(argv=None):
    '''Parse command-line arguments'''
    parser = argparse.ArgumentParser(
        description='Add or update a Route53 A record using boto3'
    )
    zone_group = parser.add_mutually_exclusive_group(required=True)
    zone_group.add_argument('--zone-id', help='Route53 hosted zone ID')
    zone_group.add_argument('--zone-name', help='Route53 hosted zone name')
    parser.add_argument(
        '--name',
        required=True,
        help='DNS record name (e.g. www.example.com)')
    parser.add_argument(
        '--value',
        required=True,
        nargs='+',
        help='IP address(es) to set for the A record')
    parser.add_argument(
        '--ttl',
        type=int,
        default=300,
        help='TTL in seconds (default: 300)')
    parser.add_argument(
        '--action',
        choices=['CREATE', 'UPSERT', 'DELETE'],
        default='UPSERT',
        help='Change action (default: UPSERT)',
    )
    return parser.parse_args(argv)


def main(argv=None):
    '''Entry point for the aws_a_record CLI'''
    args = parse_args(argv)
    client = boto3.client('route53')

    zone_id = args.zone_id
    if zone_id is None:
        zone_id = get_zone_id(client, args.zone_name)

    response = upsert_a_record(
        zone_id=zone_id,
        name=args.name,
        values=args.value,
        action=args.action,
        client=client,
    )
    status = response['ChangeInfo']['Status']
    change_id = response['ChangeInfo']['Id']
    print(
        f'''Success: {args.action} A record "{args.name}" -> {args.value}
| Status: {status} | ChangeId: {change_id}''')
    return response


if __name__ == '__main__':
    main()
