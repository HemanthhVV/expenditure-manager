# build_files.sh
echo "Geeks for Geeks"
mkdir venv
echo "venv created"
python -m venv ./venv
echo "activated"
pwd
ls
source ./venv/bin/activate
pip install -r requirements.txt
python3.9 manage.py collectstatic