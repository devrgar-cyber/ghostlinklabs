# Rebuild Recipe

The deterministic rebuild pipeline executes the steps below in order:

1. mkdir -p ghostlink/{runtime,boot,access,core,mesh,lattice,tools,reflect,agents,diagnostic,neural_link,kernel,chains,opcode,shards,reforge,time,simulation,index,docs}
2. emit runtime/ghostlink.py from template:cli
3. emit tools/* from template:tools
4. write kernel/ghostcore.seed from seed
5. write chains/*, opcode/*, docs/*
6. create tests/*
