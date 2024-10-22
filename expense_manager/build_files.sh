# build_files.sh
echo "Geeks for Geeks"
mkdir venv
python -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
python3.9 manage.py collectstatic