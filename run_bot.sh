#!/usr/bin/env bash
cur_dir=$(dirname $0)
source $cur_dir/venv/bin/activate
source $cur_dir/.env
python3 $cur_dir/bot.py