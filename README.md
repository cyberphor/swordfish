## `swordfish`

**Step 1.** Build the containers.
```bash
make
```

**Step 2.** Start the containers.
```bash
make start
```

**Step 3.** Create a public and private key. 
```bash
openssl req -x509 -newkey rsa:2048 -keyout client.key -out client.crt -days 365 -nodes
```

**Step 4.** Create a file called `.env` and add the content below to it.
```bash
export EMASS_API_CERTIFICATE=client.crt
export EMASS_API_KEY=client.key
export EMASS_API_KEY=aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee
export EMASS_USER_UID=1234567890
```

**Step 5.** Run the provided script to confirm the mock eMASS API server is working.
```bash
bash demo.sh
```

