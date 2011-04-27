Reminder Bot
====

Just add reminder@asheesh.in to your friendlist in gmail and start using the service. To start just type 'hi' or 'help'.

How to use:
----

If you want to be reminded it once at some time, do following.

    remind <time> <message>

Following will create a recursive reminder.

    remind rec <count> <time> <message>

<time> can be either [0-9]<sec|min|hour> or <absolute time>

e.g.

    * remind 10hour pay phone bill       ---- It will remind you after 10hours to pay your phone bill
    * remind 20:00 book movie ticket     ---- reminds you to book ticket at 8PM
    * remind rec 5 11:00 project meeting ---- reminds you at 11AM for next 5days for project meeting
