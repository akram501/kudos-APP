# Kudos Backend

This is the Django + DRF backend for the Kudos application.

---

## 🚀 Features

✅ JWT Authentication (djangorestframework-simplejwt)  
✅ Common architecture for Response and Error Handling  
✅ Custom user model with organization  
✅ Login with JWT  
✅ Give kudos to other users  
✅ List users in the same organization  
✅ See received kudos  
✅ Kudos remaining this week

---

## 📦 Tech Stack

- Python 3.13.2
- Django 5.1.7
- Django REST Framework 3.15.2
- PostgreSQL 14

## 🛠️ Setup & Run

1️⃣ Clone the repository
```bash
git clone https://github.com/akram501/kudos-APP.git
cd kudos-APP
```

2️⃣ Create virtual environment & activate
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3️⃣ Install requirements
```bash
pip install -r requirements.txt
```

4️⃣ Run migrations
```bash
python manage.py migrate
```

5️⃣ (Optional) Seed default data
```bash
python manage.py seed_data
```

6️⃣ Run the development server
```bash
python manage.py runserver
```

---

## ⚙️ Environment

- By default uses `sqlite3`.  
- Update `DATABASES` in `settings.py` for PostgreSQL.

---

## 🛡️ CORS

Allowed for `http://localhost:3000` for React.

## GIT

Set .env variable usign .envexample file
git user name : `akram501`
git access token : `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`