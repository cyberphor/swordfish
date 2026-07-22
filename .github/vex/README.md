# `swordfish`  
**How Do I Add a VEX Document?**  
In the event you need to create a VEX document, use `vexctl` in the same way shown below.
```bash
vexctl create \
    --author "Victor Fernandez III" \
    --product="pkg:pypi/mcp@1.28.0" \
    --vuln="GHSA-vj7q-gjh5-988w" \
    --status="not_affected" \
    --justification="vulnerable_code_not_in_execute_path" > .github/vex/tools-vex.json 
```
