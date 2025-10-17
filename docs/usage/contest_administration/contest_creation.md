---
layout: default
title: Contest Creation
grand_parent: User Manuals
parent: Contest Administration
---

# Contest Creation
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

The *Contest* database table stores details about a contest and should be populated after the PCS is deployed, initialized and secured. Create a contest by adding a new entry to the *Contest* table using the [Django Administration]({{ site.url }}/usage/contest_administration/django_administration.html) interface.

{: .warning-title }
> Multiple contests
>
> The PCS is currently limited to using only the **first** entry in the *Contest* database table. 

## Adding a contest

{: .note-title }
> Initiailization
>
> A contest is easy to intialize requiring only the *Contest date* attribute.

From the [Django Administration]({{ site.url }}/usage/contest_administration/django_administration.html) homepage, click the *Add* button located in the *Contests* row of the *CONTESTADMIN* section.

<figure>
    <img src="{{site.url}}/assets/images/contest_administration/add_contest.png?raw=true" alt="Add contest"/>
    <figcaption><small>Figure 1. Adding a Contest Model.</small></figcaption>
</figure>

Besides the *Contest date* attribute, which is required at creation, a contest's other attributes may be set during initialization or later via the [Django Administration]({{ site.url }}/usage/contest_administration/django_administration.html) interface. Once done editig a contest, click the *Save* button at the bottom of the page.

<figure>
    <img src="{{site.url}}/assets/images/contest_administration/manage_contest.png?raw=true" alt="Edit contest"/>
    <figcaption><small>Figure 2. Editing a Contest Model.</small></figcaption>
</figure>

## Contest Attributes

Each entry in the *Contest* table is comprised of the following attributes.

- **Contest date**   
  *Required.* The date of the programming contest. This value is displayed on the homepage as the *Contest Date*. 
- **Contest doors**  
  *Optional.* The scheduled time that contestants may start checking into the programming contest. This value is presented in the Contest Schedule pop-up window that is available on the homepage. 
- **Contest start**  
  *Optional.* The scheduled time that the DOMjudge server starts accepting submissions and contestants may start working on the contest problem packet. This value is presented in the Contest Schedule pop-up window that is available on the homepage. 
- **Contest freeze**  
  *Optional.* The scheduled time that the DOMjudge scoreboard is frozen. Submissions are still accepted, but the results are not displayed on the public scoreboard. The scoreboard performs a final update once the contest ends. This value is presented in the Contest Schedule pop-up window that is available on the homepage. 
- **Contest end**  
  *Optional.* The scheduled time that the DOMjudge server stops accepting new problem solution submissions and the winners are determined. This value is presented in the Contest Schedule pop-up window that is available on the homepage. 
- **Contest awards**  
  *Optional.* The scheduled time that the post-contest awards ceremony beings. This value is presented in the Contest Schedule pop-up window that is available on the homepage. 
- **Team deadline**  
  *Optional.* The scheduled deadline for a contestant to create a new team. This value is displayed on the homepage as the *Registration Deadline*.
- **Results**  
  *DO NOT EDIT.* A file containing DOMjudge results. This field is used by the contest results upload feature on the [Contest Dashboard]({{ site.url }}/usage/contest_administration/contest_dashboard.html) and **should not** be altered in Django Administration.  
- **Ec processed**  
  *Optional.* Not used in the current implementation.
- **Volunteer pin**  
  *Optional. Default:* `thankyou` The pass code that contest volunteers must provide to complete volunteer check-in.
- **Participation**  
  The contest participation format: `In-Person`, `Virtual` or `Hybrid`.
- **Lfg active**  
  *Optional.* If `True`, the Looking For Group service is active, otherwise the service is inacitve. 
- **Lunch form url**  
  *Optional.* The URL of the lunch preference survey[^1]. After this field is populated, a button with the URL appears in each user's [Account Dashboard]({{ site.url }}/usage/account_management.html#account-dashboard)
- **Order tshirt url**  
  *Optional.* The URL of the page to order a contest t-shirt. After this field is populated, the *Contest T-Shirt* button with the URL appears on the homepage. 

---
[^1]: The survey allows contestants to provide food preference and dietary restriction information to contest organizers.
