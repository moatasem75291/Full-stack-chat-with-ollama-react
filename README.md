# Full-Stack Chat Application with Ollama and React

This repository contains a full-stack chat application built using Ollama for the backend and React for the frontend. The application allows users to interact with an AI assistant that provides helpful, respectful, and honest responses.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)

## Features

- Real-time chat interface with AI assistant
- Asynchronous streaming responses
- Chat history management
- Clear and concise responses with markdown formatting
- `FastAPI` backend with RESTful endpoints
- `React` frontend with a responsive UI

## Technologies Used

- **Backend:**

  - Python
  - FastAPI
  - Pydantic
  - Uvicorn
  - Llama Index (Ollama)

- **Frontend:**
  - React
  - Preact
  - ReactMarkdown
  - CSS

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn

### Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/moatasem75291/Full-stack-chat-with-ollama-react.git
   cd Full-stack-chat-with-ollama-react
   ```
2. Install backend dependencies:

   ```sh
   cd backend
   pip install -r requirements.txt
   ```

3. Install frontend dependencies:
   ```sh
   cd ../frontend
   npm install
   # or
   yarn install
   ```

### Running the Application

1. Start the backend server:

   ```sh
   cd backend
   uvicorn app:app --reload
   ```

2. Start the frontend development server:

   ```sh
   cd ../frontend
   npm start
   # or
   yarn start
   ```

3. Open your browser and navigate to:

   ```Code
   http://localhost:8000
   ```

## Project Structure

```css
Full-stack-chat-with-ollama-react/
├── backend/
│   ├── OllamaChat.py
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── test_ollamachat.py
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatInput.jsx
│   │   │   ├── ChatMessage.jsx
│   │   ├── pages/
│   │   │   ├── Chat.jsx
│   │   │   └── ErrorPage.jsx
│   │   ├── App.css
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   ├── .gitignore
│   ├── Dockerfile
│   ├── package-lock.json
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── .gitignore
├── LICENSE
├── run_project.py
└── README.md
```

## API Endpoints

### Chat Endpoint

- **URL:** `/chat`
- **Method:** `POST`
- **Description:** Send a message to the AI assistant and receive a response.
- **Request Body:**

  ```JSON
  {
  "message": "Your message here"
  }
  ```

- **Response:**
  - On success: Streaming response with the assistant's message.
  - On error: JSON object with error details.

### Get Chat History

- **URL:** `/get_history`
- **Method:** `GET`
- **Description:** Retrieve the chat history.
- **Response:**
  - On success: JSON object with the chat history.
  - On error: JSON object with error details.

### Clear Chat History

- **URL:** `/delete_history`
- **Method:** `DELETE`
- **Description:** Clear the chat history.
- **Response:**
  - On success: JSON object with a success message.
  - On error: JSON object with error details.

### Health Check

- **URL:** `/`
- **Method:** `GET`
- **Description:** Health check endpoint to verify the service is running.
- **Response:**
  - On success: JSON object with a health status message.
  - On error: JSON object with error details.

```text
Feel free to adjust the content according to your specific project details and requirements.
```
