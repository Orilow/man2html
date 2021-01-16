from macrosfunc import table_arcticles


def html_escape(text):
    return text.replace('>', '&gt;').replace('<', '&lt;')


def render(**args):
    default_args = {
        'title': 'Some Title',
        'content': 'SOMETHING',
        'table': 'ARTICLES'
    }
    cur_table = {'table': get_table(table_arcticles)}
    default_args.update(cur_table)
    default_args.update(args)
    return template.format(**default_args)


def get_table(articles):
    new_table = ''
    for article in articles:
        new_table += '<a href="#{0}">{0}</a> | '.format(article)
    return table.format(new_table[:-3])


template = '''
<html>
    <head>
        <a id="top_of_page"></a>
        <title>{title} Linux manpage</title>
        <meta charset="utf-8">
            <style>
                <input type="text" style="width:200px; height:25px;" />
                html {{ font-family: sans  }}
                comment {{ display: none }}
                table {{ margin: 10px }}
                table td {{ padding-right: 30px }}
                ss, sh {{ display: block; margin-left: 2em; }}
                li {{ list-style:none }}
                .italic {{ font-style: italic; color:#008000 }}
                .regular {{ font-family: sans; font-weight: normal }}
                .bold {{ font-weight: bold; color:#502000}}
                tab {{ margin-left: 1em }}
            </style>
        {table}
    </head>
<body>
    <div style="float:left; width:70%; letter-spacing: 1px">
    <style>
        body {{ color: #181818; font-family: "Courier New", monospace; display:block }}
        .bold {{ color:#502000 }}
        .italic {{ font-style:italic; color:#008000 }}
        letter-spacing: 5px
    </style>
    {content}
    </div>
</body>
</html>'''


table = '''
<table style="">
    <tbody>
        <tr>
            <td>
                <div style="float:left; width:60%">
                    <p style="font-size:87%; font-family:sans-serif">
                        {0}
                    </p>
                </div>
            </td>
        </tr>
    </tbody>
</table>
'''
