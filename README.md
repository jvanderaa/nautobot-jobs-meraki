# nautobot-meraki-users

Meraki user management via job. This is meant as a start of a demonstration of using Nautobot Jobs. There are other capabilities that are clearly capable of adding.

To use, see blog post on josh-v.com. 

## Requirements

`meraki` Python SDK installed into the Nautobot environment. If following the system install documentation, here are the next steps:

- Become the `nautobot` user
- Pip install Meraki
- Exit to non-nautobot user
- Restart services

```
sudo -iu nautobot
pip install meraki
exit
sudo systemctl restart nautobot nautobot-worker
```

## Ideas That Are Not Implemented

- User deletion
  - This has other implications that I don't think creating a job that can delete users is going to be a good idea at this time
- User check
- Update user networks

> There is likely much more to come on this front.