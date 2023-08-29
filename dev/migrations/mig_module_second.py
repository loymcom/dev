from glob import glob
import os
import re
from xml.etree import ElementTree
from mig_module_common import repo, module


os.chdir(repo + "/" + module)
cwd = os.getcwd()


# SUB FUNCTIONS

def find_file(filepath, pattern):
    with open(filepath, mode='r') as f:
        filetext = f.read()
        result = filetext.find(pattern)
        if result > -1:
            return filepath

def re_search_file(filepath, pattern):
    with open(filepath, mode='r') as f:
        filetext = f.read()
        if re.search(pattern, filetext):
            return filepath

def re_search_update_file(filepath, pattern, replace_with):
    with open(filepath, mode='r') as f:
        old_file = f.read()
        new_file = re.sub(
            pattern,
            replace_with,
            old_file,
        )
    if new_file != old_file:
        with open(filepath, mode='w') as f:
            f.write(new_file)

def search_xpath(filepath, pattern):
    tree = ElementTree.ElementTree()
    tree.parse(filepath)
    match = tree.findall(pattern)
    if match:
        return filepath

# MAIN FUNCTIONS

def get_files(filetype):
    dir_list = []
    if filetype == "python":
        dir_list = ["controllers", "models", "reports"]
    elif filetype == "views":
        dir_list = ["views"]

    filepath_list = []
    for dir in dir_list:
        if os.path.isdir(dir):
            for filename in os.listdir(dir):
                filepath = os.path.join(dir, filename)
                if os.path.isfile(filepath):
                    filepath_list.append(filepath)
    return filepath_list

def log_files_operation(log_message, filepaths, operation, *args, **kwargs):
    log_filepaths = []
    for filepath in filepaths:
        log_filepath = ""
        if operation == "find_files":
            log_filepath = find_file(filepath, *args, **kwargs)
        elif operation == "re_search_files":
            log_filepath = re_search_file(filepath, *args, **kwargs)
        elif operation == "re_search_update_files":
            log_filepath = re_search_update_file(filepath, *args, **kwargs)
        elif operation == "search_xpath":
            log_filepath = search_xpath(filepath, *args, **kwargs)
        if log_filepath:
            log_filepaths.append(log_filepath)
    if log_filepaths:
        print(log_message)
        for log_filepath in log_filepaths:
            print("    - "+log_filepath)

# TASKS TO DO IN THE MIGRATION
# https://github.com/OCA/maintainer-tools/wiki/Migration-to-version-16.0
print("TODO: MIGRATE {} FROM 15.0 TO 16.0 (see https://github.com/OCA/maintainer-tools/wiki/Migration-to-version-16.0)".format(module))
print("")

# Squash
print("Squash administrative commits (if any)")
print("    - git log --oneline")
print("    - git rebase -i HEAD~9")

# Set version 16.0.1.0.0
log_files_operation(
    log_message="Set version 16.0.1.0.0",
    filepaths=["__manifest__.py"],
    operation="re_search_files",
    pattern='\"version\":\s*\"[\d|\.]*\"',
    # replace_with='"version": "16.0.1.0.0"',
)

# Remove migrations
if os.path.isdir('migrations'):
    # os.system("rm -rf "+cwd+"/migrations")
    print("Remove the migrations\n    - migrations")

# Replace name_search with _rec_names_search
log_files_operation(
    log_message="Consider replacing name_search with _rec_names_search",
    filepaths=get_files("python"),
    operation="find_files",
    pattern="name_search",
)

# Remove <field name="groups_id"> inside <record>
log_files_operation(
    log_message="Move groups_id from the view to the elements of the view. Consider adding invisible fields (e.g. company_id) for users who are not in the group.",
    filepaths=get_files("views"),
    operation="search_xpath",
    pattern=".//record[@model='ir.ui.view']/field[@name='groups_id']",
)

# fields_get_keys()
log_files_operation(
    log_message="Replace fields_get_keys() with _fields or get_views()",
    filepaths=get_files("python"),
    operation="find_files",
    pattern="fields_get_keys(",
)

# get_xml_id()
log_files_operation(
    log_message="Replace get_xml_id() with get_external_id()",
    filepaths=get_files("python"),
    operation="find_files",
    pattern="get_xml_id(",
)

# flush()
log_files_operation(
    log_message="flush() is deprecated. Use flush_model(), flush_recordset() or env.flush_all().",
    filepaths=get_files("python"),
    operation="find_files",
    pattern="flush(",
)

# recompute()
log_files_operation(
    log_message="recompute() is deprecated. Use flush_model(), flush_recordset() or env.flush_all().",
    filepaths=get_files("python"),
    operation="find_files",
    pattern="recompute(",
)

# refresh()
log_files_operation(
    log_message="refresh() is deprecated. Use invalidate_model(), invalidate_recordset() or env.invalidate_all().",
    filepaths=get_files("python"),
    operation="find_files",
    pattern="refresh(",
)

# invalidate_cache()
log_files_operation(
    log_message="invalidate_cache() is deprecated. Use invalidate_model(), invalidate_recordset() or env.invalidate_all().",
    filepaths=get_files("python"),
    operation="find_files",
    pattern="invalidate_cache(",
)

# setUp()
log_files_operation(
    log_message="Use setUpClass() instead of setUp().",
    filepaths=get_files("python"),
    operation="find_files",
    pattern="setUp(",
)

# Other
print("Other things to consider:")
print("    - More types of indexes")
print("    - web.assets_qweb is removed. Use the proper asset scope (web.assets_backend, web.assets_frontend, etc).")
print("    - Put unaccent=False on field definitions where no distinction should be made between accented words.")
print("    - Add tests to increase code coverage.")
print("    - Check tasks of previous versions if you are migrating from lower versions than v15.")
print("    - Do the rest of the changes you need to do for making the module works on new version.")
print("Test the module")