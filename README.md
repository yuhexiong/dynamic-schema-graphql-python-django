# Dynamic Schema GraphQL Django

**(also provided Traditional Chinese version document [README-CH.md](README-CH.md).)**


define Doris table schema in yaml and fetch data in GraphiQL.  


## Overview

- Language: Python v3.12
- Web FrameWork: Django v4.1


### ENV

copy `.env.example` as `.env`  
able to change SECRET_KEY  
```yaml
SECRET_KEY='django-insecure-qywaz)eg+ua2q26x$^3*&sr&gh0ca74*n^mm4j-*h)!80#&^9p'
DEBUG=True
```

etc/database.yaml
```yaml
host: localhost
name: database
user: root
password: password
port: 9030
```

etc/schema.yaml  
enabled data type: `String`, `Integer`, `Double`, `Date`
```yaml
tables:
  - name: adventure_game_heroes
    fields:
      - name: id
        type: Integer
      - name: hero_name
        type: String
      - name: occupation
        type: String
      - name: level
        type: Integer
      - name: weapon_name
        type: String
      - name: weapon_type
        type: String
      - name: weapon_power
        type: Double
      - name: equipment_status
        type: String
      - name: join_date
        type: Date
```

### Example Data

[adventure_game_heroes.sql](adventure_game_heroes.sql)

![image](./images/doris_example.png)


## Run

### Run Docker
```bash
docker compose up -d
```

### Run Local

```bash
poetry install
```

activate poetry environment  
windows: click .venv/Scripts/activate.bat  


```bash
python manage.py runserver
```

## UI
```
localhost:8000/graphql  
```

### Query

(i) filter option
```
"equals": value, 
"greater_than": value, 
"greater_than_or_equals": value,
"less_than": value, 
"less_than_or_equals": value, 
"between": {"start": value, "end": value}
```
(ii) limit  
(iii) offset  
(iv) order_by: [ {column, order: ASC/DESC} ]  

#### Example  
```graphql
query {
  adventure_game_heroes (
    filter: {
      join_date: {
        between: {
          start: "2023-04-01",
          end: "2023-10-01"
        }
      },
      occupation: {
        equals: "Warrior"
      }
    },
    limit: 3,
    offset: 0,
    order_by: [
      {
        column: "join_date",
        order: ASC
      }
    ]
  ) {
    id,
    join_date,
    hero_name,
    occupation,
    level,
    weapon_name,
    weapon_type,
    weapon_power,
    equipment_status
  }
}
```
![image](./images/ui_example.png)

### Swagger
```
localhost:8000/swagger-ui  
```