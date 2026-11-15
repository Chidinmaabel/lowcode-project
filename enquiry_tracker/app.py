import os
from datetime import date
import secrets
from flask import Flask, abort, redirect, render_template, request, url_for, session

from db import get_db, init_app

STATUSES = ["new", "contacted", "quote_sent", "accepted", "lost"]


def clean_form(form):
    """Read the form fields, tidy them, and check the required ones.

    Returns (data, errors). errors is empty if everything is valid.
    """
    data = {
        "customer_name": form.get("customer_name", "").strip(),
        "phone": form.get("phone", "").strip(),
        "email": form.get("email", "").strip(),
        "service_type": form.get("service_type", "").strip(),
        "description": form.get("description", "").strip(),
        "follow_up_date": form.get("follow_up_date", "").strip(),
    }

    errors = {}

    if not data["customer_name"]:
        errors["customer_name"] = "Customer name is required."
    elif len(data["customer_name"]) > 200:
        errors["customer_name"] = "Customer name must be 200 characters or fewer."

    if not data["phone"]:
        errors["phone"] = "Phone is required."

    if not data["email"]:
        errors["email"] = "Email is required."

    if data["follow_up_date"]:
        try:
            date.fromisoformat(data["follow_up_date"])
        except ValueError:
            errors["follow_up_date"] = "Please enter a valid follow-up date."
    return data, errors


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or os.urandom(32)
    app.config["DATABASE"] = os.path.join(app.root_path, "enquiries.db")

    init_app(app)
    @app.before_request
    def protect_post_requests():
        if request.method == "POST":
            token = session.get("_csrf_token")
            submitted_token = request.form.get("_csrf_token")

            if not token or not submitted_token:
                abort(400)

            if not secrets.compare_digest(token, submitted_token):
                abort(400)

    @app.context_processor
    def inject_csrf_token():
        def generate_csrf_token():
            if "_csrf_token" not in session:
                session["_csrf_token"] = secrets.token_hex(32)
            return session["_csrf_token"]

        return {"csrf_token": generate_csrf_token}
    # GET / : list all enquiries, newest first
    @app.route("/")
    def index():
        db = get_db()
        enquiries = db.execute(
            "SELECT * FROM enquiry ORDER BY created_at DESC, id DESC"
        ).fetchall()
        return render_template("index.html", enquiries=enquiries)

    # GET /enquiry/new : show the empty form
    @app.route("/enquiry/new")
    def new_enquiry():
        return render_template("enquiry_form.html", data={}, errors={})

    # POST /enquiry : validate, save, redirect to /
    @app.route("/enquiry", methods=["POST"])
    def create_enquiry():
        data, errors = clean_form(request.form)

        if errors:
            # Show the form again with messages and the values already typed
            return render_template(
                "enquiry_form.html", data=data, errors=errors
            ), 400

        db = get_db()
        db.execute(
            "INSERT INTO enquiry "
            "(customer_name, phone, email, service_type, description, follow_up_date) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (
                data["customer_name"],
                data["phone"],
                data["email"],
                data["service_type"] or None,
                data["description"] or None,
                data["follow_up_date"] or None,
            ),
        )
        db.commit()
        return redirect(url_for("index"))

    # GET /enquiry/<id> : show one enquiry
    @app.route("/enquiry/<int:enquiry_id>")
    def show_enquiry(enquiry_id):
        db = get_db()
        enquiry = db.execute(
            "SELECT * FROM enquiry WHERE id = ?", (enquiry_id,)
        ).fetchone()
        if enquiry is None:
            abort(404)
        return render_template(
            "enquiry_detail.html", enquiry=enquiry, statuses=STATUSES
        )

    # POST /enquiry/<id>/status : change status, redirect back to the enquiry
    @app.route("/enquiry/<int:enquiry_id>/status", methods=["POST"])
    def change_status(enquiry_id):
        new_status = request.form.get("status", "")
        if new_status not in STATUSES:
            abort(400)

        db = get_db()
        enquiry = db.execute(
            "SELECT id FROM enquiry WHERE id = ?", (enquiry_id,)
        ).fetchone()
        if enquiry is None:
            abort(404)

        db.execute(
            "UPDATE enquiry SET status = ? WHERE id = ?",
            (new_status, enquiry_id),
        )
        db.commit()
        return redirect(url_for("show_enquiry", enquiry_id=enquiry_id))

    return app