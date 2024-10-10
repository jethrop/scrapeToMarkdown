[Back](/blog)

[Blog](/blog)

# vec2pg: Migrate to pgvector from Pinecone and Qdrant

16 Aug 2024

•

4 minute read

[![Oliver Rice
avatar](/_next/image?url=https%3A%2F%2Fgithub.com%2Folirice.png&w=96&q=75)Oliver
RiceEngineering](https://github.com/olirice)

![vec2pg: Migrate to pgvector from Pinecone and
Qdrant](/_next/image?url=%2Fimages%2Fblog%2Flw12%2Fday-5%2Fthumb_vec2pg.png&w=3840&q=100)

[vec2pg](https://github.com/supabase-community/vec2pg) is a CLI utility for
migrating data from vector databases to [Supabase](https://supabase.com/), or
any Postgres instance with [pgvector](https://github.com/pgvector/pgvector).

## Objective#

Our goal with <https://github.com/supabase-community/vec2pg> is to create an
easy on-ramp to efficiently copy your data from various vector databases into
Postgres with associated ids and metadata. The data loads into a new schema
with a table name that matches the source e.g. `vec2pg.<collection_name>` .
That output table uses <https://github.com/pgvector/pgvector's> `vector` type
for the embedding/vector and the builtin `json` type for additional metadata.

Once loaded, the data can be manipulated using SQL to transform it into your
preferred schema.

When migrating, be sure to increase your Supabase project's [disk
size](https://supabase.com/dashboard/project/_/settings/database) so there is
enough space for the vectors.

## Vendors#

At launch we support migrating to Postgres from
[Pinecone](https://www.pinecone.io/) and [Qdrant](https://qdrant.tech/). You
can vote for additional providers in the [issue
tracker](https://github.com/supabase-community/vec2pg/issues/6) and we'll
reference that when deciding which vendor to support next.

Throughput when migrating workloads is measured in records-per-second and is
dependent on a few factors:

  * the resources of the source data
  * the size of your Postgres instance
  * network speed
  * vector dimensionality
  * metadata size

When throughput is mentioned, we assume a
[Small](https://supabase.com/docs/guides/platform/compute-add-ons) Supabase
Instance, a 300 Mbps network, 1024 dimensional vectors, and reasonable
geographic colocation of the developer machine, the cloud hosted source DB,
and the Postgres instance.

### Pinecone#

vec2pg copies entire Pinecone indexes without the need to manage namespaces.
It will iterate through all namespaces in the specified index and has a column
for the namespace in its Postgres output table.

Given the conditions noted above, expect 700-1100 records per second.

### Qdrant#

The `qdrant` subcommand supports migrating from cloud and locally hosted
Qdrant instances.

Again, with the conditions mentioned above, Qdrant collections migrate at
between 900 and 2500 records per second.

## Why Use Postgres/pgvector?#

The main reasons to use Postgres for your vector workloads are the same
reasons you use Postgres for all of your other data. Postgres is performant,
scalable, and secure. Its a well understood technology with a wide ecosystem
of tools that support needs from early stage startups through to large scale
enterprise.

A few game changing capabilities that are old hat for Postgres that haven't
made their way to upstart vector DBs include:

### **Backups** #

Postgres has extensive supports for backups and point-in-time-recovery (PITR).
If your vectors are included in your Postgres instance you get backup and
restore functionality for free. Combining the data results in one fewer
systems to maintain. Moreover, your relational workload and your vector
workload are transactionally consistent with full referential integrity so you
never get dangling records.

### **Row Security** #

[Row Level Security
(RLS)](https://supabase.com/docs/guides/database/postgres/row-level-security)
allows you to write a SQL expression to determine which users are allowed to
insert/update/select individual rows.

For example

`  

_10

create policy "Individuals can view their own todos."

_10

on public.todos

_10

for select

_10

using

_10

( ( select auth.uid() ) = user_id );

  
`

Allows users of Supabase APIs to update their own records in the `todos`
table.

Since `vector` is just another column type in Postgres, you can write policies
to ensure e.g. each tenant in your application can only access their own
records. That security is enforced at the database level so you can be
confident each tenant only sees their own data without repeating that logic
all over API endpoint code or in your client application.

### **Performance** #

pgvector has world class performance in terms of raw throughput and dominates
in performance per dollar. Check out some of our prior blog posts for more
information on functionality and performance:

  * [**What's new in pgvector v0.7.0**](https://supabase.com/blog/pgvector-0-7-0)
  * [**pgvector 0.6.0: 30x faster with parallel index builds**](https://supabase.com/blog/pgvector-fast-builds)
  * [**Matryoshka embeddings: faster OpenAI vector search using Adaptive Retrieval**](https://supabase.com/blog/matryoshka-embeddings)

Keep an eye out for our upcoming post directly comparing pgvector with
Pinecone Serverless.

## Next Steps#

To get started, head over to the [vec2pg GitHub
Page](https://github.com/supabase-community/vec2pg), or if you're comfortable
with CLI help guides, you can install it using `pip` :

`  

_10

pip install vec2pg

  
`

If your current vector database vendor isn't supported, be sure to weigh in on
the [vendor support issue](https://github.com/supabase-
community/vec2pg/issues/6).

[Launch Week12](/launch-week)

12-16 August

[Day 1 -postgres.new: In-browser Postgres with an AI
interface](/blog/postgres-new)[Day 2 -Realtime Broadcast and Presence
Authorization](/blog/supabase-realtime-broadcast-and-presence-
authorization)[Day 3 -Supabase Auth: Bring-your-own Auth0, Cognito, or
Firebase](/blog/third-party-auth-mfa-phone-send-hooks)[Day 4 -Introducing Log
Drains](/blog/log-drains)[Day 5 -Postgres Foreign Data Wrappers with
Wasm](/blog/postgres-foreign-data-wrappers-with-wasm)

Build Stage

[01 -GitHub Copilot](/blog/github-copilot-extension-for-vs-code)[02
-pg_replicate](https://news.ycombinator.com/item?id=41209994)[03 -Snaplet is
now open source](/blog/snaplet-is-now-open-source)[04 -Supabase
Book](/blog/supabase-book-by-david-lorenz)[05
-PostgREST](/blog/postgrest-12-2)[06 -vec2pg](/blog/vec2pg)[07
-pg_graphql](/blog/pg-graphql-1-5-7)[08 -Platform Access
Control](/blog/platform-access-control)[09 -python-support](/blog/python-
support)[10 -Launch Week Summary](/blog/launch-week-12-top-10)[Community
Meetups](/launch-week#meetups)

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fvec2pg&text=vec2pg%3A%20Migrate%20to%20pgvector%20from%20Pinecone%20and%20Qdrant)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fvec2pg&text=vec2pg%3A%20Migrate%20to%20pgvector%20from%20Pinecone%20and%20Qdrant)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fvec2pg&t=vec2pg%3A%20Migrate%20to%20pgvector%20from%20Pinecone%20and%20Qdrant)

[Last postThe Supabase Book by David Lorenz16 August 2024](/blog/supabase-
book-by-david-lorenz)

[Next postIntroducing Log Drains15 August 2024](/blog/log-drains)

[launch-week](/blog/tags/launch-week)[release-notes](/blog/tags/release-
notes)[tech](/blog/tags/tech)[ai](/blog/tags/ai)

On this page

  * Objective
  * Vendors
    * Pinecone
    * Qdrant
  * Why Use Postgres/pgvector?
    * **Backups**
    * **Row Security**
    * **Performance**
  * Next Steps

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fvec2pg&text=vec2pg%3A%20Migrate%20to%20pgvector%20from%20Pinecone%20and%20Qdrant)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fvec2pg&text=vec2pg%3A%20Migrate%20to%20pgvector%20from%20Pinecone%20and%20Qdrant)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fvec2pg&t=vec2pg%3A%20Migrate%20to%20pgvector%20from%20Pinecone%20and%20Qdrant)

## Build in a weekend, scale to millions

[Start your project](https://supabase.com/dashboard)[Request a
demo](/contact/sales)

