# use ubuntu as builder 
FROM ubuntu:24.04 AS builder

RUN apt-get update && apt-get install --no-install-recommends -y \
    python3.12 \
    python3.12-venv \
    python3-pip \
    build-essential \
    && rm -rf /var/lib/apt/lists/*


# create and activate virtual environment
RUN python3.12 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# install requirements from requirements.txt
COPY . . 
RUN pip install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip install .

################################################################

# use ffmpeg image to run
FROM jrottenberg/ffmpeg:8.1-ubuntu2404 as runner

# install python on runner
RUN apt-get update && apt-get install --no-install-recommends -y python3.12 python3.12-venv iproute2 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY --from=builder /opt/venv /opt/venv

# make sure all messages always reach console
ENV PYTHONUNBUFFERED=1

# activate virtual environment
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN ls -lh -a

USER ubuntu
WORKDIR /home/ubuntu

# Override default entrypoint
ENTRYPOINT ["python", "-m", "experiments_engine"] 
CMD []
