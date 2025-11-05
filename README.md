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
## License

This project is licensed under the [MIT License](LICENSE)
