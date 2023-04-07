# AWS DDNS

Dynamic DNS program for updating AWS DNS A records based on your public IP.


Requires AWS CLI configured on host and user with following policy permissions:

```
route53:ChangeResourceRecordSets
route53:ListResourceRecordSets
```


Installation:

```
pip3 install -r requirements.txt
```


Usage:

```
aws-ddns.py -r ddns.example.com. -z ABCDE12345ABCDE123456
aws-ddns.py --record ddns.example.com. --hosted-zone-id ABCDE12345ABCDE123456
```

## Docker

```
docker build . -t aws-ddns
docker run --rm --mount type=bind,src="/home/<user>/.aws/credentials",target="/root/.aws/credentials" --name ddns aws-ddns:latest --record ddns.example.com. --hosted-zone-id ABCDE12345ABCDE123456
```
