# GUVI AWS 3-Tier Architecture Project

## Overview

This project demonstrates a three-tier web application architecture on Amazon Web Services (AWS). It separates the web entry point, application processing, and database storage into distinct layers to improve security, maintainability, and scalability.

## Architecture

```text
Users
  |
  v
Public Application Load Balancer
  |
  v
Web Tier
Web-A (Nginx / reverse proxy / jump host)
  |
  v
Private Application Tier
App-A (Flask)     App-B (Flask)
  |                    |
  +---------+----------+
            |
            v
       RDS MySQL
       Database Tier
```

*The diagram is conceptual. Actual traffic paths depend on the configured load balancers, target groups, listeners, and security groups.*

## AWS Components

- **VPC:** Provides network isolation for project resources.
- **Public subnet:** Hosts the public-facing entry point and any required jump-host resources.
- **Private subnets:** Host application instances that should not be directly exposed to the internet.
- **Application Load Balancer (ALB):** Routes incoming requests to registered targets according to its listener and target-group configuration.
- **Web tier:** Uses Nginx as a reverse proxy where configured.
- **Application tier:** Runs the Flask applications on EC2 instances.
- **Database tier:** Uses Amazon RDS for MySQL to store application data.
- **Security groups:** Control network access between the tiers.

## Repository Structure

```text
GUVI-AWS-3-Tier-Architecture/
├── app.py
├── requirements.txt
├── index.html
├── nginx.conf
├── App.md
├── DB.md
├── proxy.md
└── app-a/
    ├── app.py
    ├── requirements.txt
    ├── index.html
    ├── nginx.conf
    ├── App.md
    ├── DB.md
    └── proxy.md
```

The root application files represent App-B, while the `app-a/` directory contains App-A's application files and documentation.

## Application Features

The Flask applications provide a health endpoint and a feedback submission endpoint.

- `GET /` — Returns a JSON health response.
- `POST /submit` — Accepts JSON containing `name`, `email`, and `feedback`, then inserts the feedback into MySQL when the database connection and table are configured correctly.

Example request body:

```json
{
  "name": "Test User",
  "email": "test@example.com",
  "feedback": "Testing the feedback application"
}
```

Example health response:

```json
{
  "status": "Flask is running"
}
```

## Configuration and Environment Variables

Database credentials should be provided through environment variables rather than hardcoded in application source code.

| Variable | Purpose |
|---|---|
| `DB_HOST` | RDS endpoint or database hostname |
| `DB_USER` | MySQL username |
| `DB_PASSWORD` | MySQL password |
| `DB_NAME` | Database name |

For local development, a `.env` file may be used if `python-dotenv` is installed. Do not commit `.env` files, passwords, access tokens, private keys, or other secrets to GitHub.

## Installation

Run the commands on the application instance where the relevant application files are deployed.

For App-B:

```bash
cd ~/studentapp
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

For App-A, use its deployed application directory and its corresponding `requirements.txt`.

Configure the required environment variables before starting the application. Do not put real credentials in this README.

## Testing

Check the health endpoint locally on the application instance:

```bash
curl http://127.0.0.1:5000/
```

Test feedback submission:

```bash
curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","feedback":"Test feedback"}'
```

A successful submission should return a success response. Confirm the record in MySQL separately if database persistence needs to be verified.

Test the application through the appropriate load balancer or web endpoint after confirming the listener rules, target health, Nginx configuration, and security-group rules.

## Security Considerations

- Keep application instances in private subnets where appropriate.
- Restrict SSH access to trusted sources and use a jump host where required.
- Allow only necessary traffic between the web, application, and database tiers.
- Restrict database access to the required application security group.
- Store credentials outside source control.
- Never publish AWS access keys, GitHub tokens, private SSH keys, or database passwords.

## Project Status

This repository contains the application code and documentation for the App-A and App-B components. Confirm the AWS resource configuration and end-to-end connectivity in your AWS account before treating the complete architecture as production-ready.

## Author

Naveen
