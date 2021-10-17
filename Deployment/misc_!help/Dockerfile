# syntax=docker/dockerfile:1
FROM python
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN rm requirements.txt
RUN apt-get update && apt-get install -y iputils-ping
ENV BOT_TOKEN=ODc3Mzk3MTk2NTE1OTk5ODE1.YRyB0A.3lrE2CAf1CVFAUm4RthnVKENvJM
COPY source.py /app/files/source.py
COPY flag.txt flag.txt
COPY image0.png /app/files/image0.png
COPY image1.png /app/files/image1.png
COPY image2.png /app/files/image2.png
COPY image3.png /app/files/image3.png
CMD cd /app/files && python source.py