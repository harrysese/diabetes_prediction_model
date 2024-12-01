
set -o errexit
pip install -r requirement.txt
py manage.py collectstatic  --no-input