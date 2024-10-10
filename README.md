

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


