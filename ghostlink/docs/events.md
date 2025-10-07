# Event Protocol

## Trace Event Schema
```json
{
  "type": "object",
  "required": [
    "ts",
    "kind",
    "data"
  ],
  "properties": {
    "ts": {
      "type": "string"
    },
    "kind": {
      "type": "string"
    },
    "data": {
      "type": "object"
    },
    "hash": {
      "type": "string"
    }
  }
}
```

## Event Kinds
- BOOT
- ROUTE
- TOOL
- PIPELINE_STAGE
- SNAPSHOT
- HALT
- ERROR
