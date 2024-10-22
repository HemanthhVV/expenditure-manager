# build_files.sh
echo "Starting...."
mkdir venv
echo "venv created"
python -m venv ./venv
echo "activated"
pwd
ls venv
source venv/bin/activate
pip install -r requirements.txt
python3.9 manage.py collectstatic