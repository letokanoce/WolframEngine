FROM python:3.10.9
WORKDIR /WolframEngine
COPY app /WolframEngine/app
COPY main.py /WolframEngine
COPY requirements.txt /WolframEngine
RUN pip install -r requirements.txt
EXPOSE 3002
CMD ["python", "main.py"]