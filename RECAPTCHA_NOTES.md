RECAPTCHA re-enable instructions

Edited files
- login.html

Summary
- All reCAPTCHA usage in the project has been disabled (commented out) so you can develop without a configured domain/site key. The only occurrence found and changed was login.html.

Quick steps to re-enable
1. Register your site in Google reCAPTCHA admin and get a Site Key and Secret (choose reCAPTCHA v2 "I'm not a robot" if you want the current markup).
2. In login.html replace the placeholder site key: locate the commented block containing `data-sitekey="YOUR_RECAPTCHA_SITE_KEY"` and set it to your Site Key.
3. Uncomment the HTML block for the widget:
   - Remove the surrounding HTML comment markers so the `div class="recaptcha-container"` and its child `div class="g-recaptcha"` are active again.
4. Re-enable the client-side checks:
   - Find the JS block commented like: `// Check reCAPTCHA response (disabled while no domain/site key available)` and remove the `/* ... */` around the `grecaptcha.getResponse()` check.
5. Re-enable reset on error:
   - Find the commented `grecaptcha.reset()` block (the `try { grecaptcha.reset(); } catch (e) { ... }`) and remove the comment markers.
6. Re-enable the external script include at the bottom of the file:
   - Uncomment the `<script src="https://www.google.com/recaptcha/api.js" async defer></script>` line.

Server-side verification (recommended)
- After you receive `g-recaptcha-response` on the client, verify it with your Secret on the server:

Example (curl):

curl -X POST "https://www.google.com/recaptcha/api/siteverify" \
  -d secret=YOUR_SECRET_KEY \
  -d response=TOKEN_FROM_CLIENT

- The response will be JSON. Check the `success` boolean before trusting the login attempt.

Notes and tips
- If you plan to use reCAPTCHA v3, you'll need to change the client-side integration and scoring logic accordingly.
- If you later add reCAPTCHA to other pages, follow the same approach: place the `g-recaptcha` widget HTML, include the `api.js` script, and check the token with `grecaptcha.getResponse()` on submit.
- To find any remaining occurrences, grep for `g-recaptcha`, `grecaptcha`, or `data-sitekey`.

Files changed: login.html (reCAPTCHA sections commented out).