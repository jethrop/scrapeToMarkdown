[Back](/blog)

[Blog](/blog)

# NoSQL Postgres: Add MongoDB compatibility to your Supabase projects with
FerretDB

31 Jan 2024

•

6 minute read

[![Thor Schaeff
avatar](/_next/image?url=https%3A%2F%2Fgithub.com%2Fthorwebdev.png&w=96&q=75)Thor
SchaeffDevRel & DX](https://twitter.com/thorwebdev)

![NoSQL Postgres: Add MongoDB compatibility to your Supabase projects with
FerretDB](/_next/image?url=%2Fimages%2Fblog%2Fgetting-
started%2Fferretdb%2Fferretdb.jpg&w=3840&q=100)

[FerretDB](https://www.ferretdb.com/) is an open source document database that
adds MongoDB compatibility to other database backends, such as
[Postgres](https://www.postgresql.org/) and [SQLite](https://www.sqlite.org/).
By using FerretDB, developers can [access familiar MongoDB features and tools
using the same syntax and commands](https://blog.ferretdb.io/mongodb-crud-
operations-with-ferretdb/) for many of their use cases.

In this post, we'll start from scratch, running FerretDB locally via Docker,
trying out the connection with `mongosh` and the MongoDB Node.js client, and
finally deploy FerretDB to [Fly.io](https://fly.io/) for a production ready
set up.

If you prefer video guide, you can follow along below. And make sure to
subscribe to the [Supabase YouTube
channel](https://www.youtube.com/channel/UCNTVzV1InxHV-
YR0fSajqPQ?view_as=subscriber&sub_confirmation=1)!

## Prerequisites#

  * A Supabase project. Create yours here: [database.new](https://database.new).
  * [Docker](https://www.docker.com/) or [Orbstack](https://orbstack.dev/).
  * [Optional] A [Fly.io](https://fly.io/) account for production deployment.

## Run FerretDB locally with Docker#

FerretDB provides a [Docker
image](https://github.com/ferretdb/FerretDB/pkgs/container/ferretdb) allowing
us to run it locally, for example via [Orbstack](https://orbstack.dev/), with
a couple simple commands.

FerretDB only requires the Postgres database URI to be provided as the
`FERRETDB_POSTGRESQL_URL` environment variable. Every Supabase project comes
with a full Postgres database. You can find the connection URI string in your
[Supabase
Dashboard](https://supabase.com/dashboard/project/_/settings/database).

Make sure **Use connection pooling** is checked and **Session mode** is
selected. Then copy the URI. Replace the password placeholder with your saved
database password.

If your network supports IPv6 connections, you can also use the direct
connection string. Uncheck **Use connection pooling** and copy the new URI.

Terminal

`  

_10

# Set the required environment variables

_10

export DB_USER=postgres

_10

export DB_PASSWORD=<your db password>

_10

export SUPA_PROJECT_REF=<your Supabase project ref>

_10

export SUPA_REGION=<your project region>

_10

export
DB_URL=postgres://$DB_USER.$SUPA_PROJECT_REF:$DB_PASSWORD@$SUPA_REGION.pooler.supabase.com:5432/postgres

_10

_10

# Run FerretDB in docker container

_10

docker run -p 27017:27017 -p 8080:8080 -e FERRETDB_POSTGRESQL_URL=$DB_URL
ghcr.io/ferretdb/ferretdb

  
`

FerretDB runs on the default MongoDB port `27017` and also spins up some
monitoring tools on port `8080`. Once up and running you can access these at
[localhost:8080](http://localhost:8080).

Once up and running, constructing the MongoDB URI is easil:

Terminal

`  

_10

export MONGODB_URL=mongodb://$DB_USER.$SUPA_PROJECT_REF:[[email
protected]](/cdn-cgi/l/email-protection):27017/ferretdb?authMechanism=PLAIN

  
`

## Test with `mongosh`#

If you have MongoDB installed locally on your machine, you can test via
`mongosh`, the MongoDB shell.

Terminal

`  

_10

mongosh '$MONGODB_URL'

  
`

If you don't have MongoDB installed locally, you can run the shell via a
Docker container:

Terminal

`  

_10

docker run --rm -it --entrypoint=mongosh mongo \

_10

"$MONGODB_URL"

  
`

### Insert documents into FerretDB#

With `mongosh` running, let's try to insert some documents into our FerretDB
instance. You are going to insert two footballer data into a `players`
collection.

ferretdb>

`  

_33

db.players.insertMany([

_33

{

_33

futbin_id: 3,

_33

player_name: "Giggs",

_33

player_extended_name: "Ryan Giggs",

_33

quality: "Gold - Rare",

_33

overall: 92,

_33

nationality: "Wales",

_33

position: "LM",

_33

pace: 90,

_33

dribbling: 91,

_33

shooting: 80,

_33

passing: 90,

_33

defending: 44,

_33

physicality: 67

_33

},

_33

{

_33

futbin_id: 4,

_33

player_name: "Scholes",

_33

player_extended_name: "Paul Scholes",

_33

quality: "Gold - Rare",

_33

overall: 91,

_33

nationality: "England",

_33

position: "CM",

_33

pace: 72,

_33

dribbling: 80,

_33

shooting: 87,

_33

passing: 91,

_33

defending: 64,

_33

physicality: 82,

_33

base_id: 246

_33

}

_33

]);

  
`

Great! Now when you run `db.players.find()`, it should return all the
documents stored in the collection.

### Update document record in FerretDB#

Next, you need to update "Giggs" record to reflect his current position as a
`CM`. To do this, we can just run an `updateOne` command to target just that
particular player:

ferretdb>

`  

_10

db.players.updateOne(

_10

{ player_name: "Giggs" },

_10

{ $set: { position: "CM" } }

_10

);

  
`

Let's query the collection to see if the changes have been made:

ferretdb>

`  

_10

db.players.find({player_name: "Giggs"})

  
`

You can run many MongoDB operations on FerretDB. See the [list of supported
commands](https://docs.ferretdb.io/reference/supported-commands/) in the
FerretDB documentation for more.

## Inspect the JSONB data in the Supabase Dashboard#

FerretDB stores each collection in a table on the `ferretdb` schema, each
document represented by a JSONB entry. You can inspect this in the [Table
Editor](https://supabase.com/dashboard/project/_/editor) in your Supabase
Dashboard.

## Deploy to Fly.io#

For production use cases, you can easily deploy FerretDB on Fly. Simply create
a `fly.toml` file (make sure to [update
`primary_region`](https://fly.io/docs/reference/regions/))

fly.toml

`  

_17

app = "supa-ferretdb-<your-supabase-project-ref>"

_17

primary_region = "bos"

_17

_17

[build]

_17

image = "ghcr.io/ferretdb/ferretdb"

_17

_17

[[services]]

_17

internal_port = 27017

_17

protocol = "tcp"

_17

_17

[[services.ports]]

_17

port = "27017"

_17

_17

[[vm]]

_17

cpu_kind = "shared"

_17

cpus = 1

_17

memory_mb = 1024

  
`

And follow these [flyctl](https://fly.io/docs/hands-on/install-flyctl/)
commands:

  * fly launch --no-deploy
    * An existing fly.toml file was found for app supa-ferretdb?
    * Would you like to copy its configuration to the new app? (y/N) > y
  * fly secrets set FERRETDB_POSTGRESQL_URL=$DB_URL
  * fly deploy
  * fly ips allocate-v4
    * Note: this is a paid feature! You can test it for free as long as you [release the dedicated IPv4](https://community.fly.io/t/we-are-going-to-start-charging-for-dedicated-ipv4-in-january-1st/15970#how-not-to-be-billed-2) before the end of the billing period!

Now simply replace `127.0.0.1` in the `MONGODB_URL` with your dedicated IPv4
address and you're ready to roll!

## Conclusion#

FerretDB allows you to run MongoDB workloads on Postgres and SQLite. This
flexibility means you can easily add MongoDB compatibility to your Supabase
projects, while avoiding vendor lock-in and retaining control of your data
architecture.

To get started with FerretDB, check out the [FerretDB quickstart
guide](https://docs.ferretdb.io/quickstart-guide/).

## More Supabase#

  * [Migration guides](/docs/guides/resources#migrate-to-supabase)
  * [Options for connecting to your Postgres database](/docs/guides/database/connecting-to-postgres)

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fnosql-
mongodb-compatibility-with-ferretdb-and-
flydotio&text=NoSQL%20Postgres%3A%20Add%20MongoDB%20compatibility%20to%20your%20Supabase%20projects%20with%20FerretDB)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fnosql-
mongodb-compatibility-with-ferretdb-and-
flydotio&text=NoSQL%20Postgres%3A%20Add%20MongoDB%20compatibility%20to%20your%20Supabase%20projects%20with%20FerretDB)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fnosql-
mongodb-compatibility-with-ferretdb-and-
flydotio&t=NoSQL%20Postgres%3A%20Add%20MongoDB%20compatibility%20to%20your%20Supabase%20projects%20with%20FerretDB)

[Last postMatryoshka embeddings: faster OpenAI vector search using Adaptive
Retrieval13 February 2024](/blog/matryoshka-embeddings)

[Next postpgvector 0.6.0: 30x faster with parallel index builds30 January
2024](/blog/pgvector-fast-builds)

[postgres](/blog/tags/postgres)[developers](/blog/tags/developers)[mongodb](/blog/tags/mongodb)

On this page

  * Prerequisites
  * Run FerretDB locally with Docker
  * Test with `mongosh`
    * Insert documents into FerretDB
    * Update document record in FerretDB
  * Inspect the JSONB data in the Supabase Dashboard
  * Deploy to Fly.io
  * Conclusion
  * More Supabase

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fnosql-
mongodb-compatibility-with-ferretdb-and-
flydotio&text=NoSQL%20Postgres%3A%20Add%20MongoDB%20compatibility%20to%20your%20Supabase%20projects%20with%20FerretDB)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fnosql-
mongodb-compatibility-with-ferretdb-and-
flydotio&text=NoSQL%20Postgres%3A%20Add%20MongoDB%20compatibility%20to%20your%20Supabase%20projects%20with%20FerretDB)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fnosql-
mongodb-compatibility-with-ferretdb-and-
flydotio&t=NoSQL%20Postgres%3A%20Add%20MongoDB%20compatibility%20to%20your%20Supabase%20projects%20with%20FerretDB)

## Build in a weekend, scale to millions

[Start your project](https://supabase.com/dashboard)[Request a
demo](/contact/sales)

