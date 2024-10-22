# build_files.sh
echo "Starting...."
mkdir venv
echo "venv created"
pwd
echo "printing dir"
ls
echo "done printing dir"
python -m venv venv/
echo "activated"
ls venv/
source venv/bin/activate
pip install -r requirements.txt
python3.9 manage.py collectstatic