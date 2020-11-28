#!/bin/bash

export FLASK_ENV=development
ln -sf /run/secrets/db_password ./db_password
python backend.py
