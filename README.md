
# MintTenantCore – FastAPI Multi-Tenant Backend

This is the backend API for the **MintTenantCore** platform, a multi-tenant, role-based access control system built using **FastAPI** and **Firebase Authentication**. The system supports separate branding, feature flags, and layouts for each tenant.

---

## 🚀 Deployment

- **Live URL:** https://mint-tenant-core-back-end.onrender.com  
- **Hosting Platform:** [Render](https://render.com)

---

## 🛠 Tech Stack

| Layer        | Technology             |
| ------------ | ---------------------- |
| Backend      | FastAPI                |
| Auth         | Firebase Authentication |
| DB (optional)| Firestore              |
| Storage      | File-based JSON (`tenants.json`) |
| Deployment   | Render                 |
| CSS/Frontend | Tailwind (React-based client) |
| Testing      | Pytest (optional)      |

---

## 🧪 Getting Started

### 💡 Setup Guidelines (Local)

> Recommended for development/testing

1. **Clone the repo:**

   ```bash
   git clone https://github.com/your-org/minttenantcore-backend.git
   cd minttenantcore-backend
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables:**

   Create a `.env` file in the root directory:

   ```env
   HOST=0.0.0.0
   PORT=8000
   JWT_SECRET_KEY=your_secret_here
   JWT_ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   ALLOWED_ORIGINS=http://localhost:3000
   ```

5. **Run the application:**

   ```bash
   uvicorn main:app --reload
   ```

6. **API Docs:**

   - Swagger UI: [https://mint-tenant-core-back-end.onrender.com/docs](http://localhost:8000/docs)
   - ReDoc: [https://mint-tenant-core-back-end.onrender.com/redoc](http://localhost:8000/redoc)

---

### 🧩 Firebase Setup

If you’re using Firebase Auth:

1. Go to the [Firebase Console](https://console.firebase.google.com)
2. Create a project and enable **Authentication**
3. Download the `firebase-adminsdk.json` service account key
4. Reference it in your app (e.g., `FIREBASE_CREDENTIALS_PATH=...`)
5. Ensure Firestore contains a `users` collection with `{ role, tenant }` metadata

---

## 🔐 Authentication

All protected endpoints require a valid Firebase **ID token** in:

```
Authorization: Bearer <id_token>
```

User roles are determined by Firestore metadata (e.g., `Admin`, `HR`, `Employee`).

---

## 📦 Key API Endpoints

| Method | Endpoint               | Role     | Purpose                     |
|--------|------------------------|----------|-----------------------------|
| GET    | `/auth/me`             | Any      | Get current user info       |
| POST   | `/tenant/create`       | Admin/HR | Create new tenant           |
| GET    | `/tenant/config`       | Any      | Get tenant config           |
| PUT    | `/tenant/config`       | Admin/HR | Update tenant branding      |
| GET    | `/tenant/features`     | Any      | Get enabled features        |
| PUT    | `/tenant/features`     | HR       | Update features flags       |

---

## 📌 Roadmap / Improvements

- 🔄 Switch file storage (`tenants.json`) to Firestore
-  🎛  Admin panel for managing users, tenants, flags
- 🧪 Add test suite with coverage reports (pytest + httpx)
- 🔒 Refresh token blacklisting (future-ready)
- 🌍 Multi-language (i18n) support
- ⚡ Feature toggle caching and prefetching
- 📊 Feature usage analytics (optional)

---

## 🧑‍💻 Contributing

Pull requests welcome!

```bash
   git checkout -b my-feature
   git commit -m "Add feature"
   git push origin my-feature
```

---

## 👥 Author

Made with ❤️ by Naveen Kumar  
Contact: naveenjs.be@gmail.com
