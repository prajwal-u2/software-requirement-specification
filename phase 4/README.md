# Overview

Welcome to the **P4 Project** for the **SPORTS system**. This project provides a mini web server to give you hands-on experience with the end-to-end process of auto-scheduling teams across various venues. The server is powered by **FastAPI**, a Python-based web framework. You can find its documentation here:  
[FastAPI Documentation](https://fastapi.tiangolo.com/)

The SPORTS system web portal includes three primary pages:
- **Landing Page**: Can be ignored for this assignment.
- **Login Page**: Authentication portal to be used once for sign on

Credentials:
```
email: user@example.com
password: password
```
- **Scheduler Page**: Contains buttons to test and run your scheduling code. Refer to the "Test Cases" section for details about each dataset.

---

# Web Server

You are free to implement the auto-scheduler in a language of your choice. 
However, the initial setup requires Python libraries to run the FastAPI server. 
Using the server is optional, yet highly recommended for testing your scheduler.

### Setup Instructions

Run the following bash scripts to set up and launch the server:

```bash
./bin/build-env
source ./bin/run-env
./bin/launch
```

After running the launch script, open a browser and navigate to:  
https://localhost:8000/

### Language Support

Supported languages include **py**, **java**, and **cpp**.

When launching the system specify the language of your scheduler in the launch command, if none is provided, it will default to python. If you are running python ignore, the language argument as demonstrated in the setup.

```
./bin/launch <language>
```

---

# Scheduler

For students who decide to use a different language in implementing the 
autoscheduler, it is important to follow a few guidelines. These guidelines 
are present so that the FastAPI instance may still call the scheduler.
If you navigate to the data directory you should see nine subdirectories.

### Input Files

Each test case directory contains three input files:
- **`team.csv`**: Team information.
- **`league.csv`**: League details.
- **`venue.csv`**: Venue availability and properties.

### Output File

Your program should generate a **`schedule.csv`** file in the same directory as the input files.

### CLI Format

The scheduler must run from the command line with the following format:

```
./bin/<language>/schedule <case>
```

Supported languages include Python (`py`), Java (`java`), and C++ (`cpp`). For example, to
run case 6 using Python:

```
./bin/py/schedule case6
```

# Helper Code

To assist with this assignment, two modules have been provided:

- **`IntervalTree`**: A utility for detecting overlaps and managing schedules. While you are free to design your own solution, it is strongly recommended to use this approach.
- **`Game`**: Encapsulates the attributes required for the final schedule, ensuring your output aligns with the front-end rendering.

---

# Serialization Format

Your final output file (`schedule.csv`) must contain the following headers:

- **`team1Name`**: Name of Team 1.
- **`team2Name`**: Name of Team 2.
- **`week`**: Week number of the year (1–52).
- **`day`**: Day of the week (1–7, where Monday = 1).
- **`start`**: Match start time (0–23.5, in 30-minute increments).
- **`end`**: Match end time (0–23.5, in 30-minute increments).
- **`season`**: Year of the season (assume 2024 for all matches).
- **`league`**: Name of the league.
- **`location`**: Venue description in the format `"<venue_name> Field #<field_number>"`.
---

# Test Cases

Testing is best conducted through the web server. However, tests can also be run via the CLI:

```
./bin/test <case>
```

Later test cases are evaluated on thresholds rather than completeness due to limited availability. Passing all test cases does not guarantee an "A". Ensure your work is well-documented and reach out on **Piazza** for questions. You may assume that each game is 2 hours long, however this should not be hardcoded.

### Case Details

1. **Case 1**: 8 Teams, 1 League, 1 venue, 4 fields, uniform availability.  
2. **Case 2**: 8 Teams, 3 Leagues, 1 venue, 4 fields, uniform availability.  
3. **Case 3**: 16 Teams, 1 League, 1 venue, 1 field, uniform availability.  
4. **Case 4**: 24 Teams, 1 League, 1 venue, 1 field, limited availability.  
5. **Case 5**: Synthetic data with 52 teams, 3 leagues, limited venues, and limited availability.  
6. **Case 6**: Synthetic data with 104 teams, 3 leagues, limited venues, and limited availability.  
7. **Case 7**: Synthetic data with 104 teams, 3 leagues, varied games, limited venues, and availability.  
8. **Case 8**: Synthetic data with 104 teams, 3 leagues, 1 venue, full availability.  
9. **Generated**: Large randomly generated set of data, for the brave and bold. More varied attributes with some erroneous data points.

---

# Submission

For submission, please make sure to submit a zip file of your codebase to Canvas. Include a brief write-up describing any extra code your team implemented and/or build instructions if anything was changed. Additionally, provide a summary of how your algorithm works and why you chose the given design.
