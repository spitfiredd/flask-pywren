# Based on: https://github.com/ibm-functions/runtime-python/tree/master/python3.7
# See https://github.com/pywren/pywren-ibm-cloud/tree/master/runtime
# for building custom pywren runtimes

FROM ibmfunctions/action-python-v3.7:master
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt