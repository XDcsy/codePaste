import web
import time
import os

from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name, get_lexer_for_filename
from web.template import ALLOWED_AST_NODES
ALLOWED_AST_NODES.append('Constant')

render = web.template.render('templates/')

urls = (
    '/', 'index',
    '/p/(.*)', 'html'
)

def trans(content, type, style, suffix):
    print(type, style, suffix)
    if not suffix:
        lexer = get_lexer_by_name(type)
    else:
        try:
            lexer = get_lexer_for_filename(suffix)
        except:
            lexer = get_lexer_by_name(type)
    # 指定风格
    formatter = HtmlFormatter(style=style)
    formatter_noclass = HtmlFormatter(style=style, noclasses=True, cssclass='')
    # 获取html
    html = highlight(content, lexer, formatter)
    html_noclass = highlight(content, lexer, formatter_noclass).replace('&lt;', '&amp;lt;').replace('&gt;', '&amp;gt;')
    return html, html_noclass

class html:
    def GET(self, file_id):
        try:
            with open("./data/" + str(file_id), 'r') as f:
                content = f.read()
            param = web.input(type="text",style="default", suffix=None)
            html, raw = trans(content, param.type, param.style, param.suffix)
            return render.paste(html, raw, "../static/css/"+param.style+".css", time.strftime("%Y-%m-%d %X", time.localtime()))
        except:
            return render.error()

class index:
    def GET(self):
        return open("index.html", encoding='UTF-8').read()

    def POST(self):
        form = web.input()
        file_id = (int)(time.time())
        if not os.path.exists("./data/"):
            os.makedirs("./data/")
        with open("./data/"+str(file_id), 'w', newline='') as f:
            f.write(form.content)
        raise web.seeother('/p/' + str(file_id) + '?type=' + form.type + '&suffix=' + form.suffix)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
