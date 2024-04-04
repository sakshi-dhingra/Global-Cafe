# BROAD DISTRIBUTION


| Symbol | Meaning |
| --- | --- |
| ❗ | pending |
| 🟡 | in-progress |
| ✅ | completed |

## PART I
1. DB stuff - **April ,Tanay**
    * postgres local setup on laptop ✅
    * add db entry and all tables ✅
2. CLI app for both staff and users - **Brian**
    * CLI application interface (menu driven)                   
    * HTTP client implementation ✅
    * Login & authentication ✅
        + using user_id - 6 character string for now ✅
    * code partitioning❗
        + staff UI (billing)❗
        + user UI (view catalogue, points)❗
    * group ✅
        + spend points?  ✅
        + view group points ✅
3. API server - **David**
    * expose functionality (API) ✅
        + billing ✅
        + get data ✅
        + points redemption ✅
    * python code for CRUD operations ✅
        + modify existing API code to use DB instead of groups, users, menu_items and transactions dictionaries. ✅
        + implement transaction code (locking) for points award and redemption to avoid parallel write operations and inconsistencies ❗
4. Flask Server - CLI client integration & testing - **Sakshi** 🟡

### Priority 2
1. UI app using streamlit **if time permits**
    * easy to make
    * will make project look complex

2. Cloud Infra setup - **Sakshi** 
    * Register for AWS free-tier ✅
    * EC2 and Auto-scaling groups (ASG -> horizontal scaling) ✅
    * Application load balancer (ALB) ✅
    * RDS - Postgres instances with HA + replication ✅

---

## PART II

3. failure scenarios 
    
* DB failure scenarios - **Sakshi**

    - DB failure 
        + switch active-standby
        + stop active DB instance
    - Server failure & load 
        + stop EC2 instance for API server
        + turn off HTTP service in EC2 instance so ASG health-check fails and instance is replaced
    - Connection failure
        + cli and server
    - Consistency issues
        + how/where is it implemented
        + DB access, order of requests
    - Region change
        + Access through gateway 


* Tokens - **David** 
    + no double spending
    + check from which group tokens are spent

    + Transaction update lock for group points (eg, below)

```
BEGIN TRANSACTION;
 
-- Set appropriate isolation level
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
 
-- Select the record with appropriate locks
SELECT * FROM YourTable WITH (UPDLOCK, HOLDLOCK) WHERE YourCondition;
 
-- Perform your operations on the record
-- UPDATE YourTable SET ... WHERE YourCondition;
 
-- Commit the transaction
COMMIT TRANSACTION;
```

* Loads of requests from multiple clients **Brian**
    + demonstrate multiple clis and requests (maybe in a loop)
    + script to create 20 users and 5 groups - to keep transactions ongoing.
    + keep testing consistency as part of script

* Discounts **will see afterwards**
    + customers not being able to avail an entitled discount

-------------------------------------------

### Changes in API and CLI 

 **April**
1. CLI: Group id field in user's table should be replaced by Groups which will be a list of groups user is part of.

```
    USERS
    username,password,full_name,group_id
    username,password,full_name,groups

    sakshi,abcd,sakshi dhingra,[324322,324324,322423]


    GROUPS
    group_name,location,users,points
    DHingras,Dublin,[313431,232124,4534534],0
```

2. API: New endpoint to add a user to group

3. CLI:, user can join a group after login by using group_id

4. CLI: add another ques in cli - what is your home region?  - assign user id based on this - '001-<>' for R1 '002-<>' for R2, '003-<>' for R3. 

  
-----------------

* Basic caching: cache catalogue table using a dictionary in API server.
    {
        "request-details": {
            "data": response,  #unpack
            "timestamp": value
        }
    }

    if current - cache_timestamp > expiry, request from database again

* Changes in diagram


---
KEY FEATURES

Code
* Transaction locks to avoid duplicate writes

========================================

## Routing Logic

R1                       R2                        R3
[DB]                    [DB]                      [DB]
001                     002                        003

Note: user_id consists of <rid>,<_uid>  #region id, _user id
        group_id consists of <rid>, <_gid> 

USERS
    username,password,full_name,groups
    sakshi@abcd.com,abcd,Sakshi Dhingra,[001-abcdef,002-astgv1,001-sdfsd2]

GROUPS
    group_name,location,users,points
    Dhingras,Dublin,[001-abcdef,002-astgv1,001-sdfsd2],0

WHEN USER MAKES A TRANSACTION OR FETCHES GROUP DETAILS
1. Get user id and lookup all the groups linked to that user in user table under groups column.
2. For each group linked to the user:
    check each group-id and extract rid. 
    check if rid is same as current location
        if yes, find the group id details (such as group name and points) from that location's group table 
        else, check rid and route the query to that specific region's database's group table and give users and points in group

        Note: the logic to get users part of a group will be similar. For group_id get members by refering to users column and then do routing lookup

    Then _Group id: Group members, points_ for all linked group ids will be displayed to user

3. User will choose a group from which he/she wants to redeem points. 

===============================================





