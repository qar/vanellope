#! /usr/bin/python
# coding=utf-8
#
# Frequently used regex pattern
#

# User registered name
UNAME = r'^[a-zA-Z0-9]{1,16}$'

# Email
EMAIL = r'^[a-z0-9\.]+@[a-z0-9]+\.[a-z]{2,4}$'

# CSS color value
COLOR = r"#[0-9a-fA-F]{6}"


# Notificatin
### THIS IS EXPERIMENTAL
NOTICE = r"[ ]+@[a-zA-Z0-9]{1,16}[ ]+"