#!/bin/bash
pip list --outdated | sed 's/(.*//g' | xargs pip install -U
