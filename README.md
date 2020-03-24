# ticket_api

A Customer Support Ticket System API built with Django REST API framework.

## Dependencies
To run this project you need to have:
* [Docker](https://www.docker.com/)

## Setup the project
1. Install the dependencies above
2. `$ git clone https://github.com/nthtson/ticket_api.git` - Clone the project
3. `$ cd ticket_api` - Go into the project folder
4. `$ sudo chmod a+x start.sh` - Make sure start.sh is executable

If everything goes OK, you can now run the project!

## Running the project

1. `$ docker-compose up --build -d` - Opens the server
2. Open [http://localhost:8080](http://localhost:8080)

## Demo 
The ticket_api includes a basic demo (resides in the demo/ top-level folder.), so that you may easily get started with testing or developing ticket_api. `Demo` is built with as basic frontend UI in javascript and HTML/CSS to showcase both the customer service and user experience using this API. 

NOTE: Here is default customer service account is created after built:
```
Email: support@example.com
Password: Support@123
```

**API Endpoints**

* Sign up:
    * Endpoint: /api/signup/
    * Method: post
    * Header:
        * Content-Type: application/json
    * Request body example:
        ```yaml
        {
            "email": "user@example.com",
            "password": "Abc12345"
        }
    * Response example:
        ```yaml
        {
            "email": "user@example.com",
            "is_customer_service": False
        }
    * Note: User can NOT use this api to create customer service user.
* Authentication:
    * Endpoint: /api/auth/login/
    * Method: post
    * Header:
        * Content-Type: application/json
    * Request body example:
        ```yaml
        {
            "email": "user@example.com",
            "password": "Abc12345"
        }
    * Response example:
        ```yaml
        {
            "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
        }
* Create ticket:
    * Endpoint: api/new_ticket/
    * Method: post
    * Header:
        * Content-Type: application/json
        * Authorization: Token <token>
    * Request body example:
        ```yaml
        {
            "subject": "Trouble redemption",
            "description": "message content"
        }
    * Response example:
        ```yaml
        {
          "success": true,
          "result": {
            "id":2,
            "subject":"Trouble redemption"
          }
        }
* Get ticket list:
    * Endpoint: api/ticket_list/
    * Method: get
    * Header:
        * Authorization: Token <token>
    * Response example:
        ```yaml
        {
          "success":true,
          "result":{
            "count":1,
            "next":null,
            "previous":null,
            "results":[
              {
                "subject":"Trouble redemption",
                "description":"Help me please!",
                "replies_count":1,
                "owner":"admin@gmail.com",
                "ticket_id":"46fe5123ce92",
                "status":"open",
                "human_time":"4 minutes ago",
                "id":2
              }
            ]
          }
        }
    * Pagination is applied.
    
* Get a ticket details:
    * Endpoint: api/tickets/<ticket_pk>/
    * Method: get
    * Header:
        * Authorization: Token <token>
    * Response example:
        ```yaml
        {
          "success":true,
          "result":{
            "subject":"Trouble redemption",
            "description":"Help me please!",
            "replies_count":1,
            "owner":"admin@gmail.com",
            "ticket_id":"46fe5123ce92",
            "status":"open",
            "human_time":"4 minutes ago",
            "id":2
          }
        }
    
* Reply to a ticktet:
    * Endpoint: api/tickets/<reply_id>/reply/
    * Method: post
    * Header:
        * Content-Type: application/json
        * Authorization: Token <token>
    * Request body example:
        ```yaml
        {
            "message": "Let me check"
        }
    * Response example:
        ```yaml
        {
          "success":true,
          "result":{
            "id":4,
            "status":"Success"
          }
        }
* Delete a reply:
    * Endpoint: api/replies/<reply_id>/
    * Method: delete
    * Header:
        * Content-Type: application/json
        * Authorization: Token <token>
        
**Unit Testing**

`$ python manage.py test`