LifeLink Blood Portal
A dynamic Google Apps Script web application to facilitate blood donation management, donor registration, blood requests, and real-time blood stock tracking.

Features
User Roles: Admin, Donor, Requester with role-based access.

Donor Registration: Secure donor signup with validation and sanitization.

Blood Requests: Submit and track urgent blood requests.

Dashboard: Real-time stats on donors, requests, and blood stock.

Donor Search: Admin-only paginated search by name, blood group, or city.

Authentication: User registration and secure login with hashed passwords.

Multi-page SPA: Content dynamically served based on URL parameters (?page=).

Theming: Dark and light mode toggle.

Pages Included: Home (dashboard), About, FAQs, Contact, Privacy Policy, Terms and Conditions, Disclaimer.

Backend: Google Sheets used as data backend for donors, requests, users, and stocks.

Input Sanitization: Protects against injection by cleaning user input.

Validation: Phone number format and required fields checked on server side.

Setup Instructions
Clone the repository or copy the project files to your local development environment.

Open the project in Google Apps Script Editor.

Update the SPREADSHEET_ID in Code.gs to point to your Google Sheets backend.

Create or verify the following sheets exist in your spreadsheet (case-sensitive):

Donors

Requests

BloodStock

Users

Deploy the project as a web app:

Click Deploy > New deployment.

Choose Web app.

Set access permissions and deploy.

Access the URL provided to use the portal.

Usage
Register users and donors via the frontend forms.

Submit blood requests and view donor availability.

Admin users can search donors and view dashboard stats.

Navigate between pages using the quick links (e.g., Home, About, FAQs).

Toggle between dark and light modes for better accessibility.

File Structure Highlights
Code.gs — Backend Google Apps Script code handling data logic, validation, routing, and authentication.

Index.html — Main SPA index page with navigation and dynamic content sections.

Other HTML files (About.html, Faq.html, Contact.html, etc.) — Static pages served dynamically via doGet routing.

Security Notes
Basic input sanitization implemented on the server.

Passwords are hashed using SHA-256 before storage (note: suitable for demo, recommend stronger hashing with salt in production).

Role validation restricts sensitive operations.

Support and Contact
For issues, questions, or suggestions, contact:

Email: csds23134@glbitm.ac.in

Phone: +91 7755866281

