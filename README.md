# Replit Bill Management Project

## Overview
This project is a **bill management system** that allows users to:
- Upload bill records from a spreadsheet.
- View, search, and filter bills based on sponsors, cosponsors, and tracker status.
- Hide and unhide bills from the user's view without deleting them.
- Use Prisma for database management.
- Use Flask for the web interface.
- Manage relations visually using **Prisma Studio**.
- Generate **Entity Relationship Diagrams (ERD)**.
- Deploy on **Shared Hosting Servers** (Apache/Nginx) without Supabase.

## Setup Instructions (Replit or Local Server)
### **1. Clone the Repository**  
```sh
git clone <your-repo-url>
cd replit_project
```

### **2. Install Dependencies**  
```sh
pip install flask prisma pandas
npm install -g prisma prisma-erd-generator
```

### **3. Apply Prisma Schema**  
```sh
npx prisma migrate dev --name init_schema
npx prisma generate
```

### **4. Import Bill Data**  
```sh
python import_bills.py
```

### **5. Start Prisma Studio (GUI for Managing Database)**  
```sh
npx prisma studio
```
- Use this to **view and manage database relations**.

### **6. Generate ERD Diagram (Entity Relationship Diagram)**  
```sh
npx prisma-erd-generator
```
- This will generate `prisma/ERD.svg`, which visually represents table relationships.

### **7. Start the Flask App (Development Mode)**  
```sh
python app_hide.py
```
- Open `http://localhost:5000` in your browser.

---

## **Deployment on Shared Hosting (Apache/Nginx + MySQL)**
### **1. Upload Project Files to Server**
- Copy all files **except `dev.db` (SQLite)** to your server.
- Ensure your server supports **Python, Flask, MySQL/PostgreSQL**.

### **2. Set Up MySQL Database (If Using MySQL Instead of SQLite)**
- Modify `prisma/schema.prisma` to use MySQL instead of SQLite:
  ```prisma
  datasource db {
    provider = "mysql"
    url      = env("DATABASE_URL")
  }
  ```
- Set up your **database credentials** in `.env`:
  ```sh
  DATABASE_URL="mysql://username:password@your-host/database-name"
  ```

### **3. Install Dependencies on Server**
```sh
pip install flask prisma pandas mysql-connector-python
npm install -g prisma prisma-erd-generator
```

### **4. Apply Prisma Schema for MySQL**
```sh
npx prisma migrate deploy
npx prisma generate
```

### **5. Run Flask App in Production Mode**
```sh
gunicorn -w 4 -b 0.0.0.0:8000 app_hide:app
```

- Configure **Apache/Nginx Reverse Proxy** to direct traffic to `http://localhost:8000`.

### **6. Set Up Auto Start (Systemd)**
Create `/etc/systemd/system/flask_app.service`:
```
[Unit]
Description=Gunicorn instance to serve Flask app
After=network.target

[Service]
User=your-user
Group=www-data
WorkingDirectory=/path-to-project
ExecStart=/usr/bin/gunicorn --workers 4 --bind 0.0.0.0:8000 app_hide:app

[Install]
WantedBy=multi-user.target
```
Enable and start the service:
```sh
sudo systemctl enable flask_app
sudo systemctl start flask_app
```

---

## **File Structure**
```
replit_project/
│── schema.prisma        # Prisma database schema
│── app_hide.py          # Flask backend with hide/unhide functionality
│── index_hide.html      # Web interface
│── bills_formatted.csv  # Formatted bill data from spreadsheet
│── import_bills.py      # Script to import CSV into Prisma database
│── README.md            # Instructions for setup
```

## **Alternative GUI Tools for Managing Database Relations**
If you need **drag-and-drop relations**, use:
- **Beekeeper Studio** (SQLite, PostgreSQL, MySQL) → [https://www.beekeeperstudio.io](https://www.beekeeperstudio.io)
- **DBeaver** (Advanced relations) → [https://dbeaver.io](https://dbeaver.io)
- **TablePlus** (User-friendly GUI) → [https://tableplus.com](https://tableplus.com)

Now you can **visually manage relationships, view data, and modify records easily**.
