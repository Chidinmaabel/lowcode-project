# Week 3 – Independent Code Review

## Finding 1 – Follow-up date is not validated on the server

**File:** `enquiry_tracker/app.py`  
**Related file:** `enquiry_tracker/schema.sql`  
**Priority:** Medium  
**Review decision:** Accepted

**What the reviewer identified:**

The application collects the follow-up date as text but does not check whether the submitted value is a genuine calendar date before saving it.

The HTML form uses an input of type `date`. However, browser-side validation can be bypassed, so the server should also validate the date.

**Why I accept this finding:**

The follow-up date is intended to help the business owner organise future customer follow-ups. Saving an invalid date could cause problems when the application uses these dates later.

**My understanding:**

The date picker helps the user select a date, but it does not replace server-side validation. The Flask application should check the date before saving it to the database.

**Planned action:**

Investigate and update the `clean_form()` function in `app.py` to reject invalid follow-up dates while still allowing the field to be left empty.

**Testing planned:**

- Confirm that a valid date is accepted.
- Confirm that an empty optional date is accepted.
- Confirm that an invalid date is rejected.

**Status:** Accepted – fixed and tested.
**Reason for decision:**

I accepted this finding because the specification describes follow_up_date as an optional date. The application should accept a valid date or an empty value, but it should reject invalid date text. Browser-side date selection alone is not sufficient because server-side validation is also needed.

**Implementation and testing result:**

The follow-up date validation was added to `clean_form()` in `app.py`. I tested three scenarios:

- Invalid date (`2026-02-30`): rejected with HTTP 400 and an error message.
- Valid date (`2026-11-20`): accepted with HTTP 200.
- Blank date: accepted and saved successfully.

**Conclusion:** The issue has been fixed and all three tests passed.

### Finding 2 – Forms have no CSRF protection

**Priority:** Medium

**Files:** `app.py`, `templates/enquiry_form.html`, `templates/enquiry_detail.html`

**What I found:**

The application has two forms that submit POST requests, but neither includes CSRF protection.

**Reason for decision:**

I accept this finding because CSRF protection helps prevent unwanted requests being submitted to the application through another website. Although this is a course project, it is important to consider security before making the application available to real users.

**Status:** Accepted – not yet fixed.

### Finding 3 – Customer email addresses are not checked for valid format

**Priority:** Low – potential improvement

**File:** `app.py`

**Reason for decision:**

I reject this finding as a failure to meet the current specification because my specification requires the email field to be completed but does not explicitly require email-format validation. The application correctly rejects an empty email address.

However, I recognise that checking email format would be a useful improvement for a future version.

**Status:** Rejected as a current defect – consider for future improvement.

### Finding 4 – Some database constraints rely on application validation

**Priority:** Low – improvement

**File:** `schema.sql`

**Reason for decision:**

I reject this as a current application defect because the application already checks that customer name, phone and email are not empty before saving an enquiry. However, I understand that additional database constraints could provide another layer of protection if records were inserted through a different route.

**Status:** Rejected as a current defect – possible future improvement.
## Positive findings – What is working well

The independent reviewer identified the following good practices in my application:

1. **Flask routes:** All five routes in my specification are present.
2. **Required fields:** Customer name, phone and email are checked.
3. **SQL queries:** Parameterised queries are used, helping protect against SQL injection.
4. **Status validation:** The application only accepts the permitted enquiry statuses.
5. **Database connection:** The database connection is properly closed after use.
6. **HTML templates:** A shared `base.html` template is used.
7. **XSS protection:** Jinja's automatic HTML escaping is retained.
8. **Database structure:** Primary keys, defaults and status constraints are defined.

## Acceptable design decisions

The reviewer confirmed that the following are acceptable because they are outside the current project specification:

- No login or registration.
- No SMS or WhatsApp notifications.
- No automatic follow-up reminders.
- No advanced dashboard or reporting.
- No JavaScript framework.
- SQLite instead of PostgreSQL.
- No ORM.

These features are not being treated as defects because they are outside the agreed scope of this project.

## Review conclusion

The application substantially meets my specification. I accepted two findings for further investigation and correction: server-side follow-up date validation and CSRF protection. I rejected two findings as current specification failures, while recognising them as possible future improvements.

The original application has not yet been modified. The accepted findings will be addressed through separate changes, tests and Git commits.