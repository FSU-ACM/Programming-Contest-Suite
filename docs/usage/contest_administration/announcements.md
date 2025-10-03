---
layout: default
title: Announcements System
grand_parent: User Manuals
parent: Contest Administration
---


# Announcements System
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

The PCS supports the dissemination of simple text announcements to multiple distribution endpoints. Announcements are managed through the Django Administration interface. 

##  Distribution Endpoints

The PCS offers both embedded and remote distribution endpoints, allowing users to access announcements on a wide variety of devices, platforms, and services.

### Homepage

The most recent[^1] announcements are displayed on the PCS homepage in the *Recent Announcements* column.

### Announcements List

The *Announcements* page, located at `<site_url>/announcements/`, is a public list of all published announcements.

### RSS Feed

The announcemets list is published as an RSS feed, available at `<site_url>/announcements/feed/rss`. Links to the feed are located on the homepage and the *Announcements* page.

### Email

Announcements may be emailed to PCS users assuming the PCS has a working [email configuration]({{ site.url }}/deployment/configuration.html#email). A user may opt-out of receiving announcement emails by [updating their profile]({{ site.url }}/usage/account_management.html#profile).

### Discord

Announcements may be delivered to a [Discord webhook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) assuming the PCS has a working [Discord configuration]({{ site.url }}/deployment/configuration.html#discord).

## Adding an announcement

From the Django Administration homepage, click the *Add* button located in the *Announcements* row of the *ANNOUNCEMENTS* section. 

## Publication status

An announcement's visibility is controlled by its publication status. Announcments may be published and unpublished using the *Status* attribute.

### Draft

When the *Draft* status is selected, an announcement is stored in the PCS database but not delivered to any distribution endpoint.

### Publish

When the *Publish* status is selected, an announcement is stored in the PCS database, visible on the homepage and *Announcements* pages, and available in the RSS feed. If the announcement is configured for  *Email* or *Discord* distribution, it is delivered to those endpoints.

## Announcement Attributes

Each announcement in the database is comprised of the following attributes.

- **Title**  
  *Required, Unique.* The title of the announcement.
- **Slug**  
  *Required, Unique.* The announcement's slug field.
- **Author**  
  *Required.* The PCS user attached as the announcement's author. May be any user in the database.
- **Updated on**  
  *Required.* The date and time the announcement was last updated. Automatically updated by the PCS. 
- **Content**  
  *Required.* The body text of the announcement.
- **Created on**  
  *Required.* The date and time the announcement was created.
- **Status**  
  *Required, Default*: `Draft` The announcement's publication status: `Draft` or `Publish`
- **Send discord**  
  *Required, Default*: `checked` If selected, the announcement is delivered to a Discord webhook. Otherwise, the published announcement is not delivered to a Discord endpoint.
- **Send email**  
  *Required, Default*: `checked`  If selected, the announcement is delivered to PCS users who have not opted-out of receiving announcement emails. Otherwise, the published announcement is not distributed by email.

## Editing announcements

{: .note-title }
> Announcement updates
>
> When an announcement's status is *Publish*, clicking the *Save* button when editing/updating an announcement will *always* trigger delivery to selected *Discord* or *Email* endpoints. Consider avoiding incremental updates to announcements when using the aforementioned endpoints.

### Publishing drafts

If an existing announcement is updated from *Draft* to *Publish*, the *Discord* and *Email* distribution selection at the time the new status is saved will determine the distribution behavior, respectively.

### Unpubishing announcements

If an existing announcement is updated from *Publish* to *Draft*, the anouncement will no longer be visible on the site or available in the RSS feed. If the the announcement was published to the *Discord* or *Email* endpoints, the announcement url contained in those messages will result in an HTTP 404 error until the announcement is republished.

---
[^1]: In the mobile view, only the most recent announcement is displayed. In the desktop view, the six most recent announcements are displayed. 