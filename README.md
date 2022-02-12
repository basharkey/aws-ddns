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
aws-ddns.py -r ddns.example.com -z ABCDE12345ABCDE123456
aws-ddns.py --record ddns.example.com --hosted-zone-id ABCDE12345ABCDE123456
```
