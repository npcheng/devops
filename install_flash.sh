pip install virtualenv
python_package='
flask
flask-login
flask-openid
flask-mail
flask-sqlalchemy
sqlalchemy-migrate
flask-whooshalchemy
flask-wtf
flask-babel
guess_language
flipflop
coverage'

for pkg in $python_package
do
    pip install $pkg
done

