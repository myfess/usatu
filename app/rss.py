import datetime

from django.http import HttpResponse

from app import mydb
from app.message import get_message_text


def get_blog_rss(request):
    db = mydb.MyDB()

    rs = db.SqlQuery(db.sql('blog_posts'), {
        'start': 0,
        'count': 10,
        'username': None
    })

    items = ''

    for r in rs:
        t = get_message_text(request, r, is_comment=False, blog=True, preview=False)
        _time = datetime.datetime.fromtimestamp(r['time']).strftime('%a, %d %b %Y %H:%M:%S %z')

        s = '''
            <item>
                <title>{title}</title>
                <link>http://highload.org/post{post_id}</link>
                <guid>http://highload.org/post{post_id}</guid>
                <description><![CDATA[{text}]]></description>
                <author>my_fess</author>
                <pubDate>{pub_date}</pubDate>
            </item>
        '''.format(
            title=r['title'],
            text=t['message_text'],
            post_id=r['blog_post_id'],
            pub_date=_time
        )
        items += s

    res = '''<?xml version="1.0" encoding="UTF-8"?>'''
    res += '''
        <rss version="2.0">
            <channel>
                <title>HighLoad.org</title>
                <link>http://highload.org</link>
                <description>HighLoad.org – блог о высоких нагрузках</description>
            </channel>
            {items}
        </rss>
    '''.format(items=items)

    return HttpResponse(res, content_type='text/xml')



