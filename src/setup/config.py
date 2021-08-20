#!usr/bin/env python3
#-*-coding:utf-8-*-

import json
import os
import sys
from deepmerge import always_merger

class Config:
    instance = None

    def __new__(cl):
        if cl.instance is None: cl.instance = super().__new__(cl)
        return cl.instance

    def __init__(self):
        with open("config/config.json", "r") as f:
            self.base = json.load(f)
        self.dev, self.staging, self.prod = {}, {}, {}
        if os.access("config/config.development.json", os.R_OK):
            with open("config/config.development.json", "r") as f:
                self.dev = json.load(f)
        if os.access("config/config.staging.json", os.R_OK):
            with open("config/config.staging.json", "r") as f:
                self.staging = json.load(f)
        if os.access("config/config.production.json", os.R_OK):
            with open("config/config.production.json", "r") as f:
                self.prod = json.load(f)

        self.environment = None
        if len(sys.argv) > 1 and sys.argv[1] in ["development", "staging", "production"]:
            self.environment = sys.argv[1]

        self.merged = dict(self.base)
        if self.environment is None or self.environment == "development":
            always_merger.merge(self.merged, self.dev)
        if self.environment is None or self.environment == "staging":
            always_merger.merge(self.merged, self.staging)
        if self.environment is None or self.environment == "production":
            always_merger.merge(self.merged, self.prod)

    def __getitem__(self, key):
        return self.merged[key]
