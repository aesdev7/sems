# sems
A Security Management System.
                      +--------------------------------------+
                      |      External Systems                |
                      | (Airports, Law Enforcement, etc.)    |
                      +----------------+-----------------------+
                                       │
                                       ▼
                +--------------------------------------+
                |          User Interface              |
                |      (Web & Mobile Applications)     |
                +----------------+-----------------------+
                                       │
                                       ▼
                +--------------------------------------+
                |  Authentication & Authorization      |
                |   (SSO, RBAC, Multi-Factor Auth)       |
                +----------------+-----------------------+
                                       │
                                       ▼
                +--------------------------------------+
                |         API Gateway / Service Layer  |
                +----------------+-----------------------+
                                       │
                    ┌──────────────────┴───────────────────┐
                    │                                      │
           +--------▼---------+                  +---------▼----------+
           |   Incident       |                  |  Threat & Risk     |
           |   Reporting      |                  |  Assessment        |
           |   Module         |                  |  Module            |
           +------------------+                  +--------------------+
                    │                                      │
                    ├──────────────┐           ┌───────────┤
                    ▼              ▼           ▼           ▼
         +----------------+   +--------------+   +----------+   +--------------+
         | Passenger &    |   | Cargo &      |   | Compliance &   | Data Analytics|
         | Baggage        |   | Supply Chain |   | Audit Module   | & Reporting   |
         | Screening      |   | Security     |   |                | Module        |
         +----------------+   +--------------+   +---------------+---------------+
                                       │
                                       ▼
                           +-----------------------------+
                           | Notification & Alerting     |
                           |       Module                |
                           +-----------------------------+
                                       │
                                       ▼
                           +-----------------------------+
                           | External Integration / APIs |
                           +-----------------------------+



HERE IS A SAMPLE CODE TO BE REVIWED.
This is designed specifically around IOSA Security Section No.8. The focus is on security incident management, risk assessment, compliance auditing, and training—key elements emphasized by IOSA in this section. The simulation includes an API gateway that routes requests to IOSA‑specific modules:

import sqlite3
import datetime

# User Database using SQLite
class UserDatabase:
    def __init__(self, db_path="users.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.create_users_table()
        self.populate_sample_users()

    def create_users_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                role TEXT
            )
        ''')
        self.conn.commit()

    def populate_sample_users(self):
        # Insert sample users if they don't already exist
        cursor = self.conn.cursor()
        sample_users = [
            ("iosa_admin", "adminpass", "administrator"),
            ("security_staff", "staffpass", "security_officer")
        ]
        for username, password, role in sample_users:
            cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                    (username, password, role)
                )
        self.conn.commit()

    def get_user(self, username):
        cursor = self.conn.cursor()
        cursor.execute("SELECT username, password, role FROM users WHERE username=?", (username,))
        return cursor.fetchone()

    def close(self):
        self.conn.close()

# Authentication Module updated to use the User Database
class AuthenticationModule:
    def __init__(self, user_db: UserDatabase):
        self.user_db = user_db
    
    def login(self, username, password):
        user = self.user_db.get_user(username)
        if user:
            db_username, db_password, db_role = user
            if password == db_password:
                print(f"[Auth] User '{username}' authenticated as {db_role}.")
                return True
        print("[Auth] Authentication failed.")
        return False

# IOSA Incident Reporting Module (aligned with Section No.8 requirements)
class IOSAIncidentReportingModule:
    def __init__(self):
        self.incidents = []
    
    def report_incident(self, incident_details):
        # Append a timestamp to the incident details
        incident_details["timestamp"] = datetime.datetime.now().isoformat()
        self.incidents.append(incident_details)
        incident_id = len(self.incidents)
        print(f"[IOSA Incident] Reported incident {incident_id}: {incident_details}")
        return f"Incident ID: {incident_id}"

# IOSA Risk Assessment Module
class IOSARiskAssessmentModule:
    def assess_risk(self, data):
        # Assess risk based on provided severity following IOSA guidelines
        severity = data.get("severity", "low").lower()
        risk_mapping = {"low": "Low Risk", "medium": "Moderate Risk", "high": "High Risk"}
        risk_result = risk_mapping.get(severity, "Unknown Risk")
        print(f"[IOSA Risk] Threat assessment result: {risk_result}")
        return risk_result

# IOSA Compliance Audit Module
class IOSAComplianceAuditModule:
    def run_audit(self, _data=None):
        report = "IOSA Compliance Audit: All procedures meet Section No.8 standards."
        print(f"[IOSA Audit] {report}")
        return report

# Security Training Module to meet IOSA training and awareness requirements
class SecurityTrainingModule:
    def __init__(self):
        self.training_records = {}
    
    def record_training(self, staff_id, training_details):
        self.training_records[staff_id] = {
            "training_details": training_details,
            "date": datetime.datetime.now().isoformat()
        }
        print(f"[Training] Recorded training for {staff_id}: {training_details}")
        return f"Training recorded for {staff_id}"
    
    def check_training_compliance(self, staff_id):
        record = self.training_records.get(staff_id)
        if record:
            print(f"[Training] {staff_id} is compliant with training requirements.")
            return True
        print(f"[Training] {staff_id} is NOT compliant with training requirements.")
        return False

# Notification & Alerting Module
class NotificationModule:
    def send_alert(self, alert_info):
        recipients = alert_info.get("recipients", [])
        message = alert_info.get("message", "")
        print(f"[Notification] Alert sent to {', '.join(recipients)}: {message}")
        return "Alert sent"

# External Integration Module (e.g., notifying emergency services)
class ExternalIntegrationModule:
    def notify_external_agency(self, data):
        print(f"[External] Notifying external agency with data: {data}")
        return "External agency notified"

# API Gateway to route requests between modules
class APIGateway:
    def __init__(self, modules):
        # 'modules' is a dictionary mapping module names to module instances
        self.modules = modules
    
    def route_request(self, module_name, action, data):
        if module_name in self.modules:
            module = self.modules[module_name]
            func = getattr(module, action, None)
            if callable(func):
                print(f"[Gateway] Routing '{action}' to module '{module_name}'.")
                return func(data)
            else:
                print(f"[Gateway] Action '{action}' not found in module '{module_name}'.")
        else:
            print(f"[Gateway] Module '{module_name}' not available.")
        return None

# Main simulation demonstrating a sample use case based on IOSA Security Section No.8
if __name__ == "__main__":
    # Initialize the User Database and Authentication Module
    user_db = UserDatabase()
    auth_module = AuthenticationModule(user_db)
    
    # Initialize other modules
    incident_module = IOSAIncidentReportingModule()
    risk_module = IOSARiskAssessmentModule()
    audit_module = IOSAComplianceAuditModule()
    training_module = SecurityTrainingModule()
    notification_module = NotificationModule()
    external_module = ExternalIntegrationModule()
    
    # Map modules for the API Gateway
    modules = {
        "incident": incident_module,
        "risk": risk_module,
        "audit": audit_module,
        "training": training_module,
        "notification": notification_module,
        "external": external_module
    }
    api_gateway = APIGateway(modules)
    
    # Simulate user login from the database
    if auth_module.login("security_staff", "staffpass"):
        # 1. Report an incident following IOSA Section No.8 guidelines
        incident_details = {
            "incident_type": "Unauthorized Access",
            "location": "Terminal A - Restricted Area",
            "description": "An unauthorized individual was detected in a secure area.",
            "severity": "high"
        }
        incident_id = api_gateway.route_request("incident", "report_incident", incident_details)
        
        # 2. Assess the risk of the reported incident
        risk_result = api_gateway.route_request("risk", "assess_risk", {"severity": "high"})
        
        # 3. Record a mandatory training session for security staff
        training_info = {"topic": "IOSA Security Section No.8 Procedures", "duration": "2 hours"}
        training_status = training_module.record_training("security_staff", training_info)
        
        # 4. Check training compliance for the staff member
        training_compliance = training_module.check_training_compliance("security_staff")
        
        # 5. Run a compliance audit based on IOSA requirements
        audit_report = api_gateway.route_request("audit", "run_audit", None)
        
        # 6. Send a notification alert about the incident
        alert_info = {
            "recipients": ["security_lead@airport.com"],
            "message": f"High risk incident reported: {incident_id}. Immediate response required."
        }
        alert_status = api_gateway.route_request("notification", "send_alert", alert_info)
        
        # 7. Notify external agencies (e.g., emergency services) if needed
        external_status = api_gateway.route_request("external", "notify_external_agency",
                                                    {"incident_id": incident_id, "risk": risk_result})
    
    # Close the user database connection when done
    user_db.close()
