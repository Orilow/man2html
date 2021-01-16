def html_escape(text):
    return text.replace('>', '&gt;').replace('<', '&lt;')


def render(**args):
    default_args = {'title': '', 'content': ''}
    default_args.update(args)
    return template.format(**default_args)



template = '''<html>
<head>
    <title>man2html - {title}</title>
    <meta charset="utf-8">
    <style>
        html {{ font-family: sans  }}
        comment {{ display: none }}
        table {{ margin: 10px }}
        table td {{ padding-right: 30px }}
        ss, sh {{ display: block; margin-left: 2em; }}
        li {{ list-style:none }}
        .italic {{ font-style: italic }}
        .regular {{ font-family: sans; font-weight: normal }}
        .bold {{ font-weight: bold }}
        tab {{ margin-left: 1em }}
    </style>
</head>
<body>
    {content}
</body>
</html>'''