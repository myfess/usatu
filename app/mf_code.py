# -*- coding: utf-8 -*-

""" Работа с BB кодами """

from app import consts


def mf_code(s):
    s = print_smile(s)
    return mf_code2(s)


def mf_code2(s):
    mf_code_string = ''
    s = s.replace('[br]', '<br />')
    s = s.replace('[*]', '<li>')
    content = ''
    regim_tag = False
    find_tag_open = False
    tag_open = ''
    tag_close = ''

    for c in s:
        if c == '[':
            regim_tag = True
        elif regim_tag and c == ']':
            regim_tag = False
            if not find_tag_open:
                if not isset_tag(tag_name_from_open_tag(tag_open)):
                    mf_code_string += '[{}]'.format(tag_open)
                    tag_open = ''
                else:
                    find_tag_open = True
            else:
                if ('/' + tag_name_from_open_tag(tag_open)) == tag_close:
                    mf_code_string += perform_tag(
                        tag_name_from_open_tag(tag_open),
                        tag_param_from_open_tag(tag_open),
                        content
                    )
                    content = ''
                    find_tag_open = False
                    tag_open = ''
                    tag_close = ''
                else:
                    content += '[{}]'.format(tag_close)
                    tag_close = ''
        elif regim_tag and c != ']' and not find_tag_open:
            tag_open += c
        elif regim_tag and c != ']' and find_tag_open:
            tag_close += c
        elif not find_tag_open:
            mf_code_string += c
        else:
            content += c

    return mf_code_string


def tag_name_from_open_tag(tag):
    tag_name = tag.split('=')
    return tag_name[0]


def tag_param_from_open_tag(tag):
    tag_name = tag.split('=')
    tag_param = ''
    for i in range(1, len(tag_name)):
        if i != 1:
            tag_param += '='
        tag_param += tag_name[i]
    return tag_param


def isset_tag(tag):
    array_tag = [
        'b', 'i', 'u', 'code', 'quote', 'list', '*', 'url', 'email',
        'IMG', 'size', 'color', 'font', 'align', 'htext'
    ]
    return tag in array_tag


def htext_handler(param):
    param_array = param.split(',')
    tag_id = param_array[0]
    tag_id_show = tag_id + '_show'
    caption_open = param_array[1]
    caption_close = param_array[2]

    res = '''
        <span id={tag_id_show}>
            <a
                style="cursor: hand"
                onclick="
                    document.all['{tag_id}'].style.display = '';
                    document.all['{tag_id_show}'].style.display = 'none';
                "
            >
                <b><u>{caption_open}</u></b>
            </a>
        </span>
        <span id={tag_id} style="display: none">
            <a
                style="cursor: hand"
                onclick="
                    document.all['{tag_id}'].style.display = 'none';
                    document.all['{tag_id_show}'].style.display = '';
                "
            >
                <b><u>{caption_close}</u></b>
            </a>
        <br />
    '''.format(
        tag_id_show=tag_id_show,
        tag_id=tag_id,
        caption_open=caption_open,
        caption_close=caption_close
    )

    return res


def perform_tag(name, param, content):
    mf_code_string = ''
    if name == 'IMG':
        mf_code_string += '''
            <img src='{}' border="0" style="max-width: 500px;" VSPACE="10">
        '''.format(content)
        return mf_code_string
    elif name == 'quote':
        mf_code_string += '''
            <table border="0" width="95%" align="center">
                <tr>
                    <td>
                        <table class="quote_table">
                            <tr>
                                <td>{}</td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        '''.format(mf_code2(content))
        return mf_code_string
    elif name == 'code':
        mf_code_string += '''
            <table border="0" width="95%" align="center">
                <tr>
                    <td class="TextContent">
                        <b>Код</b>
                    </td>
                </tr>
                <tr>
                    <td>
                        <table
                            width="100%"
                            cellpadding="3"
                            bgcolor="#9ca2ad"
                            border="0"
                            bordercolor="#9ca2ad"
                            cellspacing="1"
                        >
                            <tr>
                                <td bgcolor="#F8F8F7">{}</td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        '''.format(mf_code2(content))
        return mf_code_string

    open_tag = {
        'b': '<b>',
        'i': '<i>',
        'u': '<u>',
        'list': '<ul>'
    }

    open_tag_param = {
        'email': '<a href="mailto:{}">',
        'url': '<a href="{}" target="_blank">',
        'color': '<span style="color:{}">',
        'font': '<span style="font-family: {}">',
        'align': '<div align="{}">',
        'size': '<span style="font-size: {}pt; line-height: 100%">'
    }

    if name in open_tag:
        mf_code_string += open_tag[name]
    elif name in open_tag_param:
        mf_code_string += open_tag_param[name].format(param)
    elif name == 'htext':
        mf_code_string += htext_handler(param)
    else:
        mf_code_string += '[{}, {}]'.format(name, param)

    mf_code_string += mf_code2(content)

    close = {
        'b': '</b>',
        'i': '</i>',
        'u': '</u>',
        'list': '</ul>',
        'email': '</a>',
        'url': '</a>',
        'color': '</span>',
        'font': '</span>',
        'align': '</div>',
        'size': '</span>',
        'htext': '</span>'
    }

    if name in close:
        mf_code_string += close[name]
    else:
        mf_code_string += '[/{}]'.format(name)

    return mf_code_string


def print_smile(s):
    smile_array = {
        ':huh:': 'huh.gif',
        ':o': 'ohmy.gif',
        ';)': 'wink.gif',
        ':P': 'tongue.gif',
        ':D': 'biggrin.gif',
        ':lol:': 'laugh.gif',
        'B)': 'cool.gif',
        ':rolleyes:': 'rolleyes.gif',
        '{_{': 'dry.gif',
        ':)': 'smile.gif',
        ':angry:': 'mad.gif',
        ':(': 'sad.gif',
        ':unsure:': 'unsure.gif',
        ':blink:': 'blink.gif',
        ':ph34r:': 'ph34r.gif'
    }

    for sm, value in smile_array.items():
        ss = '''
            <img
                src="{USATU_PATH}/picture/smile/{value}"
                border="0"
                alt="{sm}"
                class="rte_smile"
                style="vertical-align: middle"
                alt="{value}"
            />
        '''.format(
            sm=sm,
            value=value,
            USATU_PATH=consts.USATU_PATH
        )

        s = s.replace(sm, ss)

    return s
