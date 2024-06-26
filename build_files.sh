echo "BUILD START"

# create a virtual environment named 'venv' if it doesn't already exist
python3.9 -m venv venv

# activate the virtual environment
source venv/bin/activate

# install all deps in the venv
python3.9 -m pip install --no-cache-dir -r requirements.txt

# collect static files using the Python interpreter from venv
# python3.9 manage.py collectstatic --noinput

# echo "Contents of staticfiles directory:"
# ls -R staticfiles

echo "BUILD END"