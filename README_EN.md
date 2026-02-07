# 🏳️‍🌈 GenderPrism / PrismaDeGênero

Welcome to the **GenderPrism** repository (known as **PrismaDeGênero** in Portuguese). This is an open-source educational platform dedicated to gender literacy, diversity, and inclusion.

Our goal is to deconstruct prejudices and build a more equal society through accessible education.

## 🚀 About the Project

**GenderPrism** is a full-stack web application that offers courses, educational materials, and a safe community for learning about gender identity, sexuality, and human rights.

### ✨ Key Features

*   **Multilingual**: Full support for Brazilian Portuguese (pt-BR) and English (en-US).
*   **"Prism" Visual Identity**: Modern design based on color spectrum and glassmorphism.
*   **Course Management**: Course listing with prices and descriptions.
*   **Enrollment System**: Users can enroll and track progress (Dashboard).
*   **Secure Authentication**: Login (Username/Email) and Registration with differentiated permissions (Admin vs Student).
*   **Student Dashboard**: Visual progress tracking and course history.

## 🛠️ Technologies Used

### Backend (API)
*   **Python 3**
*   **Django REST Framework**: For building a robust API.
*   **SQLite**: Default database (can be migrated to PostgreSQL).

### Frontend (Interface)
*   **Vue.js 3**: Reactive JavaScript framework (Composition API).
*   **Vite**: Ultra-fast build tool.
*   **Tailwind CSS**: Utility-first CSS framework.
*   **Vue Router & Pinia**: Routing and state management.
*   **Vue I18n**: Internationalization.

---

## ⚙️ How to Run the Project

Follow the steps below to run the project locally on your machine.

### Prerequisites
*   Node.js (v16+) and npm
*   Python (v3.8+) and pip

### 1. Setting up the Backend (Django)

```bash
# Enter the backend folder
cd backend

# Create a virtual environment (optional, but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python3 manage.py migrate

# Create a superuser (to access admin and create courses)
python3 manage.py createsuperuser

# Start the server
python3 manage.py runserver
```

The backend will be running at: `http://localhost:8000`

### 2. Setting up the Frontend (Vue.js)

```bash
# Open a new terminal and enter the frontend folder
cd frontend

# Install Node dependencies
npm install

# Start the development server
npm run dev
```

The frontend will be running at: `http://localhost:5173` (or similar port indicated in the terminal).

---

## 🤝 How to Contribute

This is a public and collaborative project! We greatly appreciate your help to make it even better. Whether fixing bugs, adding new features, improving documentation, or translating content.

### Contribution Guide

1.  **Fork** this repository.
2.  **Clone your Fork** to your local machine.
    ```bash
    git clone https://github.com/YOUR_USERNAME/GenderSchool.git
    ```
3.  **Create a Branch** for your feature or fix.
    ```bash
    git checkout -b feature/my-new-feature
    ```
4.  **Make the changes** and commit.
    ```bash
    git commit -m "feat: Add new feature X"
    ```
5.  **Push to your repository**.
    ```bash
    git push origin feature/my-new-feature
    ```
6.  **Open a Pull Request (PR)** in the original repository.
    *   Describe in detail what was done.
    *   If possible, attach screenshots or videos.

### What can you do?
*   🐛 **Report Bugs**: Open an Issue describing the problem.
*   💡 **Suggest Improvements**: Have a cool idea? Open an Issue to discuss.
*   📝 **Improve Documentation**: Help make this README or the code clearer.
*   🌍 **Translation**: Help add new languages.

---

## 📄 License

This project is under the MIT license. Feel free to use, modify, and distribute.

---

<p align="center">
  Made with 🏳️‍🌈 and ❤️ by the <strong>GenderPrism</strong> community.
</p>
