# BPC170 Study Mod

An interactive quiz application for studying BPC170 course material with module-based question selection.

## Features

- Select specific modules to study
- 766 questions across 9 modules
- Modern, responsive UI
- Progress tracking
- Instant feedback on answers

## Local Development

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Populate the database:
   ```bash
   python data/populate_db.py
   ```
5. Run the application:
   ```bash
   python run.py
   ```
6. Open http://localhost:5000 in your browser

## Render Deployment

### Setup Instructions

1. **Connect Repository to Render:**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `TechWorksAZ/BPC170_StudyMod`

2. **Configure Build Settings:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn run:app`
   
   **Note:** The database will be automatically populated on first startup by `run.py`. No need to run `populate_db.py` during the build.

3. **Environment Variables (Optional but Recommended):**
   - Add `SECRET_KEY` environment variable with a secure random string
   - You can generate one with: `python -c "import secrets; print(secrets.token_hex(32))"`

4. **Deploy:**
   - Click "Create Web Service"
   - Render will automatically build and deploy your app

### Important Notes

- The database will be automatically populated during the build process
- The app uses SQLite stored in the `instance` folder
- Make sure `data/questions.csv` is committed to the repository
- The app will automatically populate the database on first run if it's empty

## Module Information

- **Module 2:** Installing Motherboards & Connectors (63 questions)
- **Module 3:** Installing System Devices (108 questions)
- **Module 4:** Troubleshooting PC Hardware (101 questions)
- **Module 5:** Comparing Local Networking Hardware (110 questions)
- **Module 6:** Configuring Addressing & Internet Connections (129 questions)
- **Module 7:** Supporting Network Services (46 questions)
- **Module 8:** Summarizing Virtualization & Cloud Concepts (30 questions)
- **Module 9:** Supporting Mobile Devices (88 questions)
- **Module 10:** Supporting Print Devices (91 questions)

## Technology Stack

- **Backend:** Flask (Python)
- **Database:** SQLite with SQLAlchemy ORM
- **Frontend:** HTML, CSS, JavaScript
- **Deployment:** Gunicorn (WSGI server)

