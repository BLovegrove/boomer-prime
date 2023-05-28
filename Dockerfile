FROM python:3.10

COPY ./ /boomer/

RUN python3.10 -m pip install -r /boomer/requirements.txt

# Remove local copies as these files get mounted instead.
# RUN rm -r /bot/files

WORKDIR /boomer

CMD ["python3.10", "./bot/__main__.py"]