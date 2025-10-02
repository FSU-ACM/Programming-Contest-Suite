---
layout: default
title: Contest Dashboard
grand_parent: User Manuals
parent: Contest Administration
---

# Contest Dashboard
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

The Contest Dashboard centralizes many of the administrator actions available in the PCS. The interface may be accessed directly by navigating to `<site_url>/contestadmin/`.

{: .important-title }
> Dashboard access
>
> A user profile must be assigned the *Contest Organizer* role to access the the Contest Dashboard and Contest Statistics page.

![Contest Dashboard]({{ site.url }}/assets/images/contest_administration/contest_dashboard.png?raw=true)

## Dashboard Summary

- **Pre-Contest**
    - Generate and download the DOMjudge TSV files required to populate the DOMserver database with contestant data
- **Post Contest**
    - Upload the results TSV file(s) from DOMjudge 
        - In DOMjudge: *Administer > Import / Export > results.tsv w/ sort order 0*
- **Extra Credit**
    - Generate and download the CSV files with contestant participation data
    - Notify all faculty registered with the contest that participation results are available
- **Contest Tools**
    - Create a specified number of Upper/Lower Division walk-in teams
    - Check in/out all users (useful for virtual contests)
- **Update User Role**
    - Update an account's role (Contestant, Docent, Proctor, Question Writer, Organizer)
- **Account Tools**
    - Manually activate a user account. Useful if a registrant has issues verifying their account.
    - Mark a given team as a Faculty Team
- **Volunteers**
    - Displays all volunteers registered in the system, whether they have registered for extra credit, and if they've checked into the contest

## Contest Statistics

The Contest Statistics page quantifies numerous PCS database features. The interface may be accessed directly by navigating to `<site_url>/contestadmin/statistics/`.
