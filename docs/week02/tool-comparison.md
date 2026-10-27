\# Week 02: AI Tool Comparison — Flask Contact Form



&#x20;1. Requirement



Build a contact form for a Flask 3.x application with name, email and message fields. Validate all fields on the server, reject empty fields and malformed email addresses, re-render the form with an error message and HTTP 400 when invalid, and show a confirmation page on success. Use only Flask and the Python standard library.



&#x20;2. Prompts used



&#x20;Claude



Saved verbatim in `experiments/week02/claude/PROMPT.md`:



&#x20;Write a contact form for a Flask 3.x application. Give me templates/contact.html and the route in app.py. Validate name, email and message on the server — not only in the browser. Reject an empty field and a malformed email address, re-rendering the form with an error message and an HTTP 400. On success show a confirmation page. Do not use any package outside Flask and the Python standard library. Output each file separately with its full path.



ChatGPT



Saved verbatim in `experiments/week02/chatgpt/PROMPT.md`:



&#x20;Write a contact form for a Flask 3.x application. Give me templates/contact.html and the route in app.py. Validate name, email and message on the server — not only in the browser. Reject an empty field and a malformed email address, re-rendering the form with an error message and an HTTP 400. On success show a confirmation page. Do not use any package outside Flask and the Python standard library. Output each file separately with its full path.



Note: the prompts were intended to be the same so the implementations could be compared fairly. The saved prompt files are the source of truth for the exact wording.



3\. Evaluation method



Both implementations were run locally. Tests included empty fields, a malformed email (`notanemail`), an empty name after changing its browser-side value, a valid submission, and the JavaScript test string `<script>alert(1)</script>`.



4\. Scores



Scores are from 1 (poor) to 5 (excellent). They are based on observed tests and code review.



&#x20;Criterion    | Claude  | ChatGPT 



&#x20;Correctness  |  5/5    |  5/5 

&#x20;Code quality | 4/5     |  4/5 

&#x20;Completeness | 5/5     |  5/5 

&#x20;Security     | 4/5     |  3/5



5\. Evidence and observations



&#x20;Claude



Claude's implementation ran locally without code changes. It rejected empty fields and malformed emails, returned HTTP 400 for invalid submissions, and displayed a confirmation message after a valid submission. Its server-side validation also enforces maximum lengths for name, email and message.



The code includes a CSRF token check, uses a redirect after a successful POST to avoid accidental resubmission on refresh, and uses Flask/Jinja templates for output. The template preserves entered values and displays field-specific errors.



The JavaScript test did not produce an alert, but the submitted message was not displayed on the confirmation page, so this did not conclusively verify message escaping. Debug mode is enabled for local development and should not be enabled in production. The secret key has a random fallback for development, but production should set `SECRET\_KEY` through the environment.



&#x20;ChatGPT



ChatGPT's implementation ran locally without code changes. It rejected empty fields and malformed email addresses with HTTP 400 responses, accepted a valid submission, and displayed a confirmation page. The server also rejected an empty name after its browser-side value was changed.



Its email validator performs several format checks using Python standard-library functionality. Its templates use Flask/Jinja expressions, which auto-escape values by default. The confirmation page displays the submitted name but not the message, so the JavaScript test did not fully verify message escaping.



The implementation is shorter and easier to follow, but it does not include the CSRF-token check or explicit input length limits present in Claude's version. Debug mode is enabled and should be disabled in production.



&#x20;6. Comparison and decision



Claude is the selected implementation because it meets the functional requirements and includes additional safeguards: CSRF-token validation, explicit input length limits, and a redirect after successful POST submission. These features provide concrete reasons for choosing it over the simpler ChatGPT implementation.



ChatGPT was also functionally successful and has a detailed email-format validator. The choice is therefore based on the additional safeguards in Claude's code, not on a claim that ChatGPT failed the assignment.



&#x20;7. Limitations



Testing was performed manually in a local development environment. The JavaScript test did not conclusively verify message escaping because the submitted message was not rendered on the confirmation page. The scores reflect the evidence collected during this exercise.



&#x20;8. Final implementation



The Claude implementation will be copied into the main application after this comparison. The unselected ChatGPT output will remain in experiments/week02/` for reference.



