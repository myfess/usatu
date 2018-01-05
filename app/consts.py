# -*- coding: utf-8 -*-

""" Константы """

from secret import config

PRODUCTION = False
#PRODUCTION = True

ENABLE_ADD_FILE = False
ADS = False
SAPE = False
JIVOSITE = False
REFORMAL = False
COUNTERS = False
CAPTCHA_PUBLIC = '6LdT8yQUAAAAAB6JhSIKamgccowQt3B2_vI1y2_f'
CAPTCHA_SECRET = config.CAPTCHA_SECRET

GUEST_PERMISSION = 'g'
EDITOR_PERMISSION = 'e'
ADMIN_PERMISSION = 'a'
USER_PERMISSION = 'u'

GUEST_ID = -1
GUEST = 'Гость'
GUEST_IPB = 'Guest'

COUNT_COMMENTS_PAGE = 20
COUNT_MESSAGES_PAGE = 10

SQL_PATH = 'app/sql'
DOCS_PATH = 'files'
FILES_PATH = 'files'
USATU_PATH = 'static/app'
USATU_BINARY = 'static/files'
TEACHERS_PHOTO_PATH = USATU_BINARY + '/teachers'
APP_ROOT_PATH = 'app/'

USATU_NEWS_CATEGORY = 2

CACHE_INTERVAL = '1 day'

OLD_SITE_PROXY = 'usatu.com'
NAV_CAPTION = 'USATU.com'

DOMEN = 'localhost:1004'
CAPTCHA_ON = False
TYPESCRIPT = True
ES5 = False

if PRODUCTION:
    #DOMEN = 'highload.org'
    DOMEN = 'usatu.com'
    CAPTCHA_ON = True
    TYPESCRIPT = False
    ES5 = True

USATU_AVATAR_PATH = 'http://' + DOMEN + '/' + USATU_BINARY + '/avatars/'
USATU_UPLOAD_PATH = USATU_BINARY + '/uploads/'
