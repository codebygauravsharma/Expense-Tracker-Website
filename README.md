Here’s the updated README to reflect your use of PostgreSQL:

---

# Expense Management Website

This is a Django-based web application for managing personal income, expenses, and user preferences. The project is designed to help users track their financial data efficiently, providing a simple and user-friendly interface.

## Features
- **Authentication**: Secure user login and registration.
- **Expense Tracking**: Log and categorize expenses.
- **Income Tracking**: Track and manage sources of income.
- **User Preferences**: Set and update preferences, such as currency options.
- **Dynamic UI**: Uses static files like HTML, CSS, and JavaScript for an interactive and responsive design.

## Project Structure
```
├── authentication/      # Handles user authentication (login, registration)
├── expenseapp/          # Core functionality for managing expenses
├── expenseswebsite/     # Django project settings and configurations
├── static/              # Static assets (CSS, JS, images)
├── templates/           # HTML templates for rendering views
├── userincome/          # Manages income-related features
├── userpreferences/     # Handles user-specific settings like currency preferences
├── .env                 # Environment variables (should not be pushed to GitHub)
├── currencies.json      # Stores currency data for user preferences
├── db.sqlite3           # Default SQLite database (can be replaced with PostgreSQL)
├── manage.py            # Django management script
├── requirements.txt     # Python dependencies for the project
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/codebygauravsharma/Expense-Tracker-Website.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Expense-Tracker-Website
   ```
3. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # For Linux/macOS
   venv\Scripts\activate      # For Windows
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Configure the PostgreSQL database:
   - Update the `.env` file with your PostgreSQL credentials:
     ```
     SECRET_KEY=your-secret-key
     DEBUG=True
     DATABASE_URL=postgres://username:password@localhost:5432/your_database_name
     ```
   - Replace `username`, `password`, `localhost`, and `your_database_name` with your PostgreSQL details.

6. Apply migrations:
   ```bash
   python manage.py migrate
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Usage

1. Open the web browser and go to `http://127.0.0.1:8000/`.
2. Register or log in to access the features.
3. Use the navigation bar to manage your expenses, income, and preferences.

## Environment Variables

The project uses a `.env` file for storing sensitive data. Example `.env` format:
```
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=postgres://username:password@localhost:5432/your_database_name
```

## Technologies Used
- **Backend**: Python, Django
- **Frontend**: HTML, CSS, JavaScript
- **Database**: PostgreSQL
- **Version Control**: Git


## License
This project is licensed under the [MIT License](LICENSE).

---
