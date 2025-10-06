# Opcode Specification

## Grammar
```
program := (command NEWLINE)*; command := IDENT (WS arg)*; arg := STRING | NUMBER | IDENT;
```

## Map
- `T:generate[english]->tool.gen`
- `T:explain[python]->tool.doc`
- `T:compress[tool]->shard.zip`
- `T:expand[opcode]->tool.unzip`
- `T:reforge[fragment]->tool.repair`
- `T:route[tools]->chain`
- `T:validate[tool@time]->verdict`
