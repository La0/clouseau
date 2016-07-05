# Clouseau Backend

This is the documentation for the REST Api, exposing some clouseau bug analysis.

## Setup

Install the prerequisites via `pip`:
```sh
sudo pip install -r backend-requirements.txt
```

Create the database, and an initial analysis:
```sh
FLASK_APP='backend/__init__.py' flask initdb
```

## Build analysis data

At first no bugs are in your database, you need to run the workflow through this command:
```sh
FLASK_APP='backend/__init__.py' flask run_workflow
```

Every registered analysis will:
 * fetch bug list from Bugzilla
 * for each bug, build the bug analysis and store it

## API

### /analysis/<analysis_id>/

Fetches all the details of an analysis, with the associated bugs and their payloads:

```
GET /analysis/1/

{
  "id" : 1,
  "name" : "demo",
  "bugs": [
    {
      "bugzilla_id": 12345, 
      "id": 42, 
      "payload": {
        "analysis": {
          "backout_num": 0, 
          "blocks": 0, 
          "changes_size": 78, 
          "code_churn_last_3_releases": 20, 
          "code_churn_overall": 175, 
          "comments": 8, 
          "crashes": 467, 
          "depends_on": 0, 
          "developer_familiarity_last_3_releases": 3, 
          "developer_familiarity_overall": 61, 
          "modules_num": 1, 
          "r-ed_patches": 0, 
          "reviewer_familiarity_last_3_releases": 8, 
          "reviewer_familiarity_overall": 49, 
          "test_changes_size": 0
        }, 
        "bug": {
          "assigned_to": "xxxx@mozilla.com", 
          "assigned_to_detail": {
            ...
          }, 
        ...
```

