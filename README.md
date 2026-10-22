# ExpenseFlow — Personal Expense Tracker

## 1. Project Overview

ExpenseFlow is a web-based Personal Expense Tracker developed using Python Flask. It allows users to record, manage, and analyze their daily expenses through an interactive dashboard.

The project also demonstrates an automated Continuous Integration and Continuous Deployment (CI/CD) pipeline using GitHub, Jenkins, Docker, Docker Hub, and Kubernetes.

## 2. Objectives

- Develop a functional expense tracking web application.
- Implement automated testing using pytest.
- Maintain application source code using Git and GitHub.
- Automate application builds and testing using Jenkins.
- Containerize the application using Docker.
- Publish Docker images to Docker Hub.
- Deploy the application using Kubernetes (Minikube).
- Automatically deploy updated application versions through a CI/CD pipeline.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| SQLite | Expense data storage |
| HTML, CSS, JavaScript | Frontend development |
| Chart.js | Expense visualization |
| pytest | Automated testing |
| Git and GitHub | Version control and source repository |
| Jenkins | CI/CD automation |
| AWS EC2 | Jenkins server hosting |
| Docker | Application containerization |
| Docker Hub | Container image registry |
| Kubernetes | Container orchestration |
| Minikube | Local Kubernetes cluster |
| kubectl | Kubernetes management |

## 4. Application Features

ExpenseFlow provides:

- Add new expenses with relevant details.
- View and manage recorded expenses.
- Delete expenses.
- Filter expenses by month.
- Visualize spending using charts.
- Store expense records in an SQLite database.
- Check application health and version through the `/health` endpoint.

## 5. Project Structure

```text
personal_expense_tracker/
├── app.py
├── database.py
├── requirements.txt
├── Dockerfile
├── .docker