#!/bin/bash
source ~/.virtualenv/pyenv/bin/activate
python -m uvicorn backend.main:app --host 0.0.0.0 --port 5000 --reload
