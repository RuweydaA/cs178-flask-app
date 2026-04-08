# Ruweyda Abdi

**CS178: Cloud and Database Systems — Project #1**
**Author:** [Ruweyda Abdi]
**GitHub:** [RuweydaA]

---

## Overview

my project is a web application made with flask that connects both a MYSQL RDS and a DynamoDB databse.
Users can be addded, viewed, updated, deleted and there is an additonal employee-customer disrectory is also there from the chinook database. 

---

## Technologies Used

- **Flask** — Python web framework
- **AWS EC2** — hosts the running Flask application
- **AWS RDS (MySQL)** — relational database for [describe what you stored]
- **AWS DynamoDB** — non-relational database for [describe what you stored]
- **GitHub Actions** — auto-deploys code from GitHub to EC2 on push

---

## Project Structure

```
cs178-flask-app/
├── flaskapp.py          # Main Flask application — routes and app logic
├── dbCode.py            # Database helper functions (MySQL connection + queries)
├── templates/
│   ├── home.html.       # Landing page
│   ├── add_user.html
│   ├── delete_user.html
│   ├── update_user.html
│   ├── display_users.html
│   ├── employee_customer.html
├── .gitignore.          # Excludes creds.py and other sensitive files
└── README.md
```


## How to Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/RuweydaA/cs178-flask-app
   cd cs178-flask-app
   ```

2. Install dependencies:

   ```bash
   pip3 install flask pymysql boto3
   ```

3. Set up your credentials (see Credential Setup below)

4. Run the app:

   ```bash
   python3 flaskapp.py
   ```

5. Open your browser and go to `http://127.0.0.1:8080`

---

## How to Access in the Cloud

The app is deployed on an AWS EC2 instance. To view the live version:

```
http://52.91.21.245:8080/testdb
```

_(Note: the EC2 instance may not be running after project submission.)_

---

## Credential Setup

This project requires a `creds.py` file that is **not included in this repository** for security reasons.

Create a file called `creds.py` in the project root with the following format (see `creds_sample.py` for reference):

```python
# creds.py — do not commit this file
host = "your-rds-endpoint"
user = "admin"
password = "your-password"
db = "your-database-name"
```

---

## Database Design

### SQL (MySQL on RDS)

- `Employee` — stores employee info; primary key is `EmployeeId`
- `Customer` — stores customer info; foreign key `SupportRepId` links to Employee

JOIN query used:
```sql
SELECT Employee.FirstName, Employee.LastName, Employee.Title,
Customer.FirstName AS CustFirst, Customer.LastName AS CustLast
FROM Employee
JOIN Customer ON Employee.EmployeeId = Customer.SupportRepId
```


The JOIN query used in this project: The sql JOIN query is in the employee-customer route in flaskapp.py. it joins the employee and customer tables on supportrepid, which connects each customer to their assinged employee assistant.

### DynamoDB

- **Table name:** `[Users]`
- **Partition key:** `[UserID]`
- **Used for:** [storing user records with Name and Major]

---

## CRUD Operations

| Operation | Route | Description |
| --------- | ---------- | ----------------------------------------------------|
| Create | `/add-user` | Adds a new user to DynamoDB using|
| Read | `/display-users` | Retrieves all users from DynamoDB using|
| Update | `/update-user` | Updates a user's Major using `update_item()` |
| Delete | `/delete-user` | Removes a user from DynamoDB using `delete_item()`|

---

## Challenges and Insights

The bigges challenge was making sure the feild names in the HTML matched the named in the flask route. I kept forgetting to change it. 

---

## AI Assistance

<!-- List any AI tools you used (e.g., ChatGPT) and briefly describe what you used them for. Per course policy, AI use is allowed but must be cited in code comments and noted here. -->
