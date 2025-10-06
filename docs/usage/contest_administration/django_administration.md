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

Django Administration provides an interface for managing the PCS database. This centralized control panel is essential for tasks that cannot be handled within the Contest Dashboard. The interface may be accessed directly by navigating to `<site_url>/admin/`.

## Administration access

A user profile must be assigned privileges to access Django Administration that are separate from the [Volunteer Roles]({{ site.url }}/usage/volunteers.html#volunteer-roles) assigned through the [Contest Dashboard]({{ site.url }}/usage/contest_administration/contest_dashboard.html). These privileges may be assigned in Django Administration by a user with appropriate access, such as a superuser. 

{: .important-title }
> Docker deployment
>
> When using a [Docker deployment]({{ site.url }}/deployment/docker/docker_image.html) of the PCS, a superuser account is created automatically during system initialization.

## Action Overview

![Django Administration]({{ site.url }}/assets/images/contest_administration/django_administration.png?raw=true)

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