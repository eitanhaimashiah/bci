import os
import pathlib
from datetime import datetime
from flask import Flask


_HTML = '''
<html>
    <head>
        <title>{title}</title>
    </head>
    <body>
        {body}
    </body>
</html>
'''

_INDEX_TITLE = 'Brain Computer Interface'
_INDEX_BODY = '''
<ul>
    {users}
</ul>
'''
_INDEX_USER_LINE = '''
<li><a href="/users/{user_id}">user {user_id}</a></li>
'''

_USER_TITLE = 'Brain Computer Interface: User {user_id}'
_USER_BODY = '''
<table>
    {rows}
</table>
'''
_USER_ROW = '''
<tr>
    <td>{date}</td>
    <td>{thought}</td>
</tr>
'''


def run_webserver(address, data_dir):
    host, port = address
    app = Flask(__name__)
    data_dir = pathlib.Path(data_dir)

    @app.route('/')
    def index():
        index_user_lines = []
        for user_dir in data_dir.iterdir():
            index_user_lines.append(
                _INDEX_USER_LINE.format(user_id=user_dir.name))
        html = _HTML.format(title=_INDEX_TITLE,
                            body=_INDEX_BODY.format(
                                users="\n".join(index_user_lines)))
        return html, 200

    @app.route('/users/<int:user_id>')
    def user(user_id):
        user_path = data_dir / str(user_id)
        user_rows = []
        if not os.path.exists(user_path):
            return '', 404
        for record in user_path.iterdir():
            date = datetime.strptime(record.stem, '%Y-%m-%d_%H-%M-%S').\
                strftime('%Y-%m-%d %H:%M:%S')
            user_rows.append(_USER_ROW.format(date=date,
                                              thought=record.read_text()))
        html = _HTML.format(title=_USER_TITLE.format(user_id=user_id),
                            body=_USER_BODY.format(rows='\n'.join(user_rows)))
        return html, 200

    app.run(host=host, port=port)
