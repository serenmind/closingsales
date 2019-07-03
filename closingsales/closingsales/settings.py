import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'k8c9u1q7!j(=bj_&(ou0#=(jz*e5t#pvtnynxe_$25wjubb#m&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = []
# ALLOWED_HOSTS = ['165.227.139.15', 'closingshops.de', 'http://closingshops.de', 'www.closingshops.de', 'http://www.closingshops.de', 'localhost', 'localhost:8000']
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
     'widget_tweaks',
    'rest_framework',
    'rest_framework_jwt',
    'frontend',
    'account',
    'products',
    'address',
    'notification',
    'api',
    'dashboard',
    'debug_toolbar',
    'django_extensions'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'closingsales.middleware.LoginRequiredMiddleware',
    'closingsales.middleware.CategoryMiddleware',
    # 'closingsales.middleware.NotificationMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]

ROOT_URLCONF = 'closingsales.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'closingsales.wsgi.application'

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            }
        }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'closingsales',
#         'HOST': 'localhost'
#     }
# }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 15,
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        'api.permissions.IsOwner',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
GOOGLE_API_KEY = 'AIzaSyCx9-BAzvVk_q_Qrd4T_qcuCfVtmUldFpE'


STATIC_URL = '/static/'
# STATIC_ROOT= os.path.join(BASE_DIR, 'static')
# MEDIA_URL = '/media/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]


LOGOUT_REDIRECT_URL = '/'
LOGIN_REQUIRED_URLS = (
    r'/dashboard(.*)$',
)
LOGIN_REQUIRED_URLS_EXCEPTIONS = (
    r'/accounts(.*)$',
)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
AUTH_USER_MODEL = 'account.User'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'closingsales.de@gmail.com'
EMAIL_HOST_PASSWORD = 'ClosingSales1@'
EMAIL_PORT = 587
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
TIME_INPUT_FORMATS = ['%I:%M %p',]
