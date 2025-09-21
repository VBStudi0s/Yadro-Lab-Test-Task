#!/bin/bash

pytest -vv -s --alluredir=/tmp/allure-report

allure serve /tmp/allure-report --host 0.0.0.0 --port 8080