---
layout: default
title: User Passwords
grand_parent: User Manuals
parent: Contest Administration
---

# User Password Management

The PCS **does not** yet allow users to change their account password when logged into the system. Instead, users should use the *Lost password* link on the log-in page to perform password updates.

## Change Password Utility

In instances when a user cannot reset their password using the aforementioned method, use the form in the *Change User Password* section on the [Contest Dashboard]({{ site.url }}/usage/contest_administration/contest_dashboard.html).

{: .warning-title }
> Django administration
>
> User passwords should **not** be changed in the *Users* section of [Django Administration]({{ site.url }}/usage/contest_administration/django_administration.html), as this field represents a password's *hashed* value, not the raw value.

