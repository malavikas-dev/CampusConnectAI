from flask_mail import Message

def send_claim_email(mail, item, name, phone, message):

    msg = Message(
        subject="📢 New Claim for Your Lost Item",
        recipients=[item["email"]]
    )

    msg.body = f"""
Hello {item['owner']},

Someone has submitted a claim for your lost item.

Item:
{item['item_name']}

Claimant:
{name}

Phone:
{phone}

Message:
{message}

Please contact the claimant if this is your item.

Regards,
CampusConnect AI
"""

    mail.send(msg)