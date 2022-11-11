# Tennis court booking bot

Having grown frustrated with not being able to book a tennis court in my local area, I decided to build a python bot (with selenium) that would automate the booking process, ensuring that I got a court each week at my preferred time.

Initially, the bot hit the website at the same time each week when the courts were released for booking. However, at this time there was no availability and  I realised that there was a one week period before public release where paid members were able to book courts. Not wanting to get a paid membership, I changed the script to hit the website every 5 mins (with datetime library) from the public release time so that as soon as someone canceled their court, my bot would book it.

## Usage

Pull this repo and adapt it to your needs. Add .env file with the relevant information.

### How to run program:

```
pip3 install -r requirements.txt
python3 app.py
```

