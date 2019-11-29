# TrackingSystem

Implemented by Python with Django.

To setup on AWS, run the following commands.

```
git clone https://github.com/ycremar/TrackingSystem.git
cd TrackingSystem
chmod +x setup.sh
./setup.sh
```

To run web server locally, run the following commands.

```
source ../django_env/bin/activate
python3 manage.py collectstatic
python3 manage.py createsuperuser
python3 manage.py runserver 8080
```

To deploy App to Heroku, run the following commands.

1. Install and setup Heroku App

```
npm install -g heroku
```

Then for new apps, run
```
heroku create
```

For an existing app, run
```
heroku git:remote -a $YOUR_HEROKU_APP_NAME
```

2. Deploy App

```
git init
./push.sh $YOUR_COMMIT
heroku run python manage.py migrate
```
