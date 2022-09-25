FROM python:3.9
ADD main.py /
RUN pip freeze > requirements.txt
RUN pip3 install -r ./requirements.txt
CMD [ "python", "./main.py" ]
