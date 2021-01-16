import argparse
import htmlfunc
import macrosfunc


def fill_container(input):
    container = {'content': ''}
    first_comment_gone = False
    for line in input:
        macros, text = macrosfunc.recognize_macros(line)
        if first_comment_gone is True:
            text = htmlfunc.html_escape(text)
            if macros not in macrosfunc.macroses:
                continue
                # raise Exception('Unknown macros: '+macros)
            macros = macrosfunc.macroses[macros]
            container['content'] += macros.to_html(text, container)
        else:
            if macros != '.TH':
                continue
            else:
                first_comment_gone = True
                text = htmlfunc.html_escape(text)
                macros = macrosfunc.macroses[macros]
                container['content'] += macros.to_html(text, container)
    return container


def man2html(**args):
    source = args.get('input')
    outfile = args.get('output')
    output = htmlfunc.render(**fill_container(source))
    outfile.write(output)


def create_parser():
    parser = argparse.ArgumentParser(description='Parse MAN file extension to HTML file extension',
                                     epilog='Later will be more optional arguments!')
    parser.add_argument('input', help='Inputted file with MAN extension',
                        type=argparse.FileType('r'), metavar='INPUT')
    parser.add_argument('output', metavar='OUTPUT', help='Output file with HTML extension',
                        type=argparse.FileType('w'))
    return parser


if __name__ == '__main__':
    parser = create_parser()
    man2html(**parser.parse_args().__dict__)
