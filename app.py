import os

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from config import Config
from extensions import db
from models import Lead


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    # =========================
    # PUBLIC PAGES
    # =========================

    @app.route("/")
    def home():
        return render_template("home.html")

    @app.route("/services")
    def services():
        return render_template("services.html")

    @app.route("/solutions")
    def solutions():
        return render_template("solutions.html")

    @app.route("/portfolio")
    def portfolio():
        return render_template("portfolio.html")

    @app.route("/about")
    def about():
        return render_template("about.html")

    @app.route("/faq")
    def faq():
        return render_template("faq.html")

    # =========================
    # CONTACT / LEAD FORM
    # =========================

    @app.route("/contact", methods=["GET", "POST"])
    def contact():

        if request.method == "POST":

            name = request.form.get("name", "").strip()

            business_name = request.form.get(
                "business_name",
                ""
            ).strip()

            email = request.form.get(
                "email",
                ""
            ).strip()

            phone = request.form.get(
                "phone",
                ""
            ).strip()

            city = request.form.get(
                "city",
                ""
            ).strip()

            service = request.form.get(
                "service",
                ""
            ).strip()

            budget = request.form.get(
                "budget",
                ""
            ).strip()

            message = request.form.get(
                "message",
                ""
            ).strip()

            # Required field validation
            if not name:
                flash(
                    "Please enter your name.",
                    "error"
                )
                return redirect(
                    url_for("contact")
                )

            if not email:
                flash(
                    "Please enter your email.",
                    "error"
                )
                return redirect(
                    url_for("contact")
                )

            if not phone:
                flash(
                    "Please enter your phone number.",
                    "error"
                )
                return redirect(
                    url_for("contact")
                )

            if not service:
                flash(
                    "Please select a service.",
                    "error"
                )
                return redirect(
                    url_for("contact")
                )

            # Create lead
            lead = Lead(
                name=name,
                business_name=business_name,
                email=email,
                phone=phone,
                city=city,
                service=service,
                budget=budget,
                message=message,
                status="New"
            )

            try:

                db.session.add(lead)
                db.session.commit()

            except Exception:

                db.session.rollback()

                flash(
                    "We couldn't submit your request. Please try again.",
                    "error"
                )

                return redirect(
                    url_for("contact")
                )

            return redirect(
                url_for("thank_you")
            )

        return render_template(
            "contact.html"
        )

    @app.route("/thank-you")
    def thank_you():
        return render_template(
            "thank_you.html"
        )

    # =========================
    # ADMIN LOGIN
    # =========================

    @app.route("/login", methods=["GET", "POST"])
    def login():

        if session.get("admin_logged_in"):
            return redirect(
                url_for("admin")
            )

        if request.method == "POST":

            password = request.form.get(
                "password",
                ""
            )

            admin_password = os.getenv(
                "ADMIN_PASSWORD",
                "supergen-admin"
            )

            if password == admin_password:

                session["admin_logged_in"] = True

                return redirect(
                    url_for("admin")
                )

            flash(
                "Incorrect password.",
                "error"
            )

        return render_template(
            "login.html"
        )

    # =========================
    # ADMIN DASHBOARD
    # =========================

    @app.route("/admin")
    def admin():

        if not session.get("admin_logged_in"):

            return redirect(
                url_for("login")
            )

        leads = Lead.query.order_by(
            Lead.created_at.desc()
        ).all()

        return render_template(
            "dashboard.html",
            leads=leads
        )

    # =========================
    # ADMIN LOGOUT
    # =========================

    @app.route("/logout")
    def logout():

        session.clear()

        flash(
            "You have been logged out.",
            "success"
        )

        return redirect(
            url_for("login")
        )

    # =========================
    # 404 ERROR
    # =========================

    @app.errorhandler(404)
    def page_not_found(error):

        return render_template(
            "404.html"
        ), 404

    # =========================
    # 500 ERROR
    # =========================

    @app.errorhandler(500)
    def internal_server_error(error):

        try:
            db.session.rollback()
        except Exception:
            pass

        return (
            render_template(
                "500.html"
            ),
            500
        )

    return app


# =========================
# CREATE APPLICATION
# =========================

app = create_app()


# =========================
# LOCAL DEVELOPMENT
# =========================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )