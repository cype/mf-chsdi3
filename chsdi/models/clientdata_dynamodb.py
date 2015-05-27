# -*- coding: utf-8 -*-

import os
import ConfigParser
import pyramid.httpexceptions as exc

from boto.dynamodb import connect_to_region
from boto.dynamodb2.table import Table

'''
CREATE a table
--------------

import time
from boto.dynamodb2.table import Table
from boto.dynamodb2.fields import HashKey, GlobalKeysOnlyIndex

table = Table.create(shorturl, schema=[
    HashKey('url_short'),
], throughput={
    'read': 18,
    'write': 18,
},
global_indexes=[
    GlobalKeysOnlyIndex('UrlIndex', parts=[
        HashKey('url')
    ], throughput={
        'read': 18,
        'write': 18
    }),
])
time.sleep(30)

DROP a table
------------

from boto.dynamodb import connect_to_region

conn = connect_to_region(region_name='eu-west-1')
table=conn.get_table('shorturl')
table.delete()

'''

# http://boto.readthedocs.org/en/latest/boto_config_tut.html


def _get_dynamodb_conn(region='eu-west-1', profile_name='Credentials'):
    user_cfg = os.path.join(os.path.expanduser("~"), '.boto')
    config = ConfigParser.ConfigParser()
    config.read(["/etc/boto.cfg", user_cfg])

    access_key = config.get(profile_name, 'aws_access_key_id')
    secret_key = config.get(profile_name, 'aws_secret_access_key')

    try:
        conn = connect_to_region('eu-west-1', aws_access_key_id=access_key,
                                 aws_secret_access_key=secret_key)
    except Exception as e:
        raise exc.HTTPBadRequest('Error during connection init %s' % e)
    return conn

conn = _get_dynamodb_conn()


def get_dynamodb_table(table_name='shorturl'):
    try:
        table = Table(table_name, connection=conn)
    except Exception as e:
        raise exc.HTTPBadRequest('Error during connection to the table %s' % e)
    return table


# Different API end point
def get_dynamodb_table_simple(table_name='shorturl'):
    # url_short is the pkey
    try:
        return conn.get_table(table_name)
    except Exception as e:
        raise exc.HTTPBadRequest('Error during simple connection to the table %s' % e)
