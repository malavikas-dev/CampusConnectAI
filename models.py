import sqlite3
import os

DATABASE = os.getenv("DATABASE_PATH", "database.db")

def get_connection():

    connection = sqlite3.connect(DATABASE)

    connection.row_factory = sqlite3.Row

    return connection

def create_table():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lost_items(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        item_name TEXT,

        category TEXT,

        description TEXT,

        location TEXT,

        date TEXT,

        owner TEXT,

        phone TEXT,

        email TEXT,

        image TEXT,

        user_id INTEGER,

        status TEXT DEFAULT 'Lost'
    )
    """)

    connection.commit()
    connection.close()

def add_lost_item(
    item_name,
    category,
    description,
    location,
    date,
    owner,
    phone,
    email,
    image,
    user_id
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO lost_items
        (
            item_name,
            category,
            description,
            location,
            date,
            owner,
            phone,
            email,
            image,
            user_id,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        item_name,
        category,
        description,
        location,
        date,
        owner,
        phone,
        email,
        image,
        user_id,
        "Lost"
    ))

    connection.commit()
    connection.close()


def get_all_lost_items():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM lost_items")

    items = cursor.fetchall()

    connection.close()

    return items

def get_lost_item(item_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM lost_items WHERE id = ?",
        (item_id,)
    )

    item = cursor.fetchone()

    connection.close()

    return item

def search_lost_items(keyword):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM lost_items
        WHERE item_name LIKE ?
        OR category LIKE ?
        OR location LIKE ?
    """,
    (
        "%" + keyword + "%",
        "%" + keyword + "%",
        "%" + keyword + "%"
    ))

    items = cursor.fetchall()

    connection.close()

    return items

def filter_lost_items(search, category):

    connection = get_connection()

    cursor = connection.cursor()

    query = """
        SELECT *
        FROM lost_items
        WHERE 1=1
    """

    params = []

    if search:
        query += """
            AND (
                item_name LIKE ?
                OR location LIKE ?
                OR description LIKE ?
            )
        """

        keyword = "%" + search + "%"

        params.extend([keyword, keyword, keyword])

    if category:
        query += " AND category = ?"
        params.append(category)

    cursor.execute(query, params)

    items = cursor.fetchall()

    connection.close()

    return items

def create_found_table():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS found_items(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            item_name TEXT,

            category TEXT,

            description TEXT,

            location TEXT,

            date TEXT,

            finder TEXT,

           phone TEXT,

image TEXT,

user_id INTEGER,

status TEXT DEFAULT 'Found'
        )
    """)

    connection.commit()
    connection.close()

def add_found_item(
    item_name,
    category,
    description,
    location,
    date,
    finder,
    phone,
    image,
    user_id
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO found_items
        (item_name, category, description,
 location, date, finder, phone, image, user_id, status)

    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        item_name,
        category,
        description,
        location,
        date,
        finder,
        phone,
        image,
        user_id,
        "Found"
    ))

    connection.commit()
    connection.close()


def get_all_found_items():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM found_items")

    items = cursor.fetchall()

    connection.close()

    return items


def get_found_item(item_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM found_items WHERE id = ?",
        (item_id,)
    )

    item = cursor.fetchone()

    connection.close()

    return item

def find_matching_found_items(lost_item):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM found_items")

    found_items = cursor.fetchall()

    connection.close()

    matches = []

    for found in found_items:

        score = 0

        # Category Match
        if lost_item["category"].lower() == found["category"].lower():
            score += 40

        # Location Match
        if lost_item["location"].lower() == found["location"].lower():
            score += 20

        # Item Name Match
        lost_words = lost_item["item_name"].lower().split()
        found_words = found["item_name"].lower().split()

        common_words = set(lost_words) & set(found_words)

        score += len(common_words) * 15

        # Date Match
        if lost_item["date"] == found["date"]:
            score += 10

        if score >= 40:
            matches.append((found, score))

    matches.sort(key=lambda x: x[1], reverse=True)

    return matches

def create_claims_table():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS claims(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            lost_item_id INTEGER,

            claimant_name TEXT,

            claimant_phone TEXT,

            message TEXT
        )
    """)

    connection.commit()
    connection.close()


def add_claim(lost_item_id, name, phone, message):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO claims
        (lost_item_id, claimant_name, claimant_phone, message)

        VALUES (?, ?, ?, ?)
    """,
    (
        lost_item_id,
        name,
        phone,
        message
    ))

    connection.commit()
    connection.close()

def get_all_claims():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            claims.id,
            claims.claimant_name,
            claims.claimant_phone,
            claims.message,
            lost_items.item_name,
            lost_items.owner,
            lost_items.phone
        FROM claims
        JOIN lost_items
        ON claims.lost_item_id = lost_items.id
        ORDER BY claims.id DESC
    """)

    claims = cursor.fetchall()

    connection.close()

    return claims

def count_lost_items():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM lost_items")

    count = cursor.fetchone()[0]

    connection.close()

    return count


def count_found_items():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM found_items")

    count = cursor.fetchone()[0]

    connection.close()

    return count


def count_claims():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM claims")

    count = cursor.fetchone()[0]

    connection.close()

    return count

def update_lost_status(item_id, status):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE lost_items
        SET status = ?
        WHERE id = ?
        """,
        (status, item_id)
    )

    connection.commit()

    connection.close()


def update_found_status(item_id, status):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE found_items
        SET status = ?
        WHERE id = ?
        """,
        (status, item_id)
    )

    connection.commit()
    connection.close()


def create_users_table():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()

def add_user(name, email, password):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO users
        (name, email, password)

        VALUES (?, ?, ?)
    """,
    (
        name,
        email,
        password
    ))

    connection.commit()
    connection.close()


def get_user_by_email(email):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    )

    user = cursor.fetchone()

    connection.close()

    return user

def get_user_lost_items(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM lost_items WHERE user_id = ? ORDER BY id DESC",
        (user_id,)
    )

    items = cursor.fetchall()

    connection.close()

    return items

def count_user_lost_items(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM lost_items WHERE user_id = ?",
        (user_id,)
    )

    count = cursor.fetchone()[0]

    connection.close()

    return count

def get_user_lost_items(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM lost_items
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (user_id,)
    )

    items = cursor.fetchall()

    connection.close()

    return items

def create_notifications_table():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            message TEXT,

            is_read INTEGER DEFAULT 0
        )
    """)

    connection.commit()
    connection.close()

def add_notification(user_id, message):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO notifications
        (user_id, message)

        VALUES (?, ?)
        """,
        (user_id, message)
    )

    connection.commit()
    connection.close()

    cursor.execute(
        """
        SELECT *
        FROM notifications
        WHERE user_id=?
        ORDER BY id DESC
        """,
        (user_id,)
    )

    notifications = cursor.fetchall()

    connection.close()

    return notifications

def get_notifications(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM notifications
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (user_id,)
    )

    notifications = cursor.fetchall()

    connection.close()

    return notifications

def get_found_item_by_id(item_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM found_items WHERE id = ?",
        (item_id,)
    )

    item = cursor.fetchone()

    connection.close()

    return item

def create_chat_rooms_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_rooms(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            lost_item_id INTEGER,

            found_item_id INTEGER,

            owner_id INTEGER,

            finder_id INTEGER,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()

def create_messages_table():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            room_id INTEGER,

            sender_id INTEGER,

            message TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()

def create_chat_room(lost_item_id, found_item_id, owner_id, finder_id):

    connection = get_connection()
    cursor = connection.cursor()

    # Check if room already exists
    cursor.execute("""
        SELECT id
        FROM chat_rooms
        WHERE lost_item_id = ?
        AND found_item_id = ?
    """, (lost_item_id, found_item_id))

    room = cursor.fetchone()

    if room:
        connection.close()
        return room["id"]

    cursor.execute("""
        INSERT INTO chat_rooms
        (lost_item_id, found_item_id, owner_id, finder_id)

        VALUES (?, ?, ?, ?)
    """,
    (
        lost_item_id,
        found_item_id,
        owner_id,
        finder_id
    ))

    room_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return room_id

def get_chat_room(lost_item_id, found_item_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM chat_rooms
        WHERE lost_item_id = ?
        AND found_item_id = ?
    """, (lost_item_id, found_item_id))

    room = cursor.fetchone()

    connection.close()

    return room

def send_message(room_id, sender_id, message):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO messages
        (room_id, sender_id, message)

        VALUES (?, ?, ?)
    """, (room_id, sender_id, message))

    connection.commit()
    connection.close()


def get_messages(room_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
    messages.*,
    users.name
FROM messages
JOIN users
ON messages.sender_id = users.id
WHERE room_id = ?
ORDER BY messages.id
    """, (room_id,))

    messages = cursor.fetchall()

    connection.close()

    return messages

def get_chat_room_by_id(room_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM chat_rooms
        WHERE id = ?
    """, (room_id,))

    room = cursor.fetchone()

    connection.close()

    return room

def get_user_chat_rooms(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            chat_rooms.id,
            lost_items.item_name,
            found_items.finder,
            found_items.item_name AS found_item,
            chat_rooms.created_at
        FROM chat_rooms

        JOIN lost_items
            ON chat_rooms.lost_item_id = lost_items.id

        JOIN found_items
            ON chat_rooms.found_item_id = found_items.id

        WHERE owner_id = ?
           OR finder_id = ?

        ORDER BY chat_rooms.created_at DESC
    """, (user_id, user_id))

    rooms = cursor.fetchall()

    connection.close()

    return rooms