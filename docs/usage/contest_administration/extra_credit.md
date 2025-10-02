---
layout: default
title: Extra Credit System
grand_parent: User Manuals
parent: Contest Administration
---

# Extra Credit System
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

The extra credit system allows users to attach one or more registered courses to their account. After a contest, and once the DOMjudge results have been uploaded using the [Contest Dashboard]({{ site.url }}/usage/contest_administration/contest_dashboard.html), the PCS can generate participation reports per registered course. These reports are then distributed to course instructors.

## Pre-contest

The PCS database must be populated with course and faculty data before users can attach courses to their profile. *Course* and *Faculty* database entries are managed through the Django Administration interface. 

{: .important-title }
> Initialization order
>
> Each course in the database is tied to a faculty member database entry; therefore the *Faculty* table should be populated before the *Course* table. 

### Adding Faculty

The *Faculty* database table stores the course instructors who register one or more courses with a semester's contest. From the Django Administration homepage, click the *Add* button located in the *Facultys* row of the *MANAGER* section. 

{: .warning-title }
> Email addresses
>
> Any valid email address is allowed, although the user portion (ex. `user@example.com`) of the address should be unique across all faculty entries in the database. This constraint **is not** monitored by the PCS. In the event two or more entries have a matching user portion (ex. `user@example1.com` and `user@example2.com`), the PCS will incorrectly map courses to instructors during extra credit file processing.

### Faculty Attributes

Each Faculty entry contains the following fields.

- **Email**  
  *Required, Unique.* The email address of the instructor.
- **First name**  
  *Required.* The instructor's first name.
- **Last name**  
  *Required.* The instructor's last name.


### Adding Courses

The *Course* database table stores the courses that instructors register with a semester's contest. From the Django Administration homepage, click the *Add* button located in the *Courses* row of the *MANAGER* section. 

### Course Attributes

- **Code**  
  *Required.* The FSU course code (ex. `COP3014`)
- **Name**  
  *Required.* The course name (ex. `Programming I`)
- **Instructor**  
  *Required.* The course's istructor. 


### Adding data in bulk

*Course* and *Faculty* data may be added in bulk through the Django Administration interface. 

{: .important-title }
> Import order
>
> The faculty data file must be imported before the course data file. 

#### Faculty file

From the Django Administration homepage, navigate to the *Faculty* table by clicking the *Facultys* button in the *MANAGER* section. On the *Faculty* table page, click the *IMPORT* button in the upper right hand corner of the interface. 

The PCS supports faculty bulk uploads in the following CSV format:  

```
email,first_name,last_name
lovelace@cs.example.edu,Ada,Lovelace
turing@test.ai,Alan,Turing
boole@logic.io,George,Boole
```

A simple Python script to generate a faculty data CSV is located in the [PCS code repository](https://github.com/FSU-ACM/Programming-Contest-Suite/blob/main/utils/faculty_csv_gen.py). 

{: .highlight-title }
> Faculty data file generator
>
> The data file generation script only creates entries for `@cs.fsu.edu` email addresses.


#### Course file

From the Django Administration homepage, navigate to the *Course* table by clicking the *Courses* button in the *MANAGER* section. On the *Course* table page, click the *IMPORT* button in the upper right hand corner of the interface. The faculty member references in the course data file must already exist in the database.

The PCS supports course bulk uploads in the following CSV format: 

```
id,code,name,instructor
1,COP3330,Object Oriented Programming,lovelace@cs.example.edu
2,COP3014,Programming I,turing@test.ai
3,CDA3100,Computer Organization I,boole@logic.io
```
A simple Python script to generate a course data CSV is located in the [PCS code repository](https://github.com/FSU-ACM/Programming-Contest-Suite/blob/main/utils/course_csv_gen.py).


## Post-contest

After a contest has concluded, the PCS processes contest results from DOMjudge. This data, combined with user registration and check-in data, are used to generate attendance and participation records for each course registered in the PCS database. These records are then distributed to the registered course instructor.

### Generating reports for faculty

After DOMjudge results are uploaded to the PCS through the [Contest Dashboard]({{ site.url }}/usage/contest_administration/contest_dashboard.html), the PCS will enable the *Generate Reports* button in the *Extra Credit* section of the Contest Dashboard. 

Run the *Generate Reports* task only after uploading **all** DOMjudge results files. The task needs to be run only once, unless there are subsequent updates to the database that should also be updated in the reports. 

Each generated report represents a course in the PCS database. For each course, the PCS users who attached that course to their profile are parsed. If a user's profile is marked as checked-in to the contest, then the user's registration information and contest performance are written to the course data file.

{: .note-title }
> Excluded courses
>
> The task creates a course file only if there is at least one PCS user who both added the course to their profile and is also marked as checked-in to the contest. 

### Report format

Each row of a course data file has the following CSV format:

```
fsu_id,last_name,first_name,questions_answered,team_division,role
```

Each generated report uses the following file name format:

```bash
email-user_course-code.csv
```

Above, *email-user* represents the user portion of a course instructor's email address (ex. `user@example.com`) and *course-code* represents the course's FSU course code (ex. `COP3014`).

### Distributing reports to faculty

After the *Generate Reports* task completes, the PCS enables the *Email faculty* button located in the *Extra Credit* section of the [Contest Dashboard]({{ site.url }}/usage/contest_administration/contest_dashboard.html).  Running this task delivers an email[^1] to each faculty member in the database; notifying them that contest participation is processed, and whether files are available for any of their registered courses.


{: .note-title }
> Faculty dahboard
>
> The notification email includes a unique link to a personalized [Faculty Dashbord]({{ site.url }}/usage/faculty.html#faculty-dashboard) where the faculty member can browse their registered courses and download their data files, if avilable.

### Downloading all reports

After the *Generate Reports* task completes, the PCS enables the *Download reports* button located in the *Extra Credit* section of the [Contest Dashboard]({{ site.url }}/usage/contest_administration/contest_dashboard.html), that serves the user a ZIP file containing all generated couse data files.

---
[^1]: To the email address registered in the faculty member's database entry.
