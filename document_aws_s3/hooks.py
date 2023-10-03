from odoo import SUPERUSER_ID, api


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env["ir.attachment"]._post_init_hook_upload_directory_to_aws_s3()
