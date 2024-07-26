#!/bin/bash
sudo docker run --rm -dit \
    -p 8501:8501 \
    --name lang_st \
    lang_st