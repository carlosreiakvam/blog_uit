from flask import render_template


def page_not_found(e):
    return render_template('404.html', title="404 Siden eksisterer ikke"), 404


def unauthorized(e):
    return render_template("401.html", title="401 - Unauthorized")


def internal_server_error(e):
    return render_template("500.html", title="500 - Internal Server Error")
