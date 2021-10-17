import flask, os, jwt, base64, asyncio, requests
app = flask.Flask(__name__)
port = os.environ.get('LISTEN_PORT')

def get_file(file):
    with open(file) as f:
        return f.read()
app.jinja_env.globals['get_file'] = get_file
app.config.update(BUILT_IN='get_file()', FLAG='flag.txt')

@app.route('/')
def main():
    return flask.render_template("index.html")

@app.route('/approve', methods=['POST'])
def approve():
    title = flask.request.form.get("title")
    story = flask.request.form.get("story")
    url = flask.url_for('viewapproval', title=title, story=story, _external=True)
    content = {'url': url}
    print(content)
    req = requests.post('http://puppet:9000', json=content)
    return flask.redirect(url)

@app.route('/view-approval')
def viewapproval():
    title = flask.request.args.get("title")
    story = flask.request.args.get("story")
    try:
        token = flask.request.cookies.get('token')
        assert jwt.decode(token, "cookie", algorithms="HS256")['admin'] == "true"
    except:
        return flask.render_template("viewapproval.html", title=title, story=story, _external=True)
    else:
        return flask.redirect(flask.url_for('stories', title=title, story=story))

@app.route('/submit')
def submit():
    title = flask.request.args.get("title")
    story = flask.request.args.get("story")
    try:
        token = flask.request.cookies.get('token')
        assert jwt.decode(token, "cookie", algorithms="HS256")['admin'] == "true"
    except:
        return flask.render_template("submit_failed.html", title=title, story=story, _external=True)
    else:
        return flask.redirect(flask.url_for('stories', title=title, story=story))

@app.route('/stories')
def stories():
    try:
        token = flask.request.cookies.get('token')
        assert jwt.decode(token, "cookie", algorithms="HS256")['admin'] == "true"
    except:
        return flask.redirect('/submit')
    else:
        title = flask.request.args.get("title")
        story = flask.request.args.get("story")
        template = '''
        {%% extends 'base.html' %%}
            {%% block body %%}
            <div class="pane">
                <div class="text">
                    <p> Here's your story. Copy the link in the url to share it with your friends! </p><br>
                    <p> To be implemented: Server-side story sharing~ </p> <br><br>
                    <h2> %s </h2><br>
                    <p> %s </p>
                </div>
            </div>
        {%% endblock %%}''' % (title, story)
        return flask.render_template_string(template)
