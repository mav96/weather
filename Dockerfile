FROM python:3.6
RUN pip install falcon pyowm pymemcache
COPY main.py main.py
CMD ["python", "main.py"] 
