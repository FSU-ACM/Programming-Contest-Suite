---
layout: default
title: Django Administration
grand_parent: User Manuals
parent: Contest Administration
---

# Django Administration
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

The Django Administration provides an interface for managing objects such as Sponsors and Contests. This centralized control panel is essential for tasks that cannot be handled within a Contest Dashboard. The interface may be accessed directly by navigating to `<site_url>/admin/`.

{: .important-title }
> Administration access
>
> A user profile must be assigned the *Contest Organizer* role to access the Django Administration.

![Django Administration]({{ site.url }}/assets/images/contest_administration/django_administration.png?raw=true)

## Action Overview

- **Create Contests**
    - Create a contest for the semester.
- **Add Sponsors**
    - Set a sponsor's name, logo, and optional details like a URL, message, and ranking.
- **Create Announcements**
    - Create an announcement by setting a title, content and send via Discord and/or email.
- **Add Courses**
    - Import/Export/Add courses for extra credits.
- **Add Faculty**
    - Import/Export/Add faculty for the courses eligible for extra credits.