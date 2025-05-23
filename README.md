# Super App Project Roadmap (23rd May - 28th May)

## Team Members & Responsibilities

* **Ashish (Frontend)**: React Native App UI & Navigation
* **Bhargavee (Integration)**: SDK development, MiniApp integration
* **Hritesh (Backend)**: Node.js backend, APIs, DB, and security

---

## GitHub Repo Initialization

### Folder Structure Skeleton

```
/super-app
├── README.md
├── /mobile-app
│   ├── App.js
│   ├── /screens
│   │   ├── LoginScreen.js
│   │   ├── RegisterScreen.js
│   │   ├── HomeScreen.js
│   │   └── KYCUploadScreen.js
│   ├── /components
│   ├── /navigation
│   │   └── AppNavigator.js
│   └── /assets
├── /backend
│   ├── server.js
│   ├── /routes
│   │   ├── authRoutes.js
│   │   ├── kycRoutes.js
│   │   └── chatRoutes.js
│   ├── /controllers
│   ├── /models
│   └── /middlewares
├── /sdk
│   ├── auth.js
│   ├── chat.js
│   ├── payments.js
│   └── permissions.js
└── /mini-apps
    └── demo-app
```

### Branch Strategy

* `main`: Production-ready code
* `frontend`: Ashish's working branch
* `integration`: Bhargavee’s SDK & integration work
* `backend`: Hritesh’s backend work

### README.md (Basic Content)

````md
# 🚀 Super App Prototype

A feature-rich React Native Super App with real-time chat, payments, mini-app SDK, admin panel, and AI assistant.

## Features
- 🔐 User Authentication & KYC
- 💬 Real-time Encrypted Messaging
- 💸 Payment Integration (UPI, Cards)
- 🧠 AI-powered Finance Agent
- 📲 Mini-app Ecosystem
- 🔧 Admin Controls
- 🛡️ Privacy Dashboard

## Tech Stack
- Frontend: React Native, Redux, React Navigation
- Backend: Node.js, Express.js, MongoDB
- Real-time: Socket.IO
- AI: TensorFlow Lite / PyTorch Mobile
- Cloud: Firebase / AWS

## Getting Started
```bash
git clone https://github.com/your-username/super-app.git
cd super-app

# Start React Native App
cd mobile-app
npm install
npm start

# Start Backend (in another terminal)
cd backend
npm install
node server.js
````

## Contribution

* Create feature branches off `main`
* Use clear commit messages
* Submit PRs to respective branches (`frontend`, `backend`, `integration`)

```

---

## Day-Wise Task Distribution

### ■ Day 1: 23rd May - Project Initialization & UI Skeletons

**Ashish:**
- Initialize React Native app (Expo or CLI)
- Set up React Navigation
- Create screens:
  - Login / Register
  - KYC Upload
  - Home (Tabs: Chat, Pay, MiniApps)

**Bhargavee:**
- Set up SDK folder structure (`auth.ts`, `chat.ts`, `payments.ts`, etc.)
- Implement basic auth SDK functions: `getUser()`, `isLoggedIn()`
- Plan SDK usage from MiniApps

**Hritesh:**
- Initialize Node.js + Express backend
- Setup MongoDB (Mongoose)
- Implement `/auth/register` and `/auth/login` with JWT
- Add basic `/user` schema with KYC fields

... *(remaining content unchanged)* ...

```
