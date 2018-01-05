"""
Definition of urls for pyusatu.
"""

from django.conf.urls import url

from app.api import api_navigation, sbis_api_navigation
from app.teachers import teachers_list, get_teachers_teacher, teachers_add_edit, chair_list
from app.board import get_board_theme, get_board_theme_comments
from app.message import message_navigation_board_theme
from app.message import message_navigation_writer
from app.message import message_navigation_comment
from app.message import full_message
from app.edu_files import get_files_for_edu_main, get_files_for_edu_add_file
from app.static import get_links, get_inf, get_agreement
from app.news import message
from app.moderation import news_mod, teachers_mod, comments_mod


urlpatterns = [
    url(r'^$', message),

    url(r'^api_usatu$', api_navigation),
    url(r'^service/?$', sbis_api_navigation),

    url(r'^mod/news/?$', news_mod),
    url(r'^mod/teachers/?$', teachers_mod),
    url(r'^mod/comments/?$', comments_mod),

    url(r'^writer/?$', message_navigation_writer),
    url(r'^writer/(\d+)/?$', message_navigation_writer),
    url(r'^comment/(\d+)/?$', message_navigation_comment),
    url(r'^news/?$', message),
    url(r'^news/all/(\d+)/?$', message),
    url(r'^news/(\d+)/?$', full_message),
    url(r'^news/(\d+)/(\d+)/?$', full_message),
    url(r'^news/(\d+)/(\d+)/gotocomment/(\d+)/?$', full_message),

    url(r'^teachers/?$', teachers_list),
    url(r'^teachers/chair/(\d+)/?$', chair_list),
    url(r'^teachers/(\d+)/?$', get_teachers_teacher),
    url(r'^teachers/(\d+)/(\d+)/?$', get_teachers_teacher),
    url(r'^teachers/(\d+)/(\d+)/gotocomment/(\d+)/?$', get_teachers_teacher),
    url(r'^teachers/edit/?$', teachers_add_edit),
    url(r'^teachers/edit/(\d+)/?$', teachers_add_edit),

    url(r'^files_for_edu/?$', get_files_for_edu_main),
    url(r'^files_for_edu/add_file/?$', get_files_for_edu_add_file),
    url(r'^files_for_edu/(\d+)/?$', get_files_for_edu_main),
    url(r'^files_for_edu/(\d+)/(\d+)/?$', get_files_for_edu_main),

    url(r'^board/?$', get_board_theme),
    url(r'^board/theme/(\d+)/?$', get_board_theme_comments),
    url(r'^board/theme/(\d+)/(\d+)/?$', get_board_theme_comments),
    url(r'^board_theme/?$', message_navigation_board_theme),

    url(r'^links/?$', get_links),
    url(r'^inf/?$', get_inf),
    url(r'^agreement/?$', get_agreement),
]
