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

To use email functions, like password reset. A Config Var named 'SENDGRID_API_KEY' is needed in settings of Heroku App. You can fetch this key in SendGrid Official Site. For more information, read the article [Setup API Key Environment Variable](https://devcenter.heroku.com/articles/sendgrid#setup-api-key-environment-variable) and article [Obtain an API Key](https://devcenter.heroku.com/articles/sendgrid#obtaining-an-api-key).


2. Deploy App

```
git init
./push.sh $YOUR_COMMIT
heroku run python manage.py migrate
```
