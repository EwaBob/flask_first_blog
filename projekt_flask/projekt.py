
from flask import Flask, request, redirect, render_template,  session, url_for


import os

app = Flask(__name__)
app.secret_key = "ulalala"


@app.route("/")
def get_post():
    posts = []
    for post in os.listdir("posts"):
        posts.append(post)
    return render_template('index.html', posts=posts)


@app.route("/show/post/<post>")
def show_post(post):
    with open("posts" + "/" + post, encoding="utf-8") as content:
        line = content.read()
        return render_template('post.html',line=line, title=post)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'Admin' or request.form['password'] != 'Admin':
            error = 'Zły login lub hasło'
        else:
            session['username'] = request.form['username']
            return redirect(url_for('edition'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
   session.pop('username', None)
   return redirect(url_for('get_post'))

@app.route("/edition", methods=['GET', 'POST'])
def edition():
    posts = []
    for post in os.listdir("posts"):
        posts.append(post)
    return render_template('edition.html', posts=posts)


@app.route("/post/create", methods=['GET', 'POST'])
def post_create():
    if 'username' in session:
        username = session['username']
        message = request.args.get("message", "")

        error = None

        if request.method == 'POST':
            if request.form['title'] != '' and request.form['content'] != '':
                title = request.form.get("title")
                content = request.form.get("content")
                path = "posts" + "/" + title
                file = open(path, "w")
                file.write(content)
                file.close()
                if session.get("content"):
                    del session["content"]
                return redirect("/post/create?message=Dodano nowy post")
    else:
        return "Nie jestes zalogowany"
    posts = []
    for post in os.listdir("posts"):
        posts.append(post)
    return render_template('newpost.html',message=message, error=error, posts=posts)

@app.route("/del/<post>", methods=['GET', 'POST'])
def delpost(post):
    if 'username' in session:
        username = session['username']
        path = "posts" + "/" + post
        os.remove(path)
    else:
        return "Nie jestes zalogowany"
    return redirect(url_for('edition'))


@app.route("/update/<post>", methods=['GET', 'POST'])
def updatepost(post):
    if 'username' in session:
        username = session['username']
        message = request.args.get("message", "")
        with open("posts" + "/" + post, encoding="utf-8") as file:
            content = file.read()

        if request.method == 'POST':
            contentnew = request.form.get("content")
            with open("posts" + "/" + post, "w",  encoding="utf-8") as file:
                file.write(contentnew)
            os.rename("posts" + "/" + post, "posts" + "/" + post)
            if session.get("contentnew"):
                del session["contentnew"]
            return redirect("/update/" + str(post) + "?message=Zapisano zmiany")
    else:
        return "Nie jestes zalogowany"

    return render_template('update.html', content = content, post = post, message= message)


if __name__ == "__main__":
    app.run(debug=True)

