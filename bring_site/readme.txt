CREATE DATABASE bring_db;
CREATE USER bring_admin WITH PASSWORD 'password';
ALTER ROLE bring_admin SET client_encoding TO 'utf8';
ALTER ROLE bring_admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE bring_admin SET timezone TO 'UTC+2';
GRANT ALL PRIVILEGES ON DATABASE bring_db TO bring_admin;

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'myproject',
        'USER': 'myprojectuser',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}

ALLOWED_HOSTS = ['your_server_domain_or_IP']