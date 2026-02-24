# MathφCafe

A full-stack **CBSE Student Management Platform** built with Flask for coaching institutes. Features an admin dashboard, student portal, and public-facing website.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1-000000?logo=flask)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?logo=bootstrap&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/shivupatilmaths/MathPhiCafe)

---

## Features

### Public Website
- **Home** page with hero section, stats counter, subject showcase, and testimonials
- **About** page with faculty profiles
- **Subjects** directory with detail pages and related batches
- **Faculty** directory with qualifications and specializations
- **Gallery** with category filtering and lightbox modal
- **Testimonials** with star ratings
- **Contact** form with message management

### Admin Dashboard
- **Student Management** — Add, edit, deactivate students; auto-generated IDs (`MPC-YEAR-###`) and passwords
- **Batch Management** — Create batches, assign faculty, enroll students
- **Result Tracking** — Record exam results with automatic grade calculation (A1–E)
- **Announcements** — Create targeted announcements by grade with priority levels
- **Gallery Management** — Upload images with automatic thumbnail generation
- **Faculty Management** — Manage teacher profiles with photos
- **Notes Management** — Upload and organize PDF study materials by subject and grade
- **Contact Messages** — Inbox for contact form submissions with read/unread tracking
- **Site Settings** — Configure site name, contact info, social media links, and Google Maps embed

### Student Portal
- **Dashboard** with announcements, enrolled batches, and recent results
- **Results** viewer with subject filtering and grade display
- **Notes** browser with downloadable PDFs filtered by grade
- **Schedule** viewer for enrolled batch timings
- **Profile** management with avatar upload and password change

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Flask 3.1, SQLAlchemy, Flask-Login, Flask-WTF, Flask-Migrate |
| **Database** | SQLite |
| **Frontend** | Jinja2, Bootstrap 5.3, Bootstrap Icons, AOS animations |
| **Fonts** | Poppins, Playfair Display (Google Fonts) |
| **Image Processing** | Pillow |

---

## Project Structure

```
MathφCafe/
├── run.py                  # App entry point
├── seed.py                 # Database seeder (admin + subjects)
├── config.py               # Configuration
├── requirements.txt        # Python dependencies
├── app/
│   ├── __init__.py         # App factory
│   ├── models.py           # 13 database models
│   ├── forms.py            # 12 WTForms classes
│   ├── utils.py            # Helpers & decorators
│   ├── extensions.py       # Flask extensions
│   ├── blueprints/
│   │   ├── public/         # 8 public routes
│   │   ├── auth/           # Login/logout
│   │   ├── admin/          # 33 admin routes
│   │   └── student/        # 6 student routes
│   ├── static/
│   │   ├── css/            # style.css + admin.css
│   │   ├── js/             # main.js
│   │   └── uploads/        # avatars, gallery, notes, thumbnails
│   └── templates/
│       ├── base.html       # Base layout + navbar + footer + macros
│       ├── errors/         # 404, 403, 500
│       ├── auth/           # Login page
│       ├── public/         # 8 public page templates
│       ├── admin/          # 21 admin templates + sidebar
│       └── student/        # 5 student templates
└── instance/
    └── mathphi.db          # SQLite database (auto-created)
```

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/shivupatilmaths/MathPhiCafe.git
cd MathPhiCafe
```

### 2. Create a virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Seed the database

```bash
python seed.py
```

This creates:
- **Admin account** — username: `admin`, password: `admin123`
- **5 default subjects** — Mathematics, Physics, Chemistry, Biology, Computer Science

### 5. Run the app

```bash
python run.py
```

Open **http://localhost:5000** in your browser.

---

## Default Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |

> Students are created through the admin panel. Each student receives an auto-generated ID and password.

---

## Database Models

| Model | Description |
|-------|-------------|
| `AdminUser` | Admin accounts with superadmin flag |
| `Student` | Student profiles with grade, parent info, avatar |
| `Subject` | Academic subjects (Math, Physics, Chemistry, etc.) |
| `Faculty` | Teacher profiles with qualifications |
| `Batch` | Class batches with schedule, faculty, and capacity |
| `BatchEnrollment` | Student-to-batch many-to-many enrollment |
| `Result` | Exam results with marks, percentage, and auto-grading |
| `Announcement` | Targeted announcements with priority levels |
| `GalleryImage` | Gallery photos with auto-generated thumbnails |
| `Note` | PDF study notes organized by subject and grade |
| `Testimonial` | Student testimonials with star ratings |
| `ContactMessage` | Contact form submissions with read tracking |
| `SiteSetting` | Key-value site configuration |

---

## Deployment

### Deploy to Render (Free)

Click the button below for one-click deployment:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/shivupatilmaths/MathPhiCafe)

Or deploy manually:

1. Create a [Render](https://render.com) account (free)
2. Click **New > Web Service** and connect your GitHub repo
3. Render auto-detects `render.yaml` and configures everything
4. The build script installs dependencies and seeds the database
5. Your app will be live at `https://mathphicafe.onrender.com`

> **Note:** On Render's free tier, the service spins down after 15 minutes of inactivity. The first request after inactivity may take ~30 seconds.

---

## Screenshots

> Run the app locally to explore the full UI. The design features a vibrant gradient theme with purple (#6C63FF), pink (#FF6584), and teal (#00C9A7) accent colors.

---

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is open source and available under the [MIT License](LICENSE).
