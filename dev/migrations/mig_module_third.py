import subprocess

from mig_module_common import module


commands = """
    git checkout 16.0-mig-{module}
    git add --all
    git commit -m "[MIG] {module}: Migration to 16.0"
""".format(module=module)

subprocess.run(commands, check=True, capture_output=True, shell=True)
# subprocess.run(commands, check=False, capture_output=False, shell=True)

# WHY DOES IT NOT WORK???