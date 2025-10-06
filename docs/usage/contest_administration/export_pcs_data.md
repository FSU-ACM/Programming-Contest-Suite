---
layout: default
title: Export PCS Data
grand_parent: User Manuals
parent: Contest Administration
---

# Export PCS Data

The PCS can generate CSV files with merged user, team and contest results data, useful for archiving results post-contest. Generate the data files using the *Generate Team CSVs* utility in the *Tools* section on the [Contest Dashboard]({{ site.url }}/usage/contest_administration/contest_dashboard.html). A download button is enabled in the same section after file generation completes.

For each division, a file is generated where each row has the following CSV format:

```
team_division,team_name,questions_answered,domjudge_id,team_active,team_members
```

- **team_division**  
    The division code of the team: faculty (`F`), upper (`U`) or lower (`L`).
- **team_name**  
    The team's name registered in the PCS.
- **questions_answered**  
    The number of correct submissions by the team in DOMjudge.
- **domjudge_id**  
    The team's ID (ex. `acm-xxx`) in DOMjudge. 
- **team_active**  
    If `T` then at least one team member checked into the contest, otherwise `F`.
- **team_members**  
    The full name of each team member.