# DocumentationDB


It is just a tool made in python for help in database documentation (only tested at windows).

It spool some html files, after read some config files.

## Installation

Windows:

```sh
pip install requirements.txt
```

## Configuration

Basicaly we need a file (.env) of exist configuration path spool and there exist the key of cryptography, but only execute script for first time to create file (.env).

To configure the databases and queries, execute the second time and script will copy of template folder to config folder, so edit the 2 files (query.json and instance.json), after executed the passwords at instance.json will be encrypt.

## Example of query.json
example:
```json
{
    "oracle": [{
        "id": "test_oracle",
        "header": "Test",
        "query": "SELECT 1 FROM dual"
    }],
    "mssql":[{
        "id": "test_mssql",
        "header": "Test",
        "query": "SELECT getdate()"
    }]
}
```

Observation: when you need use " at query use backslash before, example: \\" .

Example query: 
 
```json
{
    "id": "test_oracle",
    "header": "Test",
    "query": "SELECT 1 \"teste\" FROM dual"
}
```

## Example of instance.json
example:
```json
{
    "instance": [
        {
            "name": "TestOracle",
            "ip": "192.168.1.1",
            "instanceType": "oracle",
            "type": "Test",
            "user": "user",
            "password": "password",
            "connectionString": "192.168.1.1:1521/Testdb",
            "database": "use only when mssql",
            "query": [
                "test_oracle"
            ]
        },
        {
            "name": "TestMSSQL",
            "ip": "192.168.1.1",
            "instanceType": "mssql",
            "type": "Test",
            "user": "user",
            "password": "password",
            "connectionString": "192.168.1.1",
            "database": "xxx",
            "query": [
                "test_mssql"
            ]
        },
        
    ]
}
```

## Example of usage

Just call on cmd:
```sh
python3 documentation.py
```



