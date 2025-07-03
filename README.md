# Websocket-Chat


Run locally with docker:
docker compose up --build -d


Run test:
docker-compose exec app env PYTHONPATH=/WORKDIR pytest


Architecture:

                         +----------------------+
                         |        Client        |
                         |    (Web Browser)     |
                         +----------+-----------+
                                    |
                                    |  WebSocket / HTTP
                                    v
                         +----------+------------+
                         |        Chat App       |
                         |  (WebSocket Endpoint, |
                         |  RESTful APIs)        |
                         +----------+------------+
                                    |
                                    |
                                    |                            
                                    v                            
                              +-------------+              
                              | PostgreSQL  | 
                              |  Users      |                 
                              |  Groups     |                
                              |  Messages   |                                        


Sequence Diagram:
    participant Client
    participant REST_API
    participant WS_Server
    participant DB

    Client->>REST_API: POST /users (User Creation)
    REST_API-->>Client: 201 Created

    Client->>REST_API: POST /groups (Group Creation)
    REST_API-->>Client: 201 Created

    Client->>WS_Server: WebSocket Connection
    REST_API-->>WS_Server: OK

    WS_Server-->>DB: Add user to room

    Client->>WS_Server: Send message via WebSocket
    WS_Server-->>DB: Save message
    WS_Server-->>Client: Broadcast message to other users

    Client->>REST_API: GET /messages/{group_id}
    REST_API-->>Client: JSON with message history
