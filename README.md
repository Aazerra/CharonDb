# CharonDB

A package for working with databases with mullti drivers



## Available Drivers

- [x] Mysql
- [ ] Sqlite3

## Example

```python
from charondb import MySQLManager

storage = MySQLManager(username="username", password="password",
                       host="host", database="database name", port="port", debug=True)
with open("./database.sql", "r") as sql_file:
    storage.import_database(sql_file) # .sql file
storage.insert(<table_name>, [<cols>], [<values>])
storage.exists(<table_name>, <where query>):
storage.close()
```

