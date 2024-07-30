"""
Django settings for Shop project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

# Load environment variables from .env file
load_dotenv()
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'kzu*x7^c3tcj^u^h*!vo#4u+wbpfwfp968v9352va4w8=5c2k4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # Required for allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'app_brand',
    'app_category',
    'app_admin_account',
    'app_store',
    'app_wishlist',
    'app_cart',
    'app_order',
]
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'app_admin_account.middleware.EmailVerifiedMiddleware',

    
]

ROOT_URLCONF = 'Shop.urls'

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
                'app_brand.context_processor.menu_links_brand',
                'app_category.context_processor.menu_links',
                'app_cart.context_processor.counter',
                'app_order.context_processor.order_counter',
                
            ],
        },
    },
]

WSGI_APPLICATION = 'Shop.wsgi.application'
AUTH_USER_MODEL = 'app_admin_account.Account'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)
# Correctly fetch environment variables
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('client_id')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('secret')

SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'profile',
    'email',
]

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         'SCOPE': [
#             'profile',
#             'email',
#         ],
#         'AUTH_PARAMS': {
#             'access_type': 'online',
#         }
#     }
# }

# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         'SCOPE': [
#             'profile',
#             'email',
#         ],
#         'AUTH_PARAMS': {
#             'access_type': 'online',
#         },
#         'APP': {
#             'client_id': os.getenv('client_id'),
#             'secret': os.getenv('secret'),
#             'key': ''
#         }
#     }
# }





# AUTHENTICATION_BACKENDS = [
#     'path.to.UserBackend',
#     'path.to.AdminBackend',
#     'django.contrib.auth.backends.ModelBackend',
# ]

# # Use different session engines for user and admin
# SESSION_ENGINE_USER = 'django.contrib.sessions.backends.db'
# SESSION_ENGINE_ADMIN = 'django.contrib.sessions.backends.cache'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

# Add these lines to your settings.py

# LOGIN_REDIRECT_URL = '/accounts/'  # Change to the URL where you want users to be redirected after login
# LOGOUT_REDIRECT_URL = '/login/'  # Change to the URL where you want users to be redirected after logout
# ACCOUNT_LOGOUT_REDIRECT_URL = '/'  # Change to the URL where you want users to be redirected after logout


LOGIN_REDIRECT_URL = '/accounts/'
SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_AUTO_SIGNUP = True  
ACCOUNT_LOGOUT_ON_GET = True
LOGOUT_REDIRECT_URL = "/accounts/sign-in"
STATIC_URL = '/static/'
STATICFILES_DIRS= [os.path.join(BASE_DIR,'static')]
MEDIA_URL='/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')


#for message
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
    
}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=587
EMAIL_HOST_USER='tousif2018ahamid@gmail.com'
EMAIL_HOST_PASSWORD='izcd ntum luvk xowz'
EMAIL_USE_TLS=True


# Dummy PayPal Credentials for Sandbox Environment
PAYPAL_CLIENT_ID = 'AWv6r6meLCSMivdHYqQ0iwRMvXv4EhemUhoH3QbOmqpGyWfExPhXTfaJ4IuGHd76zI6tx3UnOn0cSKfJ'
PAYPAL_SECRET = 'EMwXJvM0OnLhw5l3g9QFIfLOBpPCxCd5sRqdI8karyq9tiP7jBthqrh3nsgWqR6WDGYKPksCTsAL0TKV'
PAYPAL_MODE = 'sandbox' 

# Dummy Bkash Credentials for Sandbox Environment
BKASH_APP_KEY = 'your_bkash_sandbox_app_key'
BKASH_APP_SECRET = 'your_bkash_sandbox_app_secret'
BKASH_USERNAME = 'your_bkash_sandbox_username'
BKASH_PASSWORD = 'your_bkash_sandbox_password'