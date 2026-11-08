from datetime import date
import os
from ai_match import check_matches
from email_service import send_claim_email
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from models import (
    create_table,
    create_found_table,
    create_claims_table,
    add_lost_item,
    add_found_item,
    add_claim,
    get_all_lost_items,
    get_all_found_items,
    get_all_claims,
    get_lost_item,
    get_found_item,
    filter_lost_items,
    find_matching_found_items,
    count_lost_items,
    count_found_items,
    count_claims,
    get_messages,
    send_message,
    send_message,
    update_lost_status,
    update_found_status,
    create_users_table,
    add_user,
    get_user_by_email,
    get_user_lost_items,
    count_user_lost_items,
    get_user_lost_items,
    create_notifications_table,
    add_notification,
    get_notifications,
    create_chat_rooms_table,
    create_messages_table,
    create_chat_room,
    get_chat_room,
    get_found_item_by_id,
    get_chat_room_by_id,
    get_user_chat_rooms
)

from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-only-change-this")
app.config["UPLOAD_FOLDER"] = "static/uploads"

# Brevo Mail Configuration
app.config["MAIL_SERVER"] = "smtp-relay.brevo.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = "campusconnectai2@gmail.com"

mail = Mail(app)

create_table()
create_found_table()
create_claims_table()
create_users_table()
create_notifications_table()
create_chat_rooms_table()
create_messages_table()

@app.route("/")
def home():

    search = request.args.get("search", "")
    category = request.args.get("category", "")

    items = filter_lost_items(search, category)

    latest_items = items[:6]

    return render_template(
        "home.html",
        items=latest_items
    )

@app.route("/report-lost", methods=["GET", "POST"])
def report_lost():

    if "user_id" not in session:
        flash("Please login first.")
        return redirect(url_for("login"))

    if request.method == "POST":

        item_name = request.form["item_name"]
        category = request.form["category"]
        description = request.form["description"]
        location = request.form["location"]
        date = request.form["date"]
        owner = request.form["owner"]
        phone = request.form["phone"]
        email = request.form["email"]

        image = request.files["image"]

        filename = ""

        if image and image.filename != "":
            filename = secure_filename(image.filename)

            image.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

        add_lost_item(
    item_name,
    category,
    description,
    location,
    date,
    owner,
    phone,
    email,
    filename,
    session["user_id"]
)
        return redirect(url_for("dashboard"))

    return render_template("report_lost.html")


@app.route("/report-found", methods=["GET", "POST"])
def report_found():

    if "user_id" not in session:
        flash("Please login first.")
        return redirect(url_for("login"))

    if request.method == "POST":

        item_name = request.form["item_name"]
        category = request.form["category"]
        description = request.form["description"]
        location = request.form["location"]
        date = request.form["date"]
        finder = request.form["finder"]
        phone = request.form["phone"]

        image = request.files["image"]

        filename = ""

        if image and image.filename != "":

            filename = secure_filename(image.filename)

            image.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

        add_found_item(
    item_name,
    category,
    description,
    location,
    date,
    finder,
    phone,
    filename,
    session["user_id"]
)

        return redirect(url_for("view_found"))

    return render_template("report_found.html")

@app.route("/view-lost")
def view_lost():

    items = get_all_lost_items()

    return render_template(
        "view_lost.html",
        items=items
    )


@app.route("/view-found")
def view_found():

    items = get_all_found_items()

    return render_template(
        "view_found.html",
        items=items
    )


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/item/<int:item_id>")
def item_details(item_id):

    item = get_lost_item(item_id)

    if item is None:
        return "Item not found", 404

    found_items = get_all_found_items()

    matches = check_matches(item, found_items)

    return render_template(
        "item_details.html",
        item=item,
        matches=matches
    )

@app.route("/found/<int:item_id>")
def found_details(item_id):

    item = get_found_item(item_id)

    if item is None:
        return "Item not found", 404

    return render_template(
        "found_details.html",
        item=item
    )

@app.route("/claim/<int:item_id>", methods=["GET", "POST"])
def claim_item(item_id):

    if request.method == "POST":

        name = request.form["name"]
        phone = request.form["phone"]
        message = request.form["message"]

        # Save the claim
        add_claim(
            item_id,
            name,
            phone,
            message
        )

        # Get lost item details
        item = get_lost_item(item_id)

        # Send email
        try:
            send_claim_email(
                mail,
                item,
                name,
                phone,
                message
            )
        except Exception as e:
            print("Email Error:", e)

        return redirect(url_for("found_details", item_id=item_id))

    return render_template(
        "claim_item.html",
        item_id=item_id
    )

@app.route("/admin/claims")
def admin_claims():

    claims = get_all_claims()

    return render_template(
        "admin_claims.html",
        claims=claims
    )

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # Temporary admin credentials
        if username == "admin" and password == "admin123":

            session["admin"] = True

            return redirect(url_for("admin_dashboard"))

        else:
            flash("Invalid username or password")

    return render_template("admin_login.html")

@app.route("/admin")
def admin_dashboard():

    if "admin" not in session:
        return redirect(url_for("admin_login"))

    return render_template(

        "admin_dashboard.html",

        lost_count=count_lost_items(),

        found_count=count_found_items(),

        claim_count=count_claims(),

        lost_items=get_all_lost_items()[:5],

        found_items=get_all_found_items()[:5],

        claims=get_all_claims()[:5]

    )

@app.route("/admin/logout")
def admin_logout():

    session.pop("admin", None)

    return redirect(url_for("admin_login"))

@app.route("/test")
def test():

    items = get_all_lost_items()

    return "<br>".join(
        f"{item['item_name']} - {item['status']}"
        for item in items
    )

@app.route("/update-lost-status/<int:item_id>", methods=["POST"])
def update_lost(item_id):

    status = request.form["status"]

    update_lost_status(item_id, status)

    return redirect(url_for("admin_dashboard"))

@app.route("/update-found-status/<int:item_id>", methods=["POST"])
def update_found(item_id):

    status = request.form["status"]

    update_found_status(item_id, status)

    return redirect(url_for("admin_dashboard"))

@app.route("/send-test-email")
def send_test_email():

    msg = Message(
        subject="CampusConnect AI Test Email",
        recipients=["campusconnectai2@gmail.com"] 
    )

    msg.body = """
Hello!

Congratulations 🎉

Your CampusConnect AI email system is working successfully.

This is a test email sent using Flask and Brevo.

- CampusConnect AI
"""

    mail.send(msg)

    return "✅ Test email sent successfully!"

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        # Check if email already exists
        if get_user_by_email(email):
            flash("Email already registered.")
            return redirect(url_for("signup"))

        hashed_password = generate_password_hash(password)

        add_user(
            name,
            email,
            hashed_password
        )

        flash("Account created successfully! Please login.")

        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = get_user_by_email(email)

        if user and check_password_hash(user["password"], password):

            session["user_id"] = user["id"]
            session["user_name"] = user["name"]

            flash("Login Successful!")

            return redirect(url_for("dashboard"))

        flash("Invalid Email or Password")

    return render_template("login.html")

@app.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully.")

    return redirect(url_for("dashboard"))

@app.route("/my-reports")
def my_reports():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    return render_template(
        "my_reports.html",
        lost_items=get_user_lost_items(user_id),
        lost_count=count_user_lost_items(user_id)
    )


@app.route("/notifications")
def notifications():

    if "user_id" not in session:
        return redirect(url_for("login"))

    notifications = get_notifications(session["user_id"])

    return render_template(
        "notifications.html",
        notifications=notifications
    )

@app.route("/chat/<int:room_id>", methods=["GET", "POST"])
def chat(room_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    room = get_chat_room_by_id(room_id)

    if room is None:
        return "Chat room not found.", 404

    # Only owner or finder can access
    if session["user_id"] not in [room["owner_id"], room["finder_id"]]:
        return "Unauthorized", 403

    if request.method == "POST":

        message = request.form["message"].strip()

        if message:
            send_message(
                room_id,
                session["user_id"],
                message
            )

        return redirect(url_for("chat", room_id=room_id))

    messages = get_messages(room_id)

    return render_template(
        "chat.html",
        messages=messages,
        room=room
    )

@app.route("/chat/start/<int:found_item_id>")
def start_chat(found_item_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    found_item = get_found_item_by_id(found_item_id)

    if not found_item:
        return "Found item not found", 404

    # Temporary: find the first matching lost item
    lost_items = get_all_lost_items()

    lost_item = None

    for item in lost_items:
        if item["category"] == found_item["category"]:
            lost_item = item
            break

    if not lost_item:
        return "No matching lost item found."

    room = get_chat_room(
        lost_item["id"],
        found_item["id"]
    )

    if room:
        room_id = room["id"]
    else:
        room_id = create_chat_room(
            lost_item["id"],
            found_item["id"],
            lost_item["user_id"],
            found_item["user_id"]
        )

    return redirect(
        url_for(
            "chat",
            room_id=room_id
        )
    )
@app.route("/my-chats")
def my_chats():

    if "user_id" not in session:
        return redirect(url_for("login"))

    rooms = get_user_chat_rooms(session["user_id"])

    return render_template(
        "my_chats.html",
        rooms=rooms
    )

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)