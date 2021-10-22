## Data Stream Alerter 
to analyze logs that are being sent by SDK running on mobile devices.

### CSV structure
```csv
error_type,datetime,bundle_id
```

error_type's: FATAL, ERROR

#### add permission for docker

```shell
chmod 777 csv
```

### Alert Rules

- Alert over 10 fatal logs in less than a minute (by DateTime)
- Alert over 10 error or fatal logs in less than an hour for a specific bundle id

#### New alert Rules

can be added as plugin in plugins folder
```python
class Alerter:
    @staticmethod
    def process(data):
        ...
```

### Pandas as Stream Reader
[Support a bunch of data types](https://pandas.pydata.org/docs/user_guide/io.html)