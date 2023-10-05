# -*- coding: utf-8 -*-
{
    'name': "Documents in AWS S3",
    'version': '0.2',
    'license': 'Other proprietary',
    'author': "Henrik Norlin",
    #'website': "",
    'category': 'Administration', # https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    'depends': ['storage_backend'],
    'external_dependencies': {
        'python': ['boto3'],
    },
    'data': [],
    "post_init_hook": "post_init_hook",  # _post_init_hook_upload_directory_to_aws_s3
    'qweb': [],
    'demo': [],

    'summary': """
        USE MOUNTPOINT-S3
        https://aws.amazon.com/s3/features/mountpoint/
    """,

    'description': """
Amazon S3 Document Management
=================

Manages Document attachments with Amazon S3, using boto3 amazon library (https://github.com/boto/boto3)

        IMPLEMENTATION
        
        FIRST define system parameter:
            
            KEY: ir_attachment.location
            VALUE:
            {
               'AWS_ACCESS_KEY_ID': '',
               'AWS_SECRET_ACCESS_KEY': '',
               'HOSTNAME': '',
               'S3_BUCKET': '',
            }
            GROUP: Administration / Settings

            HOSTNAME may be ams1.vultrobjects.com then ams1 will be the region.
            
        
        THEN install this module.
        
        s3 keys: filestore/database/company/id/ab/abcdefgh...
    """,
}