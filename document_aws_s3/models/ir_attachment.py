from odoo import models, fields, api, _
from odoo import SUPERUSER_ID
from odoo.tools.config import config
from odoo.exceptions import UserError
from boto3.session import Session
import ast
import os
import logging
_logger = logging.getLogger(__name__)


class ir_attachment(models.Model):
    _inherit = 'ir.attachment'

    def _file_read(self, fname, bin_size=False):
        s3_key = self._s3_key(fname)
        aws_session, s3_bucket_name, endpoint_url = self._get_session_bucket_endpoint()

        location = self.env['ir.config_parameter'].sudo().get_param('ir_attachment.location')
        if location:
            location_dict = ast.literal_eval(location)
            
            try:
                response = aws_session.client('s3', enpoint_url=endpoint_url).get_object(Bucket=s3_bucket_name,Key=s3_key)
            except:
                _logger.info('Could not get from s3 key ' + s3_key) # I think that the response is ok also if get_object fails
                return False
            contents = response['Body'].read().encode('base64')
            return contents

    def _file_write(self, value, checksum):
        bin_value = value.decode('base64')
        fname, full_path = self._get_path(bin_value, checksum)
        company_id = self.env.company.id
        fname = 'company/' + str(company_id) + '/' + fname
        s3_key = self._s3_key(fname)
        aws_session, s3_bucket_name, endpoint_url = self._get_session_bucket_endpoint()
        try:
            error_if_not_exists = aws_session.resource('s3').Object(s3_bucket_name, s3_key).content_type
            _logger.info('_file_write: file exists: ' + fname)
        except:
            client = aws_session.client("s3", endpoint_url=endpoint_url)
            client.put_object(Bucket=s3_bucket_name, Key=s3_key, Body=bin_value, ACL='private')
        return fname
            
    def _file_delete(self, fname):
        # using SQL to include files hidden through unlink or due to record rules
        self.env.cr.execute("SELECT COUNT(*) FROM ir_attachment WHERE store_fname = %s", (fname,))
        count = self.env.cr.fetchone()[0]
        if not count:
            s3_key = self._s3_key(fname)
            aws_session, s3_bucket_name, endpoint_url = self._get_session_bucket_endpoint()
            try:
                aws_session.resource('s3').Object(s3_bucket_name, s3_key).delete()
            except Exception as e:
                _logger.warning("_file_delete: The file did not exist or could not be deleted: %s", s3_key, exc_info=True)
                
    def _s3_key(self, fname):
        s3_key = 'filestore/' + self.env.cr.dbname + '/' + str(fname)
        return s3_key
    
    def _get_session_bucket_endpoint(self):
        location = self.env['ir.config_parameter'].sudo().get_param('ir_attachment.location')
        if location:
            location_dict = ast.literal_eval(location)
            hostname = location_dict['HOSTNAME']
            aws_session = Session(
                aws_access_key_id=location_dict['AWS_ACCESS_KEY_ID'],
                aws_secret_access_key=location_dict['AWS_SECRET_ACCESS_KEY'],
                region_name=hostname.split('.')[0],
            )
            s3_bucket_name = location_dict['S3_BUCKET']
            endpoint_url = "https://" + location_dict['HOSTNAME']
            return aws_session, s3_bucket_name, endpoint_url
        else:
            _logger.warning("_get_session_bucket_endpoint: Missing ir_attachment.location", exc_info=True)
                
    def _post_init_hook_upload_directory_to_aws_s3(self):
        directory = config.get("data_dir") + '/filestore/' + self.env.cr.dbname
        s3_key_root = self._s3_key('').rstrip('\\').rstrip('/')
        aws_session, s3_bucket_name, endpoint_url = self._get_session_bucket_endpoint()
        for path,dirs,files in os.walk(directory):
            path = path.rstrip('\\').rstrip('/')
            s3_key_path = s3_key_root + path.replace(directory, '').replace("\\", "/")
            for file in files:
                s3_key = s3_key_path + '/' + file
                try:
                    error_if_not_exists = aws_session.resource('s3').Object(s3_bucket_name, s3_key).content_type
                    _logger.info('_file_write: file exists: ' + s3_key)
                except:
                    bin_value = open(os.path.join(path, file), 'rb')
                    client = aws_session.client("s3", endpoint_url=endpoint_url)
                    client.put_object(Bucket=s3_bucket_name, Key=s3_key, Body=bin_value, ACL='private')
