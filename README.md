# Fresh Store
A file based key-value local storage.

### Requirements -
**Python 3.6+**
Tested on Linux and Windows.

### API -
| **Method name** | **Arguments** | **Returns** | **Description** |
|---|---|---|---|
| **create** | **key** (str): to access data | **None** | Create an entry into the data store. |
|  | **value file** (str): the JSON file path |  | Raises error for duplicate key. |
|  | [OPTIONAL] **TTL** (int): Accessible time (in seconds). |   |   |
| **read** | **key:** (str): to access data | **JSON object** (str) | Retrieve entry from the data store. |
| **delete** | **key:** (str): to access data | **JSON object** (str) | Delete entry from the data store. |

Both **read** and **delete** return "" for key not found.

### Usage -
```bash
git clone https://github.com/ryanreh99/fresh_store.git
cd fresh_store
python3 # opens up shell
```

```python
import fresh_store
obj = fresh_store.FreshStore() # Optional file argument
obj.create("first key", "tests/examples/example_1.json")
read_obj = obj.read("first key")
no_object = obj.delete("non-existant key")
print(read_obj)
```

### Testing
```bash
# Inside `fresh_store` directory
python3 -m tests.test_api

# See comment in tests/test_api.py
# Remove `tearDownClass` method
# and view TEST_DATA_STORE.json
python3 tests/test_threading.py
# Restore changes to test_api.py
# and delete newly created JSON.
```