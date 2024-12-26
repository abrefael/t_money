## T-money, a Small Business Accounting app powered by the [frappe framework](https://frappe.io/framework)

Accounting for people with very small business (VAT free businesses) in Israel.

#### License

mit


For docker run:
```
mkdir output
docker build --build-arg CACHEBUST=$(date +%s) --tag=tmoney/accounting .
docker compose -f pwd.yml up -d
```

To update the app, run:
```
docker build --build-arg CACHEBUST=$(date +%s) --tag=tmoney/accounting .
docker compose -f up_pwd.yml up --force-recreate -d
```
