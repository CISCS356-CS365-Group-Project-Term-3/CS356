FROM python:3.12-slim AS builder

WORKDIR /app

COPY pyproject.toml .
COPY src ./src

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip
RUN pip install .


################################################################

# use python image to run
FROM python:3.12-slim AS runner

COPY --from=builder /opt/venv /opt/venv

# make sure all messages always reach console
ENV PYTHONUNBUFFERED=1

# activate virtual environment
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"
ENV DB_PASSWORD="hello"

RUN ls -lh -a

USER root
WORKDIR /home/ubuntu

# Override default entrypoint
ENTRYPOINT ["/opt/venv/bin/python", "-m", "infra_management"] 
CMD []