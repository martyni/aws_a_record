'''
Tests for aws_a_record CLI app
'''
from unittest.mock import MagicMock, patch
import pytest
from aws_a_record.app import get_zone_id, upsert_a_record, parse_args, main


MOCK_ZONE_ID = 'Z1234567890ABC'
MOCK_CHANGE_RESPONSE = {
    'ChangeInfo': {
        'Id': '/change/C1234567890',
        'Status': 'PENDING',
        'SubmittedAt': '2024-01-01T00:00:00Z',
    }
}


def _mock_route53_client(zone_name='example.com.', zone_id=MOCK_ZONE_ID):
    '''Build a mock Route53 client'''
    client = MagicMock()
    paginator = MagicMock()
    paginator.paginate.return_value = [
        {
            'HostedZones': [
                {'Name': zone_name, 'Id': f'/hostedzone/{zone_id}'}
            ]
        }
    ]
    client.get_paginator.return_value = paginator
    client.change_resource_record_sets.return_value = MOCK_CHANGE_RESPONSE
    return client


def test_get_zone_id_with_dot():
    '''get_zone_id returns the correct zone ID when name already has trailing dot'''
    client = _mock_route53_client()
    assert get_zone_id(client, 'example.com.') == MOCK_ZONE_ID


def test_get_zone_id_without_dot():
    '''get_zone_id appends a trailing dot if missing'''
    client = _mock_route53_client()
    assert get_zone_id(client, 'example.com') == MOCK_ZONE_ID


def test_get_zone_id_not_found():
    '''get_zone_id raises ValueError when zone is not found'''
    client = _mock_route53_client(zone_name='other.com.')
    with pytest.raises(ValueError, match='Hosted zone not found'):
        get_zone_id(client, 'example.com')


def test_upsert_a_record():
    '''upsert_a_record calls change_resource_record_sets with correct parameters'''
    client = _mock_route53_client()
    response = upsert_a_record(
        zone_id=MOCK_ZONE_ID,
        name='www.example.com',
        values=['1.2.3.4'],
        action='UPSERT',
        client=client,
    )
    assert response == MOCK_CHANGE_RESPONSE
    client.change_resource_record_sets.assert_called_once_with(
        HostedZoneId=MOCK_ZONE_ID,
        ChangeBatch={
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': 'www.example.com.',
                        'Type': 'A',
                        'TTL': 300,
                        'ResourceRecords': [{'Value': '1.2.3.4'}],
                    },
                }
            ]
        },
    )


def test_upsert_a_record_multiple_values():
    '''upsert_a_record handles multiple IP values'''
    client = _mock_route53_client()
    upsert_a_record(
        zone_id=MOCK_ZONE_ID,
        name='www.example.com',
        values=['1.2.3.4', '5.6.7.8'],
        client=client,
    )
    args = client.change_resource_record_sets.call_args[1]
    records = args['ChangeBatch']['Changes'][0]['ResourceRecordSet']['ResourceRecords']
    assert records == [{'Value': '1.2.3.4'}, {'Value': '5.6.7.8'}]


def test_parse_args_zone_id():
    '''parse_args parses --zone-id correctly'''
    args = parse_args(['--zone-id', MOCK_ZONE_ID, '--name',
                      'www.example.com', '--value', '1.2.3.4'])
    assert args.zone_id == MOCK_ZONE_ID
    assert args.name == 'www.example.com'
    assert args.value == ['1.2.3.4']
    assert args.ttl == 300
    assert args.action == 'UPSERT'


def test_parse_args_zone_name():
    '''parse_args parses --zone-name correctly'''
    args = parse_args(['--zone-name', 'example.com', '--name',
                      'api.example.com', '--value', '10.0.0.1'])
    assert args.zone_name == 'example.com'


def test_parse_args_ttl_and_action():
    '''parse_args handles custom ttl and action'''
    args = parse_args([
        '--zone-id', MOCK_ZONE_ID,
        '--name', 'test.example.com',
        '--value', '1.1.1.1',
        '--ttl', '60',
        '--action', 'CREATE',
    ])
    assert args.ttl == 60
    assert args.action == 'CREATE'


def test_main_with_zone_id(capsys):
    '''main() calls upsert_a_record and prints success message'''
    with patch('aws_a_record.app.boto3') as mock_boto3:
        mock_client = _mock_route53_client()
        mock_boto3.client.return_value = mock_client
        main(['--zone-id', MOCK_ZONE_ID, '--name',
             'www.example.com', '--value', '1.2.3.4'])
    captured = capsys.readouterr()
    assert 'Success' in captured.out
    assert 'UPSERT' in captured.out


def test_main_with_zone_name(capsys):
    '''main() resolves zone name to ID before upserting'''
    with patch('aws_a_record.app.boto3') as mock_boto3:
        mock_client = _mock_route53_client()
        mock_boto3.client.return_value = mock_client
        main(['--zone-name', 'example.com', '--name',
             'www.example.com', '--value', '1.2.3.4'])
    captured = capsys.readouterr()
    assert 'Success' in captured.out
