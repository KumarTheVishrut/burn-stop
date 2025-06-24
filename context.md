src/
├── app/
│   ├── (auth)/
│   │   ├── login/
│   │   │   └── page.jsx
│   │   └── signup/
│   │       └── page.jsx
│   ├── dashboard/
│   │   └── page.jsx      # Main dashboard
│   ├── organizations/
│   │   ├── create/
│   │   │   └── page.jsx
│   │   ├── [orgId]/
│   │   │   ├── services/
│   │   │   │   ├── new/
│   │   │   │   │   └── page.jsx
│   │   │   │   └── [serviceId].jsx
│   │   │   ├── users/
│   │   │   │   ├── add/
│   │   │   │   │   └── page.jsx
│   │   │   │   └── page.jsx
│   │   │   └── page.jsx  # Org details
│   │   └── page.jsx       # Org list
│   ├── reminders/
│   │   └── page.jsx       # Upcoming reminders
│   └── layout.jsx
├── components/
│   ├── ServiceCard.jsx
│   ├── ReminderAlert.jsx
│   └── OrgSidebar.jsx
└── lib/
    └── api.js            # API client



POST    /auth/login
POST    /auth/signup

POST    /organizations/          # Create org
GET     /organizations/          # List orgs (for user)
GET     /organizations/{org_id}  # Get org details

POST    /organizations/{org_id}/users    # Add user to org
DELETE  /organizations/{org_id}/users/{user_id}

POST    /organizations/{org_id}/services     # Add service
GET     /organizations/{org_id}/services     # List services
PUT     /services/{service_id}               # Update service
DELETE  /services/{service_id}               # Mark for deletion

GET     /organizations/{org_id}/reminders   # Upcoming reminders
POST    /reminders/{reminder_id}/acknowledge # Confirm action




backend/
├── main.py
├── requirements.txt
├── routers/
│   ├── __init__.py
│   ├── auth.py
│   ├── organizations.py
│   ├── services.py
│   └── reminders.py
├── models/
│   ├── user.py
│   ├── organization.py
│   └── service.py
└── utils/
    ├── security.py   # Password hashing
    └── redis_db.py   # Redis connection




redis



    user:<user_id> : {
  "email": "user@example.com",
  "hashed_password": "...",
  "organizations": [org_id1, org_id2]
}


org:<org_id> : {
  "name": "Org Name",
  "owner_id": "user_id",
  "created_at": "timestamp"
}


service:<service_id> : {
  "org_id": "org_id",
  "name": "AWS EC2",
  "type": "cloud/infra/subscription/api",
  "cost": 42.99,
  "created_at": "timestamp",
  "reminder_date": "2023-12-01",
  "status": "active/pending_deletion"
}


reminders:<org_id> : {
  score: UNIX_timestamp, 
  value: "service_id"
}
