# Robinhood Custom Backend

This shows an example of how to add a custom backend.

Currently there are 3 widgets
- Holdings - showing current equity positions
- L2 data - tabular format of L2 data (RH Gold required)
- L2 chart - showing order book depth (Gold also required)

After you clone the repo, you can run:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Make sure that RH_EMAIL and RH_PASS are set in the .env file.

```bash
RH_EMAIL=''
RH_PASS=''
```

You can launch with
```cython
uvicorn main:app --host 0.0.0.0 --port 8000
```

**IF YOU HAVE MFA - THE LOGIN WILL ASK YOU FOR THE CODE.  IF YOU
HAVE APP VERIFICATION ON, ACCEPT THE APP POPUP THEN JUST HIT ENTER"**


