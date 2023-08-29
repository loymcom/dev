import subprocess

from mig_module_common import repo, module


commands = """
    # git clone https://github.com/OCA/{repo} -b 16.0
    cd {repo}
    git checkout -b 16.0-mig-{module} origin/16.0
    git fetch origin 15.0
    git format-patch --keep-subject --stdout origin/16.0..origin/15.0 -- {module} | git am -3 --keep
    pre-commit run -a  # to run black, isort and prettier (ignore pylint errors at this stage)
    git add -A
    git commit -m '[IMP] {module}: pre-commit stuff'  --no-verify  # it is important to do all formatting in one commit the first time
""".format(repo=repo, module=module)

subprocess.run(commands, check=True, capture_output=True, shell=True)
