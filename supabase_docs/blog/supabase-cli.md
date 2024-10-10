[Back](/blog)

[Blog](/blog)

# Supabase CLI

31 Mar 2021

•

8 minute read

[![Bobbie Soedirgo
avatar](/_next/image?url=https%3A%2F%2Fgithub.com%2Fsoedirgo.png&w=96&q=75)Bobbie
SoedirgoEngineering](https://github.com/soedirgo)

![Supabase CLI](/_next/image?url=%2Fimages%2Fblog%2Fcli%2Fcli-
og.jpg&w=3840&q=100)

**UPDATE 15/08/2022:** [Supabase CLI V1 is Generally
Available](/blog/supabase-cli-v1-and-admin-api-beta) and we also released a
Management API (in beta).

Today is Day 3 of [Launch Week](/blog/launch-week), and as promised - we're
releasing our CLI.

This is the first step in a long journey of features we plan to deliver:

  * Running Supabase locally
  * Managing database migrations
  * Generating types directly from your database schema
  * Generating API and validation schemas from your database
  * Managing your Supabase projects
  * Pushing your local changes to production

Here are some of the items we have completed so far.

## Running Supabase Locally#

You can now run Supabase on your local machine, using Docker Compose. This
Docker setup is 100% compatible with every project on Supabase - the tools
used for local development are exactly the same as production.

We have released a full set of documentation [here](/docs/guides/local-
development). In this post we thought it would be useful to highlight how easy
it is to get started.

A lot of Supabase developers are familiar with React, so here are the steps
you would use to create a new React project which uses Supabase as a backend.

Install the CLI:

`  

_10

npm install -g supabase

  
`

Set up your React app:

`  

_10

# create a fresh React app

_10

npx create-react-app react-demo --use-npm

_10

_10

# move into the new folder

_10

cd react-demo

_10

_10

# Save the install supabase-js library

_10

npm install --save @supabase/supabase-js

  
`

Set up Supabase:

`  

_10

supabase init

_10

_10

# ✔ Port for Supabase URL: · 8000

_10

# ✔ Port for PostgreSQL database: · 5432

_10

# ✔ Project initialized.

_10

# Supabase URL: http://localhost:8000

_10

# Supabase Key (anon, public):
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJzdXBhYmFzZSIsImlhdCI6MTYwMzk2ODgzNCwiZXhwIjoyNTUwNjUzNjM0LCJyb2xlIjoiYW5vbiJ9.36fUebxgx1mcBo4s19v0SzqmzunP
--hm_hep0uLX0ew

_10

# Supabase Key (service_role, private):
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJzdXBhYmFzZSIsImlhdCI6MTYwMzk2ODgzNCwiZXhwIjoyNTUwNjUzNjM0LCJyb2xlIjoiYW5vbiJ9.36fUebxgx1mcBo4s19v0SzqmzunP
--hm_hep0uLX0ew

_10

# Database URL: postgres://postgres:postgres@localhost:5432/postgres

  
`

Now that your application is now prepared, you can use Supabase anywhere in
your application (for example, `App.js`):

`  

_10

import { createClient } from '@supabase/supabase-js'

_10

const SUPABASE_URL = 'http://localhost:8000'

_10

const SUPABASE_ANON_KEY =

_10

'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJzdXBhYmFzZSIsImlhdCI6MTYwMzk2ODgzNCwiZXhwIjoyNTUwNjUzNjM0LCJyb2xlIjoiYW5vbiJ9.36fUebxgx1mcBo4s19v0SzqmzunP
--hm_hep0uLX0ew'

_10

const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY)

  
`

Then start the backend and the frontend:

`  

_10

supabase start # Start Supabase

_10

npm start # Start the React app

  
`

If everything is working you should have a React app running on
`http://localhost:3000` and Supabase services running on
`http://localhost:8000`!

### Next steps:#

Soon we will give you the ability to push your changes from your local machine
to your Production project. How will we do that? Migrations!

## Migrations#

Database Migrations are a process to "change" your database schema. In a NoSQL
database you don't need migrations, because you can insert any JSON data
without validation. However with Relational databases you define your schema
upfront, and the database will reject data which doesn't "fit" the schema.
This is one of the reasons Relational databases are so scalable - schemas
ensure data integrity.

Just like an application though, a database schema needs to be constantly
updated. And that's where migrations fit! Migrations are simply a set of SQL
scripts which change your database schema.

There is one problem however: there is [no "right"
way](https://news.ycombinator.com/item?id=21405501) to do migrations.

### Diffs#

At Supabase, we do have one strong preference. We like schema "diffing" over
"manual migrations".

Manual migrations work like this:

  * A developer thinks about all the changes they want to make to their database
  * They create a SQL script which will cause those changes
  * They run that script on their database

After a while though, these scripts pile up - the `migrations` folder can
contain hundreds of migration scripts. This method is also "version control"
on top of another version control system (i.e. git).

A "diff" tool works like this:

  * a developer makes all the changes they desire to a local database
  * they use a tool to compare their local database to the production database
  * the tool then generates all the SQL scripts that are required, and runs them on the target database

In this case, the tool does all the hard work. This is obviously an ideal
state. Databases schemas are declarative, and when you check them into git,
you can see their evolution over time. The hard part is finding a tool which
can handle all the edge-cases of database diff'ing.

### Choosing the best diff tool#

After evaluating these OSS tools:

  * [migra](https://github.com/djrobstep/migra) (Python)
  * [dbdiff](https://github.com/gimenete/dbdiff) (JS)
  * [pgdiff](https://github.com/joncrlsn/pgdiff) (Go)
  * [apgdiff](https://github.com/fordfrog/apgdiff) (Java)
  * [pgquarrel](https://github.com/eulerto/pgquarrel) (C)
  * [pgAdmin Schema Diff](https://www.pgadmin.org/docs/pgadmin4/development/schema_diff.html) (Python)

We found that the most complete one was the pgAdmin Schema Diff, migra came a
close second.

The deciding factor was if the tool could track an owner change for a VIEW.

`  

_10

ALTER VIEW my_view OWNER TO authenticated;

  
`

This is critical for Row Level Security to work with views. For policies to
kick in on views, the owner must not have `superuser` or `bypassrls`
privileges. Currently migra doesn't track this change
([issue](https://github.com/djrobstep/migra/issues/160)), while the pgAdmin
Schema Diff does.

There was a problem in using the [pgAdmin Schema
Diff](https://www.pgadmin.org/docs/pgadmin4/development/schema_diff.html)
though, it's a GUI-only tool.

So we did what we always strive to do - improve existing open source software.
We created a CLI mode for the Schema Diff on [our
repo](https://github.com/supabase/pgadmin4/blob/cli/web/cli.py). We've also
released a [docker image](https://hub.docker.com/r/supabase/pgadmin-schema-
diff) for a quick start.

The CLI offers the same functionality as the GUI version. You can diff two
databases by specifying the connection strings like shown below.

`  

_24

docker run supabase/pgadmin-schema-diff \

_24

'postgres://user:pass@local:5432/diff_source' \

_24

'postgres://user:pass@production:5432/diff_target' \

_24

> diff_demo.sql

_24

_24

Starting schema diff...

_24

Comparison started......0%

_24

Comparing Event Triggers...2%

_24

Comparing Extensions...4%

_24

Comparing Languages...8%

_24

Comparing Foreign Servers...14%

_24

Comparing Foreign Tables of schema 'public'...28%

_24

Comparing Tables of schema 'public'...50%

_24

Comparing Domains of schema 'test_schema_diff'...66%

_24

Comparing Foreign Tables of schema 'test_schema_diff'...68%

_24

Comparing FTS Templates of schema 'test_schema_diff'...76%

_24

Comparing Functions of schema 'test_schema_diff'...78%

_24

Comparing Procedures of schema 'test_schema_diff'...80%

_24

Comparing Tables of schema 'test_schema_diff'...90%

_24

Comparing Types of schema 'test_schema_diff'...92%

_24

Comparing Materialized Views of schema 'test_schema_diff'...96%

_24

Done.

_24

_24

## the diff is written to diff_demo.sql

  
`

A sample diff can be seen on this [gist](https://gist.github.com/steve-
chavez/3f286a233806aeee0bcea4a47f97f0b5). This was generated by diffing these
[two
databases](https://github.com/supabase/pgadmin4/tree/cli/web/pgadmin/tools/schema_diff/tests/pg/10_plus).

On these [lines](https://gist.github.com/steve-
chavez/3f286a233806aeee0bcea4a47f97f0b5#file-diff_demo-sql-L1022-L1023), you
can see how it tracks the view's owner change (note: the `ALTER TABLE`
statement is interchangeable with `ALTER VIEW` in this case). Additionally,
you can see that it handles [domains](https://gist.github.com/steve-
chavez/3f286a233806aeee0bcea4a47f97f0b5#file-diff_demo-sql-L278-L287) just
fine, this is an edge-case that other diff tools don't handle.

Also, similarly to the pgAdmin GUI:

  * You can include and exclude database objects from the diff with `--include-objects` or `--exclude-objects`
  * You can choose a single schema to diff with the `--schema` argument or you can pick different schemas to compare with the --source-schema and --target-schema arguments. We recommend you do this for Supabase databases. Diffing the whole database can take a while because of the `extensions` schema (especially if you enable PostGIS, which adds many functions).

### Next steps#

Once we have added logins to the CLI, we will be able to use Migrations to
create a seamless workflow between local development and your production
database.

Also, the pgAdmin team has showed
[interest](https://www.postgresql.org/message-id/CA%2BOCxoyjZhV9stFMAQ-
QhHuA0%2BdLQD5XD_YT%2BQo2vY0GhkBKFw%40mail.gmail.com) in including our Schema
Diff CLI in the official pgAdmin. We'll be working with them to include this
change upstream to benefit the whole community.

## Self Hosting#

Finally, we are adding one critical command to our CLI for everybody who wants
to self-host:

`  

_10

supabase eject

  
`

This gives you everything you need to run the Supabase stack.

After running the command inside the terminal, you will see three items:

  * `docker-compose.yml` (file)
  * `kong` (directory)
  * `postgres` (directory)

If you have an existing Postgres database running elsewhere you can easily
drop the Postgres directory but first make sure you do these three things:

  * run the .sql files from the Postgres directory on your existing database
  * update all references to the DB URI in `docker-compose.yml` to your existing database
  * run [these steps](https://github.com/supabase/realtime#server) to enable replication inside the database, so that the realtime engine can stream changes from your database

You may also want to play with the environment variables for each application
inside `docker-compose.yml`.
[PostgREST](https://postgrest.org/en/v7.0.0/configuration.html) has many
additional configuration options, as does
[GoTrue](https://github.com/supabase/gotrue#configuration). In the hosted
version of Supabase we connect our own SMTP service to GoTrue for sending auth
emails, so you may also want to add these settings here in order to enable
this.

Also check `kong.yml` inside the `kong` directory where you'll see how all the
services are routed to, and with what rules, down the bottom you'll find the
JWTs capable of accessing services that require API Key access.

Once you're all set, you can start the stack by running:

`  

_10

docker compose up

  
`

Head over to the [Self Hosting Docs](/docs/guides/self-hosting) for a more
complete walk through, it also includes several [one-click
deploys](/docs/guides/self-hosting#one-click-deploys), so you can easily
deploy into your own cloud hosting provider.

If you require any assistance feel free to reach out in our [github
discussions](https://github.com/supabase/supabase/discussions) or at [[email
protected]](/cdn-cgi/l/email-
protection#3b484e4b4b54494f7b484e4b5a595a485e155254).

Check out the CLI VI [launched Monday 15th August, 2022](/blog/supabase-
cli-v1-and-admin-api-beta), contribute to the [CLI
repo](https://github.com/supabase/cli), or go here for the [hosted
version](https://supabase.com/dashboard).

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fsupabase-
cli&text=Supabase%20CLI)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fsupabase-
cli&text=Supabase%20CLI)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fsupabase-
cli&t=Supabase%20CLI)

[Last postSupabase Launches NFT Marketplace1 April 2021](/blog/supabase-nft-
marketplace)

[Next postStorage is now available in Supabase30 March 2021](/blog/supabase-
storage)

[supabase](/blog/tags/supabase)[storage](/blog/tags/storage)

On this page

  * Running Supabase Locally
  * Migrations
  * Self Hosting

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fsupabase-
cli&text=Supabase%20CLI)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fsupabase-
cli&text=Supabase%20CLI)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fsupabase-
cli&t=Supabase%20CLI)

## Build in a weekend, scale to millions

[Start your project](https://supabase.com/dashboard)[Request a
demo](/contact/sales)

