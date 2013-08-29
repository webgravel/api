#!/bin/bash

GHOME=/gravel/system/api
mkdir -p $GHOME
chmod 700 $GHOME

useradd --system --gid daemon \
    --home-dir $GHOME \
    gravelapi

chown gravelapi:daemon $GHOME
