
from flask import Flask, render_template, request
from email.utils import parseaddr
import re

app = Flask(__name__)


def is_valid_email(email):
    """Check that the email address has a valid basic format."""
    if not email or any(char.isspace() for char in email):
        return False

    if email.count("@") != 1:
        return False

    _, parsed_email = parseaddr(email)

    if parsed_email != email:
        return False

    local, domain = email.rsplit("@", 1)

    if not local or not domain or len(email) > 254:
        return False

    if len(local) > 64 or "." not in domain:
        return False

    if local.startswith(".") or local.endswith(".") or ".." in local:
        return False

    if not re.fullmatch(r"[A-Za-z0-9.-]+", domain):
        return False

    if domain.startswith(".") or domain.endswith(".") or ".." in domain:
        return False

    return all(
        label and not label.startswith("-") and not label.endswith("-")
        for label in domain.split(".")
    )


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not message:
            return render_template(
                "contact.html",
                error="All fields are required."
            ), 400

        if not is_valid_email(email):
            return render_template(
                "contact.html",
                error="Please enter a valid email address."
            ), 400

        return render_template("confirmation.html",
                               name=name)

    return render_template("contact.html", error=None)


if __name__ == "__main__":
    app.run(debug=True)
