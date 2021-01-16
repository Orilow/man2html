import re

table_arcticles = list()


def tagging(text, tag):
    sample = '<{0}>{1}</{0}>'.format(tag, text)
    if tag == 'b':
        sample = '<{0} style="color:#502000">{1}</{0}>'.format(tag, text)
    return sample


def styling(text):
    if re.findall('<b>(.*?)</b>', text) is not None:
        text = re.sub('<b>(.*?)</b>', ' <b style="color:#502000">\\1</b> ', text)
    if re.search('<i>', text) is not None:
        text = re.sub('<i>', ' <i style="color:#008000">', text)
    if re.search('<h3>', text) is not None:
        text = re.sub('<h3>', ' <h3 style="color:#D0171C; letter-spacing:normal">', text)
    return text


def check_outlinks_and_return_html(text):
    regex = re.compile('((?:http|ftp):\/\/.*?(?=[\s<]))')
    if regex.search(text) is not None:
        text = regex.sub('<a href="\\1">\\1</a>', text)
    return text


def insert_id_and_tablelink(title):
    linked_title = '''{0} <a id="{1}">{1}</a>
                    <a style="font-size:75%" href="#top_of_page">&nbsp;&nbsp;&nbsp;&nbsp;top</a>{2}'''\
                    .format(title[:4], title[5:-6], title[-6:])\
                    .replace('&nbsp;', ' ')
    linked_title = styling(linked_title)
    return linked_title


def unprocess_line(line):
    for x in re.findall('"([^"]+)"', line):
        line = line.replace(x, x.replace(' ', r'\ '))
    replacement = {
        r'\(co': '&copy;',
        r'\(rq)': '&quot;',
        r'\(aq': '&quot;',
        r'\(dq': '&quot;',
        r'\(en': '--',
        r'\"': '&quot;',
        r'\/': '&#47;',
        r'\(lq)': '&quot;',
        r'\ ': '&nbsp;',
        r'T}': '</td></tr>',
        r'\e': '&#92;',
        r'\\': '&#92;',
        'tab (@);': '',
        'l lx.': '',
        r'\&': '',
        r'\c': '',
        r'\|': '',
        r'\fR': ' ',
        r'\fP': ' ',
        '"': '',
    }
    for x in replacement:
        line = line.replace(x, replacement[x])
    line = re.sub(r'\\fB([^\s]*)', r'<b>\1</b>', line)
    line = re.sub(r'\\fI([^\s]*)', r'<i>\1</i>', line)
    line = re.sub('(.*)@T{', '<tr><td>\\1</td><td>', line)
    line = line.replace('\\', '')
    line = check_outlinks_and_return_html(line)
    line = styling(line)
    return line


def recognize_macros(raw_line):
    ml = [('', raw_line)]
    ml = re.findall(r'^([\.\'][\"\\\w\{\}\.]{1,2})(.*)', raw_line) or ml
    macros, text = ml[0]
    return macros, text


class Macros:
    """
        container preserves intermediate results
    """

    def to_html(self, text, container): pass


class SettableMacros(Macros):
    def __init__(self, tag, is_two_sided):
        self.is_two_sided = is_two_sided
        self.tag = tag

    def to_html(self, text, c):
        text = unprocess_line(text)
        return tagging(text, self.tag) + ' ' if self.is_two_sided else \
            '<{}>{}'.format(self.tag, text)


class TitleHeader(SettableMacros):
    def __init__(self):
        super(TitleHeader, self).__init__('h1', True)

    def to_html(self, text, c):
        text = unprocess_line(text).split()[0] + ' Linux manual page'
        c['title'] = text
        return super(TitleHeader, self).to_html(text, c) + '<hr>'


class SectionHeader(SettableMacros):
    def __init__(self, tag, indent_tag):
        self.indent_tag = indent_tag
        super(SectionHeader, self).__init__(tag, True)

    def to_html(self, text, c):
        result = list()
        result.append('</' + self.indent_tag + '>')
        result.append(super(SectionHeader, self).to_html(text, c))
        result.append('<' + self.indent_tag + '>')
        if self.tag == 'h3':
            table_arcticles.append(text.strip().strip('"'))
            result[1] = insert_id_and_tablelink(result[1])
        return ''.join(result)


class NoMacros(Macros):
    def to_html(self, text, c):
        return unprocess_line(text)


class FontMacros(Macros):
    def __init__(self, before, after):
        self.before = before
        self.after = after

    def to_html(self, text, c):
        before, after = self.before, self.after
        text = unprocess_line(text)
        result = ''
        for i, t in enumerate(text.split(' ')):
            result += '<{0}>{1}</{0}>'.format(before if i % 2 else after, t)
        result = re.sub('<r>(.*?)</r>', '\\1', result)
        return result + ' '


class TextParagraph(Macros):
    def to_html(self, text, c):
        return '<br>'


class StrangIf(Macros):
    def to_html(self, text, c):
        return ''


macroses = {
    '': NoMacros(),
    '.if': StrangIf(),
    '.TH': TitleHeader(),
    '.SH': SectionHeader('h3', 'sh'),
    '.SS': SectionHeader('h4', 'ss'),
    r'\|\\"': SettableMacros('comment', True),
    '.\\\"': SettableMacros('comment', True),
    '\'\\"': SettableMacros('comment', True),
    '.TP': TextParagraph(),
    '.B': SettableMacros('b', True),
    '.I': SettableMacros('i', True),
    '.PP': SettableMacros('br', False),
    '.P': SettableMacros('br', False),
    '.TS': SettableMacros('table', False),
    '.TE': SettableMacros('/table', False),
    '.pc': SettableMacros('comment', True),
    '.RS': SettableMacros('p', False),
    '.RE': SettableMacros('/p', False),
    '.SM': SettableMacros('small', True),
    '.BR': FontMacros('b', 'r'),
    '.RB': FontMacros('r', 'b'),
    '.BI': FontMacros('b', 'i'),
    '.IB': FontMacros('i', 'b'),
    '.RI': FontMacros('r', 'i'),
    '.IR': FontMacros('i', 'r'),
}
