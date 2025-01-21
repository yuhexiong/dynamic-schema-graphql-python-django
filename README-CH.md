# Dynamic Schema GraphQL Django

使用 YAML 定義 Doris 表格結構並在 GraphiQL 中取得資料。  

## Overview

- 語言：Python v3.12  
- 網頁框架：Django v4.1  

### ENV

將 `.env.example` 複製為 `.env`  
可以更改 `SECRET_KEY`  
```yaml
SECRET_KEY='django-insecure-qywaz)eg+ua2q26x$^3*&sr&gh0ca74*n^mm4j-*h)!80#&^9p'
DEBUG=True
```

`etc/database.yaml`  
```yaml
host: localhost
name: database
user: root
password: password
port: 9030
```

`etc/schema.yaml`  
支援的資料類型：`String`, `Integer`, `Double`, `Date`
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

啟用 Poetry 環境  
Windows: 點擊 `.venv/Scripts/activate.bat`  

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