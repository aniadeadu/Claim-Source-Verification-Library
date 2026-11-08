
import json
from pathlib import Path
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

# Locate the project directory
folder = Path(__file__).resolve().parent.parent

# Locate the JSON Schema file
schema_path = folder / "data" / "schema.json"

# Check whether the schema file exists
if not schema_path.exists():
    raise FileNotFoundError(
        f"Schema file not found: {schema_path}"
    )

# Load the schema
try:
    with open(schema_path, "r", encoding="utf-8") as file:
        schema = json.load(file)

except json.JSONDecodeError as error:
    print("INVALID JSON:", error)
    raise SystemExit(1)

# Check the schema against Draft 2020-12
try:
    Draft202012Validator.check_schema(schema)

    print("SUCCESS: The JSON Schema is valid.")
    print("Schema version: Draft 2020-12")
    print("Schema file:", schema_path.name)

except SchemaError as error:
    print("SCHEMA ERROR:", error.message)
    print("Problem location:", list(error.absolute_path))
    raise SystemExit(1)
