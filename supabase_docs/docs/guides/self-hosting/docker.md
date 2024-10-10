[![Supabase wordmark](/docs/_next/image?url=%2Fdocs%2Fsupabase-
dark.svg&w=256&q=75&dpl=dpl_BJ9ShNdrRifaAcUSP15Lr1pJVtdF)![Supabase
wordmark](/docs/_next/image?url=%2Fdocs%2Fsupabase-
light.svg&w=256&q=75&dpl=dpl_BJ9ShNdrRifaAcUSP15Lr1pJVtdF)DOCS](/docs)

  * [Start](/docs/guides/getting-started)
  * Products
  * Build
  * Manage
  * Reference
  * Resources

[![Supabase wordmark](/docs/_next/image?url=%2Fdocs%2Fsupabase-
dark.svg&w=256&q=75&dpl=dpl_BJ9ShNdrRifaAcUSP15Lr1pJVtdF)![Supabase
wordmark](/docs/_next/image?url=%2Fdocs%2Fsupabase-
light.svg&w=256&q=75&dpl=dpl_BJ9ShNdrRifaAcUSP15Lr1pJVtdF)DOCS](/docs)

Search docs...

K

Self-Hosting

  1. [Self-Hosting](/docs/guides/self-hosting)
  2.   3. [Self-Hosting with Docker](/docs/guides/self-hosting/docker)
  4. 

# Self-Hosting with Docker

## Learn how to configure and deploy Supabase with Docker.

* * *

Docker is the easiest way to get started with self-hosted Supabase. This guide
assumes you are running the command from the machine you intend to host from.

## Before you begin#

You need the following installed in your system: [Git](https://git-
scm.com/downloads) and Docker
([Windows](https://docs.docker.com/desktop/install/windows-install/),
[MacOS](https://docs.docker.com/desktop/install/mac-install/), or
[Linux](https://docs.docker.com/desktop/install/linux-install/)).

## Running Supabase#

Follow these steps to start Supabase locally:

GeneralAdvanced

`  

_14

# Get the code

_14

git clone --depth 1 https://github.com/supabase/supabase

_14

_14

# Go to the docker folder

_14

cd supabase/docker

_14

_14

# Copy the fake env vars

_14

cp .env.example .env

_14

_14

# Pull the latest images

_14

docker compose pull

_14

_14

# Start the services (in detached mode)

_14

docker compose up -d

  
`

If you are using rootless docker, edit `.env` and set `DOCKER_SOCKET_LOCATION`
to your docker socket location. For example: `/run/user/1000/docker.sock`.
Otherwise, you will see an error like `container supabase-vector exited (0)`.

After all the services have started you can see them running in the
background:

`  

_10

docker compose ps

  
`

Please secure your services as soon as possible using the instructions below.

For security reasons, we "pin" the versions of each service in the docker-
compose file (these versions are updated ~monthly). If you want to update any
services immediately, you can do so by updating the version number in the
docker compose file and then running `docker compose pull`. You can find all
the latest docker images in the [Supabase Docker
Hub](https://hub.docker.com/u/supabase).

### Accessing Supabase dashboard#

You can access the Supabase Dashboard through the API gateway on port `8000`.
For example: `http://<your-ip>:8000`, or
[localhost:8000](http://localhost:8000) if you are running Docker locally.

You will be prompted for a username and password. By default, the credentials
are:

  * Username: `supabase`
  * Password: `this_password_is_insecure_and_should_be_updated`

You should change these credentials as soon as possible using the instructions
below.

### Accessing the APIs#

Each of the APIs are available through the same API gateway:

  * REST: `http://<your-ip>:8000/rest/v1/`
  * Auth: `http://<your-domain>:8000/auth/v1/`
  * Storage: `http://<your-domain>:8000/storage/v1/`
  * Realtime: `http://<your-domain>:8000/realtime/v1/`

### Accessing your Edge Functions#

Edge Functions are stored in `volumes/functions`. The default setup has a
`hello` Function that you can invoke on `http://<your-
domain>:8000/functions/v1/hello`.

You can add new Functions as `volumes/functions/<FUNCTION_NAME>/index.ts`.
Restart the `functions` service to pick up the changes: `docker compose
restart functions --no-deps`

### Accessing Postgres#

You can connect to the Postgres database locally on port `5432`. For example,
if you have `psql` on your local machine you can run:

`  

_10

psql -h 127.0.0.1 -p 5432 -d postgres -U postgres

  
`

The default password is `your-super-secret-and-long-postgres-password`. You
should change this as soon as possible using the instructions below. By
default the database is not accessible from outside the local machine. You can
change this by updating the `docker-compose.yml` file.

## Securing your services#

While we provided you with some example secrets for getting started, you
should NEVER deploy your Supabase setup using the defaults we have provided.
Please follow all of the steps in this section to ensure you have a secure
setup, and then restart all services to pick up the changes.

### Generate API keys#

Create a new `JWT_SECRET` and store it securely.

We can use your JWT Secret to generate new `anon` and `service` API keys using
the form below. Update the "JWT Secret" and then run "Generate JWT" once for
the `SERVICE_KEY` and once for the `ANON_KEY`:

### Update API keys#

Replace the values in the `.env` file:

  * `ANON_KEY` \- replace with an `anon` key
  * `SERVICE_ROLE_KEY` \- replace with a `service` key

You will need to restart the services for the changes to take effect.

### Update secrets#

Update the `.env` file with your own secrets. In particular, these are
required:

  * `POSTGRES_PASSWORD`: the password for the `postgres` role.
  * `JWT_SECRET`: used by PostgREST and GoTrue, among others.
  * `SITE_URL`: the base URL of your site.
  * `SMTP_*`: mail server credentials. You can use any SMTP server.

You will need to restart the services for the changes to take effect.

### Dashboard authentication#

The dashboard is protected with Basic Authentication. The default user and
password MUST be updated before using Supabase in production. Update the
following values in the `.env` file:

  * `DASHBOARD_USERNAME`: The default username for the Dashboard
  * `DASHBOARD_PASSWORD`: The default password for the Dashboard

You can also add more credentials in `./docker/volumes/api/kong.yml`. For
example:

docker/volumes/api/kong.yml

`  

_10

basicauth_credentials:

_10

- consumer: DASHBOARD

_10

username: user_one

_10

password: password_one

_10

- consumer: DASHBOARD

_10

username: user_two

_10

password: password_two

  
`

You will need to restart the services for the changes to take effect.

## Restarting all services#

You can restart services to pick up any configuration changes by running:

`  

_10

# Stop and remove the containers

_10

docker compose down

_10

_10

# Recreate and start the containers

_10

docker compose up -d

  
`

Be aware that this will result in downtime. Simply restarting the services
does not apply configuration changes.

## Stopping all services#

You can stop Supabase by running `docker compose stop` in same directory as
your `docker-compose.yml` file.

## Uninstalling#

You can stop Supabase by running the following in same directory as your
`docker-compose.yml` file:

`  

_10

# Stop docker and remove volumes:

_10

docker compose down -v

_10

_10

# Remove Postgres data:

_10

rm -rf volumes/db/data/

  
`

This will destroy all data in the database and storage volumes, so be careful!

## Managing your secrets#

Many components inside Supabase use secure secrets and passwords. These are
listed in the self-hosting [env
file](https://github.com/supabase/supabase/blob/master/docker/.env.example),
but we strongly recommend using a secrets manager when deploying to
production. Plain text files like dotenv lead to accidental costly leaks.

Some suggested systems include:

  * [Doppler](https://www.doppler.com/)
  * [Infisical](https://infisical.com/)
  * [Key Vault](https://docs.microsoft.com/en-us/azure/key-vault/general/overview) by Azure (Microsoft)
  * [Secrets Manager](https://aws.amazon.com/secrets-manager/) by AWS
  * [Secrets Manager](https://cloud.google.com/secret-manager) by GCP
  * [Vault](https://www.hashicorp.com/products/vault) by Hashicorp

## Advanced#

Everything beyond this point in the guide helps you understand how the system
works and how you can modify it to suit your needs.

### Architecture#

Supabase is a combination of open source tools, each specifically chosen for
Enterprise-readiness.

If the tools and communities already exist, with an MIT, Apache 2, or
equivalent open license, we will use and support that tool. If the tool
doesn't exist, we build and open source it ourselves.

  * [Kong](https://github.com/Kong/kong) is a cloud-native API gateway.
  * [GoTrue](https://github.com/supabase/gotrue) is an JWT based API for managing users and issuing JWT tokens.
  * [PostgREST](http://postgrest.org/) is a web server that turns your PostgreSQL database directly into a RESTful API
  * [Realtime](https://github.com/supabase/realtime) is an Elixir server that allows you to listen to PostgreSQL inserts, updates, and deletes using websockets. Realtime polls Postgres' built-in replication functionality for database changes, converts changes to JSON, then broadcasts the JSON over websockets to authorized clients.
  * [Storage](https://github.com/supabase/storage-api) provides a RESTful interface for managing Files stored in S3, using Postgres to manage permissions.
  * [postgres-meta](https://github.com/supabase/postgres-meta) is a RESTful API for managing your Postgres, allowing you to fetch tables, add roles, and run queries, etc.
  * [PostgreSQL](https://www.postgresql.org/) is an object-relational database system with over 30 years of active development that has earned it a strong reputation for reliability, feature robustness, and performance.
  * [Supavisor](https://github.com/supabase/supavisor) is a scalable connection pooler for Postgres, allowing for efficient management of database connections.

For the system to work cohesively, some services require additional
configuration within the Postgres database. For example, the APIs and Auth
system require several [default roles](/docs/guides/database/postgres/roles)
and the `pgjwt` Postgres extension.

You can find all the default extensions inside the [schema migration scripts
repo](https://github.com/supabase/postgres/tree/develop/migrations). These
scripts are mounted at `/docker-entrypoint-initdb.d` to run automatically when
starting the database container.

### Configuring services#

Each system has a number of configuration options which can be found in the
relevant product documentation.

  * [Postgres](https://hub.docker.com/_/postgres/)
  * [PostgREST](https://postgrest.org/en/stable/configuration.html)
  * [Realtime](https://github.com/supabase/realtime#server)
  * [GoTrue](https://github.com/supabase/gotrue)
  * [Storage](https://github.com/supabase/storage-api)
  * [Kong](https://docs.konghq.com/gateway/latest/install/docker/)
  * [Supavisor](https://supabase.github.io/supavisor/development/docs/)

These configuration items are generally added to the `env` section of each
service, inside the `docker-compose.yml` section. If these configuration items
are sensitive, they should be stored in a [secret manager](/docs/guides/self-
hosting#managing-your-secrets) or using an `.env` file and then referenced
using the `${}` syntax.

docker-compose.yml

.env

`  

_10

services:

_10

rest:

_10

image: postgrest/postgrest

_10

environment:

_10

PGRST_JWT_SECRET: ${JWT_SECRET}

  
`

### Common configuration#

Each system can be [configured](../self-hosting#configuration) independently.
Some of the most common configuration options are listed below.

#### Configuring an email server#

You will need to use a production-ready SMTP server for sending emails. You
can configure the SMTP server by updating the following environment variables:

.env

`  

_10

SMTP_ADMIN_EMAIL=

_10

SMTP_HOST=

_10

SMTP_PORT=

_10

SMTP_USER=

_10

SMTP_PASS=

_10

SMTP_SENDER_NAME=

  
`

We recommend using [AWS SES](https://aws.amazon.com/ses/). It's extremely
cheap and reliable. Restart all services to pick up the new configuration.

#### Configuring S3 Storage#

By default all files are stored locally on the server. You can configure the
Storage service to use S3 by updating the following environment variables:

docker-compose.yml

`  

_10

storage:

_10

environment:

_10

STORAGE_BACKEND=s3

_10

GLOBAL_S3_BUCKET=name-of-your-s3-bucket

_10

REGION=region-of-your-s3-bucket

  
`

You can find all the available options in the [storage
repository](https://github.com/supabase/storage-api/blob/master/.env.sample).
Restart the `storage` service to pick up the changes: `docker compose restart
storage --no-deps`

#### Setting database's `log_min_messages`#

By default, `docker compose` sets the database's `log_min_messages`
configuration to `fatal` to prevent redundant logs generated by Realtime. You
can configure `log_min_messages` using any of the Postgres [Severity
Levels](https://www.postgresql.org/docs/current/runtime-config-
logging.html#RUNTIME-CONFIG-SEVERITY-LEVELS).

#### Accessing Postgres through Supavisor#

By default, the Postgres database is accessible through the Supavisor
connection pooler. This allows for more efficient management of database
connections. You can connect to the pooled database using the
`POOLER_PROXY_PORT_TRANSACTION` port and `POSTGRES_PORT` for session based
connections.

For more information on configuring and using Supavisor, see the [Supavisor
documentation](https://supabase.github.io/supavisor/).

#### Exposing your Postgres database#

If you need direct access to the Postgres database without going through
Supavisor, you can expose it by updating the `docker-compose.yml` file:

docker-compose.yml

`  

_10

# Comment or remove the supavisor section of the docker-compose file

_10

# supavisor:

_10

# ports:

_10

# ...

_10

db:

_10

ports:

_10

- ${POSTGRES_PORT}:${POSTGRES_PORT}

  
`

This is less-secure, so please make sure you are running a firewall in front
of your server.

#### File storage backend on macOS#

By default, Storage backend is set to `file`, which is to use local files as
the storage backend. For macOS compatibility, you need to choose `VirtioFS` as
the Docker container file sharing implementation (in Docker Desktop ->
Preferences -> General).

#### Setting up logging with the Analytics server#

Additional configuration is required for self-hosting the Analytics server.
For the full setup instructions, see [Self Hosting
Analytics](https://supabase.com/docs/reference/self-hosting-
analytics/introduction#getting-started).

### Upgrading Analytics#

Due to the changes in the Analytics server, you will need to run the following
commands to upgrade your Analytics server:

All data in analytics will be deleted when you run the commands below.

`  

_10

### Destroy analytics to transition to postgres self hosted solution without
other data loss

_10

_10

# Enter the container and use your .env POSTGRES_PASSWORD value to login

_10

docker exec -it $(docker ps | grep supabase-db | awk '{print $1}') psql -U supabase_admin --password

_10

# Drop all the data in the _analytics schema

_10

DROP PUBLICATION logflare_pub; DROP SCHEMA _analytics CASCADE; CREATE SCHEMA
_analytics;\q

_10

# Drop the analytics container

_10

docker rm supabase-analytics

  
`

* * *

## Demo#

A minimal setup working on Ubuntu, hosted on Digital Ocean.

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/content/guides/self-
hosting/docker.mdx)

  * Need some help?

[Contact support](https://supabase.com/support)

  * Latest product updates?

[See Changelog](https://supabase.com/changelog)

  * Something's not right?

[Check system status](https://status.supabase.com/)

* * *

[© Supabase
Inc](https://supabase.com/)—[Contributing](https://github.com/supabase/supabase/blob/master/apps/docs/DEVELOPERS.md)[Author
Styleguide](https://github.com/supabase/supabase/blob/master/apps/docs/CONTRIBUTING.md)[Open
Source](https://supabase.com/open-
source)[SupaSquad](https://supabase.com/supasquad)Privacy Settings

[GitHub](https://github.com/supabase/supabase)[Twitter](https://twitter.com/supabase)[Discord](https://discord.supabase.com/)

