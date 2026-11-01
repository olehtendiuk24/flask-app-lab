from flask import request, redirect, url_for, render_template, session, flash, make_response
from . import users_bp

USER_DATA = {
    "username": "user1",
    "password": "password123"
}

@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == USER_DATA["username"] and password == USER_DATA["password"]:
            session["username"] = username
            flash("Ви успішно увійшли в систему!", "success")
            return redirect(url_for("users.profile"))
        else:
            flash("Wrong data! Try again!", "danger")
            return redirect(url_for("users.login"))

    return render_template("users/login.html", title="Вхід")


@users_bp.route("/profile")
def profile():
    if "username" not in session:
        flash("Будь ласка, увійдіть для доступу до профілю.", "warning")
        return redirect(url_for("users.login"))

    username = session["username"]
    cookies = request.cookies
    return render_template("users/profile.html", title="Профіль", username=username, cookies=cookies)


@users_bp.route("/logout")
def logout():
    session.pop("username", None)
    flash("Ви вийшли з системи.", "info")
    return redirect(url_for("users.login"))


@users_bp.route("/add_cookie", methods=["POST"])
def add_cookie():
    if "username" not in session:
        return redirect(url_for("users.login"))

    key = request.form.get("key")
    value = request.form.get("value")
    max_age = request.form.get("max_age", type=int)

    resp = make_response(redirect(url_for("users.profile")))
    if key and value:
        resp.set_cookie(key, value, max_age=max_age if max_age else None)
        flash(f"Кукі '{key}' успішно додано!", "success")
    else:
        flash("Ключ та значення кукі не можуть бути порожніми.", "danger")
    return resp


@users_bp.route("/delete_cookie", methods=["POST"])
def delete_cookie():
    if "username" not in session:
        return redirect(url_for("users.login"))

    key = request.form.get("key")
    resp = make_response(redirect(url_for("users.profile")))
    if key:
        resp.delete_cookie(key)
        flash(f"Кукі '{key}' успішно видалено!", "info")
    return resp


@users_bp.route("/delete_all_cookies", methods=["POST"])
def delete_all_cookies():
    if "username" not in session:
        return redirect(url_for("users.login"))

    resp = make_response(redirect(url_for("users.profile")))
    for key in request.cookies:
        if key != 'session':  # Не видаляємо сесію, щоб користувач не розлогінився
            resp.delete_cookie(key)
    flash("Усі додаткові кукі видалено!", "info")
    return resp


@users_bp.route("/change_theme/<string:theme>")
def change_theme(theme):
    resp = make_response(redirect(url_for("users.profile")))
    theme_class = "dark-theme" if theme == "dark" else "light-theme"
    resp.set_cookie("theme_color", theme_class, max_age=30*24*60*60)
    flash(f"Тему змінено на {theme}!", "success")
    return resp