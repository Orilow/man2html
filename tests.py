import unittest
import man2html
import htmlfunc
import macrosfunc


class TestParser(unittest.TestCase):
    def test_creating_parser(self):
        parcer = man2html.create_parser()
        self.assertIsNotNone(parcer)


class TestMacrosesToHTML(unittest.TestCase):
    def test_init_Settable_Macros(self):
        macros = macrosfunc.SettableMacros('b', True)
        self.assertEqual(macros.tag, 'b')
        self.assertEqual(macros.is_two_sided, True)

    def test_to_html(self):
        macros = macrosfunc.SettableMacros('i', True)
        macros_html = macrosfunc.SettableMacros.to_html(macros, 'italic text', dict())
        self.assertEqual(macros_html.strip(), '<i>italic text</i>')

    def test_to_html_2(self):
        macros = macrosfunc.SettableMacros('table', False)
        macros_html = macros.to_html('start of table', dict())
        self.assertEqual(macros_html, '<table>start of table')

    def test_init_font_macros(self):
        macros = macrosfunc.FontMacros('b', 'i')
        self.assertEqual(macros.before, 'b')
        self.assertEqual(macros.after, 'i')

    def test_font_to_html(self):
        macros = macrosfunc.FontMacros('r', 'b')
        macros_html = macros.to_html('bold', dict())
        self.assertEqual(macros.before, 'r')
        self.assertEqual(macros.after, 'b')
        self.assertEqual(macros_html.strip(), '<b>bold</b>')

    def test_font_to_html_2(self):
        macros = macrosfunc.FontMacros('b', 'r')
        macros_html = macros.to_html('regular', dict())
        self.assertEqual(macros.before, 'b')
        self.assertEqual(macros.after, 'r')
        self.assertEqual(macros_html.strip(), 'regular')

    def test_no_macros(self):
        macros = macrosfunc.NoMacros().to_html('text text text', dict())
        self.assertEqual(macros, 'text text text')


class TestStylingAndIdentification(unittest.TestCase):
    def test_tag(self):
        value = macrosfunc.tagging('smth', 'i')
        b_only_value_with_styling = macrosfunc.tagging('smth else', 'b')
        self.assertEqual(value, '<i>smth</i>')
        self.assertEqual(b_only_value_with_styling, '<b style="color:#502000">smth else</b>')

    def test_styling(self):
        macrosB = macrosfunc.styling('<b>kkk</b>')
        macrosI = macrosfunc.styling('<i>ooo</i>')
        macrosH = macrosfunc.styling('<h3>art</h3>')
        self.assertEqual(macrosB, ' <b style="color:#502000">kkk</b> ')
        self.assertEqual(macrosI, ' <i style="color:#008000">ooo</i>')
        self.assertEqual(macrosH, ' <h3 style="color:#D0171C; letter-spacing:normal">art</h3>')

    def test_on_link(self):
        text = macrosfunc.unprocess_line('http://tiswww.case.edu/~chet/bash/POSIX -- a description of posix mode')
        self.assertEqual(text, '<a href="http://tiswww.case.edu/~chet/bash/POSIX">'
                               'http://tiswww.case.edu/~chet/bash/POSIX</a> -- a description of posix mode')


class TestRecognization(unittest.TestCase):
    def test_1(self):
        macros, text = macrosfunc.recognize_macros('.TPtext')
        self.assertEqual(macros, '.TP')
        self.assertEqual(text, 'text')

    def test_2(self):
        macros, text = macrosfunc.recognize_macros('.FNsmth')
        self.assertEqual(macros, '.FN')
        self.assertEqual(text, 'smth')


class TestHTML(unittest.TestCase):
    def test_html_escape(self):
        text = htmlfunc.html_escape('<><>')
        self.assertEqual(text, '&lt;&gt;&lt;&gt;')

    def test_create_table(self):
        artcls = [1, 2]
        new_table = htmlfunc.get_table(artcls)
        self.assertEqual(new_table,
                         htmlfunc.table.format('<a href="#{0}">{0}</a> | <a href="#{1}">{1}</a>'
                                               .format(artcls[0], artcls[1])
                                               )
                         )

    def test_render_with_empty_table(self):
        info = {'content': 'smth interesting', 'title': 'WOW', 'table': ''}
        html_page = htmlfunc.render(**info)
        self.maxDiff = None
        self.assertEqual(html_page, htmlfunc.template.format(**info))


class TestMan2Html(unittest.TestCase):
    def test_filling(self):
        input = ['.THtest\n', '.TPtext2\n', '.IBtext3']
        container = man2html.fill_container(input)
        self.assertEquals(container['title'], 'test Linux manual page')
        self.assertIsNotNone(container['content'])
