#!/bin/bash

pytest -vv -s --alluredir=reportallure

allure serve ./reportallure --host 0.0.0.0 --port 8080