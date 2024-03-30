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

2. Cloud Infra setup - **Sakshi**  ❗
    * Register for AWS free-tier ✅
    * EC2 and Auto-scaling groups (ASG -> horizontal scaling) ✅
    * Application load balancer (ALB) ✅
    * RDS - Postgres instances with HA + replication ✅
==================================================================================================================================
## PART II

3. ### failure scenarios 
    
* DB failure scenarios - **Sakshi**

    DB failure 
        + switch active-standby
        + stop active DB instance
    Server failure & load 
        + stop EC2 instance for API server
        + simulate high load on EC2 instance
        + turn off HTTP service in EC2 instance so ASG health-check fails and instance is replaced
    Connection failure
        + cli and server
    Consistency issues
        + how/where is it implemented
        + DB access
        + order of requests
        + double spending
    Region change
        + Access through gateway 


* Tokens - **David**
        + no double spending
        + check from which group tokens are spent

* Loads of requests from multiple clients **Brian**
        + demonstrate multiple clis and requests (maybe in a loop)
        + script to create 20 users and 5 groups - to keep transactions ongoing.
        + keep testing consistency as part of script

* Discounts **will see afterwards**
        + customers not being able to avail an entitled discount

-------------------------------------------

### Changes in API and CLI - (April/Brian/David)

1. CLI: Group id field in user's table should be replaced by Groups which will be a list of groups user is part of.

        
                    USERS
                    username,password,full_name,group_id
                    username,password,full_name,groups

                    sakshi,abcd,sakshi dhingra,[324322,324324,322423]


                    GROUPS
                    group_name,location,users,points
                    DHingras,Dublin,[313431,232124,4534534],0

2. API: New endpoint to add a user to group

3. CLI:, user can join a group after login by using group_id

4. CLI: add another ques in cli - what is your home region?  - assign user id based on this - '001-<>' for R1 '002-<>' for R2, '003-<>' for R3. 

5. Transaction update lock for group points (eg, below)

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