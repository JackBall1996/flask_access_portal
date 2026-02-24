# Project

<b>What we want</b>

We want a single, easy-to-use web application that manages the full process from requesting access to datasets to revocation.

<b>In this new system:</b>
- Users log in and fill in a request form, choosing the dataset, access type, purpose, and confirming training completion.
- A rules engine decides:
    - Non-sensitive datasets → approve automatically (self-service).
    - Sensitive datasets → send to an approver’s dashboard for review.
- Approvers can see all pending requests, approve/reject with a reason, and the system updates the database automatically.
- Permissions can expire automatically and be revoked without manual action.
- All actions are logged in an audit trail for compliance and review.

<b>Expected benefits:</b>
- Faster access for users.
- No manual file handling.
- Clear visibility of who has access to what.
- Easy to change approval rules without editing scripts.
- Complete audit trail for governance.

<b>For this student project</b>

The aim is to build a prototype of this portal. For the purposes of the project:
- It will use a relational database (PostgreSQL) to store users, datasets, requests, rules, and logs.
- No real data will be used — only test datasets and fictional user accounts.
- The focus will be on core features: requesting, approving, granting/revoking access, and logging actions.

<u><b>MoSCoW Requirements</b></u>

<b>Must Have (MVP for prototype)</b>
- User login and authentication (simple username/password acceptable for prototype).
- Request form for dataset access, capturing:
    - Dataset name
    - Access type (Sensitive, Non-sensitive)
    - Purpose of request
    - Confirmation of training completion
- Rules-based decision-making:
    - Automatically approve non-sensitive datasets (self-service).
    - Route sensitive dataset requests to an approver queue.
- Automatic permission granting/revocation in the database based on decisions.
- Basic admin interface to manage datasets, sensitivity classification, and approval rules.
- Access expiry dates with automatic revocation on expiry. Every request will expire in 6 months; every renewal will extend current access for 6 months (but can only occur if the person has valid current access).

<b>Should Have</b>
- Search and filter functionality for requests, approvals, and active permissions.
- CSV export of audit logs and current permissions.
- Basic accessibility features (keyboard navigation, labelled form fields).
- Audit trail logging every request, decision, and permission change.
- Approver dashboard showing pending requests with approve/reject actions and reason capture.

<b>Could Have</b>
- Email notifications (approval, rejection, expiry warnings).
- Training validation check (e.g., mock expiry date on user profile).
- Role templates for datasets (predefined sets of permissions).
- Bulk actions for approving/revoking multiple requests.

<b>Won’t Have (Out of scope for this module)</b>
- Integration with live UKHSA systems.
- Corporate single sign-on (SSO) integration.
- Real personal or sensitive data.
- Production-ready security, scaling, or hosting setup.

## Flask

Flask is a lightweight, open-source Python micro web framework designed for building web applications, APIs, and microservices. Flask will be used in this project to build the web application.

[Getting Started with Flask: A Beginner’s Guide to Web Development](https://medium.com/@fabiomiguel_69727/getting-started-with-flask-a-beginners-guide-to-web-development-a9d463ee0c3f) will be used in the initial stages of this project.