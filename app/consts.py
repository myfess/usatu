# -*- coding: utf-8 -*-

""" Константы """

import os

ENABLE_ADD_FILE = False
ADS = False
SAPE = False
JIVOSITE = False
REFORMAL = False
COUNTERS = False
TYPESCRIPT = True
ES5 = False
USATU_PATH = 'static/app'
PRODUCTION = False
CAPTCHA_ON = False
CAPTCHA_PUBLIC = '6LdT8yQUAAAAAB6JhSIKamgccowQt3B2_vI1y2_f'
CAPTCHA_SECRET = os.getenv('CAPTCHA_SECRET')

GUEST_PERMISSION = 'g'
EDITOR_PERMISSION = 'e'
ADMIN_PERMISSION = 'a'
USER_PERMISSION = 'u'

GUEST_ID = -1
GUEST = 'Гость'
GUEST_IPB = 'Guest'

AVATAR_PATH = 'static/app/avatars/'
UPLOAD_PATH = 'static/app/uploads/'

USATU_AVATAR_PATH = 'http://www.usatu.com/forum/html/avatars/'
USATU_UPLOAD_PATH = 'http://www.usatu.com/forum/uploads/'

DOCS_PATH = 'files'

COUNT_COMMENTS_PAGE = 20
COUNT_MESSAGES_PAGE = 10

TEACHERS_PHOTO_PATH = 'static/app/teachers'
APP_ROOT_PATH = 'app/'

USATU_NEWS_CATEGORY = 2
