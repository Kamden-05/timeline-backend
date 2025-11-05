# Timeline Backend (FastAPI + Python)

A Python backend API built with **FastAPI** to manage timelines and timeline events.  
This backend provides secure user accounts and allows users to create, edit, and manage timelines and events.

---

## Overview

The **Timeline Backend** serves as the backend for a timeline-based note-taking web app.  

**Key features:**
- User account creation and authentication.
- Create, read, update, and delete **timelines**.
- Create, read, update, and delete **timeline events**.
- Ensures that users can only access or modify their own timelines.
- Built to be consumed by the **Timeline Frontend Web App**.

**Future plans:**
  - Deployment to AWS Lambda + API Gateway
  - Public or private visibility settings for timelines.
  - Timeline sharing between users.
  - Timeline summary and search functionality
---

## Tech Stack

| Component      | Technology |
|----------------|------------|
| Framework      | FastAPI |
| Language       | Python 3.14 |
| Database       | PostgreSQL |
| ORM            | SQLModel |
| Authentication | JWT (JSON Web Tokens) |

---

Copyright 2025 Kamden Wilson

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
