# staging/post_deploy.sh
#!/usr/bin/env bash

# Load fixtures with test data.
python manage.py loaddata dummy.json
python manage.py loaddata coupon.json
