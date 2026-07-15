# CampusConnectAI
CampusConnect AI is a full-stack Flask web application designed to streamline campus lost-and-found management. It features secure authentication, AI-assisted item matching, real-time communication between users, claim management, notifications, email alerts, and an admin dashboard, all within a responsive and user-friendly interface.

# 🎒 CampusConnect AI

> An AI-powered Lost & Found platform built for educational campuses using Flask.

CampusConnect AI helps students and staff report lost or found items, receive intelligent match suggestions, communicate securely through private chat, and manage claims—all from a modern, user-friendly web application.

---

## 🚀 Features

### 👤 User Authentication
- Secure user registration
- Login & logout
- Session management
- Protected routes

### 📦 Lost & Found Management
- Report lost items
- Report found items
- Upload item images
- View all lost items
- View all found items
- Item details page

### 🤖 AI Matching
- Smart matching based on:
  - Item name
  - Category
  - Location
  - Date
- Displays possible matching items with confidence score

### 💬 Private Chat
- One-to-one chat between owner and finder
- Chat room creation
- Message history

### 📩 Claim System
- Claim ownership of found items
- Submit contact information
- Send claim message

### 🔔 Notifications
- Receive important updates
- Claim notifications
- AI match notifications

### 📧 Email Support
- Email alerts for claim requests
- SMTP integration using Brevo

### 🛠 Admin Dashboard
- View reports
- Monitor claims
- Track platform statistics

### 🎨 Premium UI
- Responsive design
- Dark theme
- Glassmorphism cards
- Bootstrap 5
- Bootstrap Icons

---

## 🛠 Tech Stack

### Backend
- Python
- Flask
- SQLite

### Frontend
- HTML5
- CSS3
- Bootstrap 5
- JavaScript

### AI
- Custom rule-based matching algorithm

### Other Libraries
- Flask-Mail
- Werkzeug

---

## 📂 Project Structure

```
CampusConnectAI/
│
├── app.py
├── models.py
├── ai_match.py
├── email_service.py
├── requirements.txt
├── Procfile
│
├── static/
│   ├── css/
│   └── uploads/
│
├── templates/
│   ├── home.html
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── chat.html
│   ├── notifications.html
│   └── ...
│
└── README.md
```

---

## ⚙ Installation

Clone the repository

```bash
git clone https://github.com/malavikas-dev/CampusConnectAI.git
```

Move into the project

```bash
cd CampusConnectAI
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the environment

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python app.py
```

Open your browser

```
http://127.0.0.1:5000
```

---

## 📸 Screenshots

Add screenshots of:

- Home Page
- <img width="1920" height="1200" alt="Screenshot 2026-07-15 220304" src="https://github.com/user-attachments/assets/101030e0-4386-407b-a440-8745f869487e" />

- Login
- <img width="1920" height="1200" alt="Screenshot 2026-07-15 220513" src="https://github.com/user-attachments/assets/03ccebe1-c870-4cbb-977c-58c320593667" />

- Dashboard
- <img width="1920" height="1140" alt="Screenshot 2026-07-15 220555" src="https://github.com/user-attachments/assets/e3d3a15d-b877-4468-9993-87d662b7eab0" />

- Lost Item Details
- <img width="1920" height="1140" alt="Screenshot 2026-07-15 221136" src="https://github.com/user-attachments/assets/1ac1cf62-f4bc-4b49-8025-4ff486260117" />

- Notification
- <img width="1920" height="1140" alt="Screenshot 2026-07-15 221438" src="https://github.com/user-attachments/assets/9557b547-0b80-402a-b97d-0dba602299d5" />

- AI Match Suggestions
- <img width="1920" height="1140" alt="Screenshot 2026-07-15 221408" src="https://github.com/user-attachments/assets/9936787c-379a-4fce-90fd-435257ad4e92" />

- Private Chat
- <img width="1920" height="1140" alt="Screenshot 2026-07-15 220608" src="https://github.com/user-attachments/assets/823ebf81-6b83-4541-9b18-ec68c2ac510e" />

- Admin Dashboard
- <img width="1920" height="1200" alt="Screenshot 2026-07-15 220913" src="https://github.com/user-attachments/assets/e32255b7-91a6-44cd-a19f-bce8c9de0082" />
- <img width="1920" height="1140" alt="Screenshot 2026-07-15 220926" src="https://github.com/user-attachments/assets/0aaadcf2-6607-450b-b9e2-50c575694308" />


---

## 🔮 Future Improvements

- Image similarity using AI
- Real-time chat with WebSockets
- Push notifications
- Google Maps integration
- QR code-based item recovery
- Progressive Web App (PWA)
- Mobile application
- PostgreSQL support

---

## 👩‍💻 Developer

**Malavika S**

B.Tech Computer Science Engineering Student

GitHub: https://github.com/malavikas-dev

---

## 📄 License

This project is developed for educational and portfolio purposes.

---

## ⭐ Support

If you found this project helpful, consider giving it a ⭐ on GitHub!
