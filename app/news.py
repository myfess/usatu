# -*- coding: utf-8 -*-

from django.shortcuts import render

from app import consts
from app import mydb
from app.common import get_default_context
from app.message import get_message_text


def message(request, page=1):
    """ Построение ленты """

    db = mydb.MyDB()
    context = get_default_context(request)

    page = int(page)
    start = (page - 1) * consts.COUNT_MESSAGES_PAGE
    cats = get_news_cats('news')

    sql = db.sql('news_count').format(cats=cats)
    count_messages = rs = db.SqlQueryScalar(sql, {'cats': cats})

    sql = db.sql('news_list').format(cats=cats)
    rs = db.SqlQuery(sql, {
        'start': start,
        'count': consts.COUNT_MESSAGES_PAGE,
        'cats': cats
    })

    news = []
    for r in rs:
        news.append(get_message_text(request, r))
    context['news'] = news

    context['PAGE_SELECT'] = create_page_select(
        count_messages, consts.COUNT_MESSAGES_PAGE, page, 'news/all/')

    return render(
        request,
        'app/messages/messages.html',
        context
    )


def get_categoty_id(name):
    db = mydb.MyDB()
    return db.SqlQueryScalar(db.sql('news_categoty_by_name'), {'name': name})


def get_news_cats(name):
    db = mydb.MyDB()
    ids = db.SqlQueryScalar(db.sql('news_cats'), {'name': name})
    return ', '.join([''' '{}' '''.format(_id) for _id in ids])


def create_page_select(count_rec, rec_on_page, this_page, link_start):
    count_page = 0
    r = '<font class="PageSelect">'
    if (count_rec % rec_on_page) != 0:
        count_page = ((count_rec - (count_rec % rec_on_page)) // rec_on_page) + 1
    else:
        count_page = count_rec // rec_on_page

    for i in range(1, count_page + 1):
        if i == this_page:
            r += '<b>[{}]</b> '.format(i)
        else:
            r += '''<a href='{link_start}{i}/'>[{i}]</a>&nbsp;'''.format(
                link_start=link_start,
                i=i
            )

        if i % 10 == 0:
            r += '<br />'
    r += '</font>'
    return r
