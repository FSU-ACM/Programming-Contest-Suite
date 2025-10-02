---
layout: default
title: DOMjudge Integration
grand_parent: User Manuals
parent: Contest Administration
---

# DOMjudge Integration
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

The PCS works alongside a DOMjudge instance by producing contest bulk data files used to configure accounts, groups and teams in DOMjudge, as well as processing the results data files exported post-contest from DOMjudge.

## Pre-contest

### Exporting contest bulk data files from PCS

After the team registration deadline, obtain the contest bulk data files from the PCS using the *Generate DOMjudge TSVs* feature in the *Pre-Contest* section on the [Contest Dashboard]({{ site.url }}/usage/contest_administration/contest_dashboard.html). These files are used to populate the DOMjudge database.

{: .important-title }
> walk-in teams
>
> All contest walk-in teams must be created before file generation

### Importing data files into DOMjudge

The files are imported through the DOMjudge jury UI using an admin account or by other methods to [add data in bulk](https://www.domjudge.org/docs/manual/main/import.html#adding-contest-data-in-bulk). In the DOMjudge jury UI locate the *Administrator* section and click the *Import / export* link. On the *Import and export* page, use the various import forms to upload the data files.

## Post-contest 

After the conclusion of a contest, obtain the contest results from DOMjudge using the export feature in the DOMjudge jury UI. Results should be exported for each contest running on the DOMjudge server. 

### Exporting results data files from DOMjudge

To export the contest results data files, access DOMjudge with an admin account. Locate the *Administrator* section and click the *Import / export* link. On the *Import and export* page, locate the *Results* section and choose the `TSV` option with `sort order 0`. 

{: .important-title }
> Data file format
>
> The exported results data files must be in TSV format.

### Importing data files into PCS

Upload the exported TSV files to the PCS using the file form in the *Post Contest* section of the [Contest Dashboard]({{ site.url }}/usage/contest_administration/contest_dashboard.html).
