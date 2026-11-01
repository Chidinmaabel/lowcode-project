# Customer Enquiry Tracker — Specification

## Purpose

The Customer Enquiry Tracker is designed for sole traders and small service businesses such as painters, tilers, plumbers and handymen. It helps them organise customer information, record enquiries and keep track of the progress of potential jobs so that enquiries are not forgotten.

## Entities

### Enquiry

- id (integer, primary key)
- customer_name (text, required, max 200)
- phone (text, required)
- email (text, required)
- service_type (text, optional)
- description (text, optional)
- status (one of: new, contacted, quote_sent, accepted, lost — default new)
- created_at (timestamp)
- follow_up_date (date, optional)

## Routes

| Method | Path | Does |
|---|---|---|
| GET | / | List all enquiries, newest first |
| GET | /enquiry/new | Display form to create an enquiry |
| POST | /enquiry | Validate and save a new enquiry, redirect to / |
| GET | /enquiry/<id> | Display one enquiry |
| POST | /enquiry/<id>/status | Change enquiry status, redirect back to the enquiry |

## Technical constraints

- Python 3.11+, Flask 3.x
- SQLite using Python's standard library sqlite3 (no ORM)
- Jinja2 templates in templates/, using one base template
- Multi-file Flask application
- Server-side validation for required fields
- Use parameterised SQL queries
- No authentication this week
- No JavaScript framework

## Out of scope

- User registration and login
- Multiple business accounts
- Public customer enquiry forms
- Automatic reminders and notifications
- SMS and WhatsApp integrations
- Employee accounts
- Advanced dashboards and reports
- File attachments
- An API
- Online hosting and payment processing

