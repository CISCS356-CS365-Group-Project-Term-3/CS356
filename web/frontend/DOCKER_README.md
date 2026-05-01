# User Management

## Database Setup

PostgreSQL runs in Docker. The schema is applied automatically on first start.

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

We can use the personal version for free 

### Configuration

Copy `.env.example` to a `.env` and edit if needed.

Our default values in `.env.example`:

| Variable | Default |
|---|---|
| POSTGRES_USER | admin |
| POSTGRES_PASSWORD | admin123 |
| POSTGRES_DB | user_management |
| POSTGRES_PORT | 5432 |

### Running

Start the database:

`docker compose up -d`
In terminal

`docker compose up`
Without -d it runs in the foreground and you'd see live logs until you hit Ctrl+C


Stop the database:

```bash
docker compose down
```

### Connecting

| Property | Value |
| Host | localhost |
| Port | 5432 |
| Database | user_management |
| User | admin |
| Password | admin123 |

Connection string:

```
postgresql://admin:admin123@localhost:5432/user_management
```

### Notes

- Data does not persist between `docker compose down` and `docker compose up` - the database is re-initialised from `db/schema.sql` each time. This can be changed but since we don't have data currently I didn't add this in yet.
- The schema file is at `db/schema.sql`.
