# Websocket Chat 

Swagger: http://localhost:8000/docs

***API: 

## Users

#### Create user:
- Endpoint: POST /users
- Payload:
```js
    {
    
      "username": 'Sample username',                # type: string
    }
```

## Messages

#### Fetch all messages in a group: 
- Endpoint: GET /messages/{group_id}



## Groups

#### Fetch  Bars: 
- Endpoint: GET /groups

#### Create  Bars: 
- Endpoint: POST /groups
- Payload:
```js
    {
    
      "name": 'Sample  group name',                # type: string
    }
```



## Websocket Connection

#### Connect websocket: 
- Endpoint: WS /ws?group_name={group_name}
- Query Params: 
```js
    {
      "group_name": "Sample group name",                # type: string
    }
```

#### Sending message:
- message format:
```js
    {
      "username": "Sameple username",                    # type: string
      "message": "Sample message"                        # type: string
    }
```