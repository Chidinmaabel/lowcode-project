import os
import re
import secrets

from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
# Set SECRET_KEY in the environment for production. The random fallback
# invalidates sessions on every restart.
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)

MAX_NAME = 100
MAX_EMAIL = 254
MAX_MESSAGE = 5000

# Pragmatic email check: local part, "@", and a dotted domain with valid labels.
EMAIL_RE = re.compile(
    r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+"
    r"@[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)+$"
)


def get_csrf_token() -> str:
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(32)
    return session["csrf_token"]


app.jinja_env.globals["csrf_token"] = get_csrf_token


def csrf_is_valid() -> bool:
    sent = request.form.get("csrf_token", "").encode()
    expected = session.get("csrf_token", "").encode()
    return bool(expected) and secrets.compare_digest(sent, expected)


def validate(name: str, email: str, message: str) -> dict:
    errors = {}

    if not name:
        errors["name"] = "Please enter your name."
    elif len(name) > MAX_NAME:
        errors["name"] = f"Name must be at most {MAX_NAME} characters."

    if not email:
        errors["email"] = "Please enter your email address."
    elif len(email) > MAX_EMAIL or not EMAIL_RE.match(email):
        errors["email"] = "Please enter a valid email address."

    if not message:
        errors["message"] = "Please enter a message."
    elif len(message) > MAX_MESSAGE:
        errors["message"] = f"Message must be at most {MAX_MESSAGE} characters."

    return errors


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "GET":
        return render_template("contact.html", form={}, errors={})

    form = {
        "name": request.form.get("name", "").strip(),
        "email": request.form.get("email", "").strip(),
        "message": request.form.get("message", "").strip(),
    }

    if not csrf_is_valid():
        errors = {"form": "Your session expired or the request was invalid. Please try again."}
        return render_template("contact.html", form=form, errors=errors), 400

    errors = validate(**form)
    if errors:
        return render_template("contact.html", form=form, errors=errors), 400

    # TODO: deliver the message (send an email, store it, etc.).
    app.logger.info("Contact message from %s <%s>", form["name"], form["email"])

    # Post/Redirect/Get so a refresh doesn't resubmit the form.
    session["contact_sent"] = True
    return redirect(url_for("contact_thanks"))


@app.route("/contact/thanks")
def contact_thanks():
    if not session.pop("contact_sent", False):
        return redirect(url_for("contact"))
    return render_template("contact.html", sent=True)


if __name__ == "__main__":
    app.run(debug=True)