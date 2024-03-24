# BROAD DISTRIBUTION


| Symbol | Meaning |
| --- | --- |
| ❗ | pending |
| 🟡 | in-progress |
| ✅ | completed |

### Priority 1
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
    * python code for CRUD operations ❗
        + modify existing API code to use DB instead of groups, users, menu_items and transactions dictionaries. ❗
        + implement transaction code (locking) for points award and redemption to avoid parallel write operations and inconsistencies ❗
4. Flask Server - CLI client integration & testing - **Sakshi** 🟡

### Priority 2
1. UI app using streamlit **if time permits**
    * easy to make
    * will make project look complex

2. Cloud Infra setup - **Sakshi**  ❗
    * Register for AWS free-tier ✅
    * EC2 and Auto-scaling groups (ASG -> horizontal scaling) ❗
    * Application load balancer (ALB) ❗
    * RDS - Postgres instances with HA + replication ❗

3. failure scenarios **will decide on Sunday**
    * DB failure
        + switch active-standby
        + delete active DB VM
    * Server failure & load
        + delete EC2 instance for API server
        + simulate high load on EC2 instance
        + turn off HTTP service in EC2 instance so ASG health-check fails and instance is replaced
    * Connection failure
        + ???