import subprocess
from subprocess import Popen, PIPE

from odoo import models
from odoo.addons.base.models.assetsbundle import CompileError, JavascriptAsset, AssetsBundle
from odoo.tools import misc


"""
SET 2 VARIABLES INSIDE transpile_jsx():
    babel
    npm_root
"""

class IrQweb(models.AbstractModel):
    """ Add ``raise_on_code`` option for qweb. When this option is activated
    then all directives are prohibited.
    """
    _inherit = 'ir.qweb'

    def _get_asset_bundle(self, bundle_name, files, env=None, css=True, js=True):
        return AssetsBundleJsx(bundle_name, files, env=env, css=css, js=js)
    
def transpile_jsx(content_bundle):
    # npm_root = subprocess.run(['npm', '-g', 'root'], text=True, capture_output=True)
    # command = ['babel', '--presets', npm_root.stdout + '/@babel/preset-react', '--no-babelrc']
    babel = "C:/Users/Henrik Norlin/AppData/Roaming/npm/babel.cmd"
    npm_root = "C:/Users/Henrik Norlin/AppData/Roaming/npm/node_modules"
    command = [babel, '--presets', npm_root + '/@babel/preset-react', '--no-babelrc']
    try:
        compiler = Popen(command, stdin=PIPE, stdout=PIPE,
                         stderr=PIPE)
    except Exception:
        raise CompileError("Could not execute command %r" % command[0])
    (out, err) = compiler.communicate(input=content_bundle)
    if compiler.returncode:
        cmd_output = misc.ustr(out) + misc.ustr(err)
        if not cmd_output:
            cmd_output = u"Process exited with return code %d\n" % compiler.returncode
        raise CompileError(cmd_output)
    return out


class JsxAsset(JavascriptAsset):
    @property
    def content(self):
        # print('jsx asset content')
        content = super().content
        content = transpile_jsx(content.encode('utf-8')).decode('utf-8')
        print (content)
        return content


class AssetsBundleJsx(AssetsBundle):

    def __init__(self, name, files, env=None, css=True, js=True):
        super(AssetsBundleJsx, self).__init__(name, files, env=env, css=css, js=js)
        for idx, js in enumerate(self.javascripts):
            # only run transpiler on our own custom script.
            # In production, a better way to distinguish jsx
            # script is needed. 
            if js.url.find('todo') >= 0:
                self.javascripts[idx] = JsxAsset(self, url=js.url, filename=js._filename, inline=js.inline)
