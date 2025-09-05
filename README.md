# Triggery
> Jingle bells, jingle bells, trigger it all away!

---

For a live demo, please see https://triggery-backend.onrender.com (credentials have been shared via email)

> [!IMPORTANT]
> [Render](https://render.com) — the cloud service we use for deployment — spins down a free web service that goes 15 minutes without receiving inbound traffic, and spins it back up whenever a request is received. It causes a noticeable delay for the first few requests until the service is back up and running (generally a couople of minutes). For example, a browser page load will hang temporarily.

## Features:

- Multiple options for creating triggers:
  - via API
  - Scheduled
  - Recurring (with versatile `crontab` like input)
- For API triggers, facility to validate 'trigger' requests against schema defined at creation, powered by [jsonschema](https://json-schema.org/).
- Test Triggers easily:
  - When creating a trigger, mark it as a "Test", and it will delete itself after executing _once_.
  - Event logs generated for testing will be clearly labelled.
- Intelligent Event Logging:
  - Real-time event logging to track all executed triggers.
  - Automatic archiving after 2 hours and final deletion after 48 hours, ensuring efficient data retention.
  - Comprehensive event metadata for tracking trigger sources, execution times, and API payloads.

## Setup

We will use `docker-compose` to orchestrate everything.

> [!NOTE]
> Before starting, please ensure ports 5432, 6379 and 8000 are open.
> On a mac, you can use `lsof -i :5432` for a quick check.


```sh
 git clone https://github.com/rajuljha/triggery.git
 cd triggery
  # Ensure docker-daemon is running
 docker start (or run the docker desktop application in the background)
 docker-compose up -d
```

Create a superuser to be able to log in to the UI:

```sh
 docker-compose exec web 'python manage.py createsuperuser'
```

## APIs

Please read through for a quick demo on how to create, test and edit triggers, alongwith viewing the events generated.

### **API Root**

```
GET /
```

<details>

![API Root](public/API_Root.png)

</details>
---


### **Create an API Trigger**
```
POST /api_triggers/
```
![API Trigger Create](public/API_Trigger_POST.png)

---


### **Get an API Trigger**
```
GET /api_triggers/<id>/
```
![API Trigger GET](public/API_Trigger_GET.png)


---


### **Update an API Trigger**

```
PUT, PATCH, DELETE /api_triggers/<id>/
```
<details>

![Update API Trigger](public/API_Trigger_UPDATE.png)

</details>


---


### **Triggering an API Trigger**

```
POST /api_triggers/<id>/trigger/
```

![Triggering API Trigger](public/API_Trigger_TRIGGER.png)

### **Response**
<details>

![Response after Triggering](public/API_Trigger_TRIGGER_RESPONSE.png)

</details>

---


### **Create a Scheduled Onetime Trigger**

> [!NOTE]
> Please enter time in UTC format (timezone awareness is a WIP)


```
POST /one_time_triggers/
```

![Scheduled Onetime Trigger Create](public/One_Time_Trigger_POST.png)

---


### **Get a Scheduled Onetime Trigger**
```
GET /one_time_triggers/<id>/
```
![Scheduled Onetime Trigger GET](public/One_Time_Trigger_GET.png)

---

### **Update a Onetime Scheduled Trigger**

```
PUT, DELETE /one_time_triggers/<id>/
```
<details>

![Scheduled Onetime Trigger Update](public/One_Time_Trigger_UPDATE.png)

</details>

---


### **Create a Recurring Scheduled Trigger**

> [!TIP]
> Use https://crontab.guru for quickly creating crontab expressions

```
POST /recurring_triggers/
```

![Recurring Scheduled Trigger Create](public/Recurring_Trigger_POST.png)

---


### **Get a Recurring Scheduled Trigger**
```
GET /recurring_triggers/<id>/
```
![Recurring Scheduled Trigger GET](public/Recurring_Trigger_GET.png)


---


- **Update a Recurring Scheduled Trigger**
```
PUT, DELETE /recurring_triggers/<id>/
```
<details>

![Update API Trigger](public/Recurring_Trigger_Update.png)

</details>

---


### **Get all Events**
```
GET /events/
```

> [!TIP]
> We can filter the results using the Filter button based on archived state and/or test state.

![Get all events](public/Events.png)


---

## Cost Analysis

The most important factors for running this analysis for this is our choice of deployment strategy, and the cloud. In this case, let us assume that we need to trigger roughly 10,000 recurring tirggers every day, 10,000 scheduled triggers and 15,0000 API triggers. This is roughly 25 tasks every minute. A suitable choice for running this load:


| Resource                             | On-demand hourly price | Approximate Monthly |
|--------------------------------------|------------------------|---------------------|
| Amazon RDS `db.db.t4g.micro`         | $0.016                 | $11.52              |
| Amazon Elasticache `cache.t4g.micro` | $0.0128                | $9.50               |
| Amazon EC2 `t2.micro` (web)          | $0.0116                | $8.50               |
| Amazon EC2 `t2.small` (celery loads) | $0.023                 | $16.50              |

That's roughly $46/month.
