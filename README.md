# sun_auto_rm_checkin
## install
after clone this repo, run the following commands:
```shell
cd sun_auto_rm_checkin
```

step1:
```shell
sudo chmod +x auto_checkin/install.sh
```

step2:

- login to wsm to get the cookie

step3:
```shell
./auto_checkin/install.sh
```
and input the cookie you get in step2

step3: list all the crontab jobs
```shell
crontab -l
```
if you want to modify the crontab job, you can use the following command:
```shell
crontab -e
```

## Automation with GitHub actions
### Step 1: Fork this repo
### Step 2: Add secrets to your repo
- Add the following secrets to your repo:
  - `WSM_COOKIE`: the cookie you get from wsm, that was saved in the wsm_cookie.txt
