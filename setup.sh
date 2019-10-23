virtualenv django_env
source django_env/bin/activate
echo 'source django_env/bin/activate' >> ~/.bashrc
sudo yum install postgresql postgresql-devel python-devel
pip3 install -r requirements.txt