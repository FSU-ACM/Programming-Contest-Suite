---
layout: default
title: Contest Administration
parent: User Manuals
has_children: true
nav_order: 1
---

# Welcome to the Contest Administration Manual!

The Programming Contest Suite (PCS) is designed to ease the administration of a programming contest hosted with the [DOMjudge](https://www.domjudge.org/) jury system by facilitating contest registration and management, generating contest data files required by DOMjudge, and processing contest results exported from DOMjudge. The articles comprising this manual document how to host a programming contest with the PCS. 

{: .important-title }
> Management Interfaces
>
> A contest is managed through Django Administration and the [Contest Dashboard]({{ site.url }}/usage/contest_administration/contest_dashboard.html). 

## Administration Flowchart

The following diagram outlines the actions performed by contest administrators throughout the process of hosting a contest.

```mermaid
---
config:
  flowchart:
    htmlLabels: false
---
flowchart
    direction TB

    %% Node style classes (keep your task colors)
    classDef D fill:#67e1b3,stroke:#092e20,stroke-width:2px,color:#000
    classDef C fill:#9bdcf1,stroke:#1b9cc6,stroke-width:2px,color:#000
    classDef L fill:#fff,stroke:#999,stroke-dasharray: 5 5,color:#000

    %% Main containers (IDs used so we can style them below)
    subgraph PreContest [**Pre-contest**]
        direction TB

        PC1["Create contest in DB"]

        subgraph ExtraCredit [**Extra Credit System**]
            direction TB
            EC1["Add faculty to DB"]
            EC2["Add courses to DB"]
            EC1 --> EC2
        end

        PC2["Assign volunteer roles"]
        PC3["Add sponsors to DB"]

        subgraph DOMjudgeFiles [**DOMjudge Files**]
            direction TB
            DJ1["Create walk-in teams"]
            DJ2["Generate and download contest data files"]
            DJ1 --> DJ2
        end

        %% connect to nodes inside sub-subgraphs (safer)
        PC1 --> ExtraCredit 
        PC1 -->|"*Before Contest Day*"| PC2
        PC1 -->|"*Before Contest Day*"| PC3
        PC1 -->|"*After Registration Deadline*"| DOMjudgeFiles
    end

    subgraph ContestDay [**Day of Contest**]
        direction LR
        CD1["Contestant check-in"]
        CD2["Volunteer check-in"]
    end

    subgraph PostContest [**Post-contest**]
        direction LR
        PO1["Upload contest results"]
        PO2["Generate extra credit reports"]
        PO3["Email faculty"]
        PO4["Download all faculty reports"]
        PO5["Generate merged registration and DOMjudge results"]
        PO6["Download all division reports"]

        PO1 -->|"*Announce course selection deadline*"| PO2 
        PO2 --> PO3
        PO2 -->|"*Optional*"| PO4
        PO1 --> PO5
        PO5 -->|"*CSV file per division*"| PO6
    end

    %% high-level connection
    PreContest -->|"*Upload contest data files to DOMjudge*"| ContestDay --->|"*Download results files from DOMjudge*"|PostContest

    %% Legend (keeps your original labels)
    subgraph Legend [Legend]
        direction TB
        L1["Django Administration"]
        L2["Contest Dashboard"]
        L1 ~~~ L2
    end

    %% Assign classes to tasks
    class PC1,PC3,EC1,EC2,L1 D
    class PC2,DJ1,DJ2,PO1,PO2,PO3,PO4,PO5,PO6,L2 C
    class Legend L

    %% Style the subgraph containers (light neutral palettes)
    %% Pre-contest: warm neutral / parchment
    style PreContest fill:#F8F8F8,stroke:#A9A9A9,stroke-width:1px

    %% Sub-subgraphs inside Pre-contest: lighter tints that tie to the Pre-contest color
    style ExtraCredit fill:#DCDCDC,stroke:#808080,stroke-width:1px
    style DOMjudgeFiles fill:#DCDCDC,stroke:#808080,stroke-width:1px

    %% Post-contest: cool neutral / very light gray-blue
    style PostContest fill:#F8F8F8,stroke:#A9A9A9,stroke-width:1px

    %% Give the Legend a subtle white box with dashed border
    style Legend fill:#FFFFFF,stroke:#CCCCCC,stroke-dasharray:5 5,stroke-width:1px
```
