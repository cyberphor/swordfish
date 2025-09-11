## Backend
The steps below describe how the `backend` service was started.

**Step 1.** Install Python.
```bash
sudo apt update
sudo apt install -y python3 python3-venv
```

**Step 2.** Create a Python virtual environment called `.venv` in the root of this project. 
```bash
python -m venv .venv
```

**Step 3.** Activate the Python virtual environment you just created. 
```bash
source .venv/bin/activate
```

**Step 4.** Install the `backend` service's current Python dependencies.
```bash
python -m pip install -r backend/requirements.txt
```

**Step 5.** Make changes to the source.

**Step 6.** Start the `backend` service and make sure it works.
```bash
python backend/server.py
```

**Step 7.** Stop the `backend` service and go back to step 4.
