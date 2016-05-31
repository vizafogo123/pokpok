#!/usr/bin/env bash
cp ./lion/*.py /Library/Python/2.7/site-packages/pyjs-0.8.2-py2.7.egg/pokpok/lion/
cp ./lion/*.py /Library/Python/2.7/site-packages/pyjs-0.8.2-py2.7.egg/pyjswidgets/pokpok/lion/
cp ./app/*.py /Library/Python/2.7/site-packages/pyjs-0.8.2-py2.7.egg/pokpok/app/
cp ./app/*.py /Library/Python/2.7/site-packages/pyjs-0.8.2-py2.7.egg/pyjswidgets/pokpok/app/

python2.7 //anaconda/bin/pyjsbuild Hello.py
