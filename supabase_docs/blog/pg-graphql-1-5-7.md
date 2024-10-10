[Back](/blog)

[Blog](/blog)

# pg_graphql 1.5.7: pagination and multi-tenancy support

15 Aug 2024

•

4 minute read

[![Oliver Rice
avatar](/_next/image?url=https%3A%2F%2Fgithub.com%2Folirice.png&w=96&q=75)Oliver
RiceEngineering](https://github.com/olirice)

![pg_graphql 1.5.7: pagination and multi-tenancy
support](/_next/image?url=%2Fimages%2Fblog%2Flw12%2Fday-5%2Fthumb_pg_graphql.png&w=3840&q=100)

# What's new in pg_graphql 1.5.7#

Since our [last check-in on pg_graphql](/blog/whats-new-in-pg-graphql-v1-2)
there have been a few quality of life improvements worth calling out. A quick
roundup of the key differences includes:

  * Pagination via First/Offset
  * Schema based multi-tenancy
  * Filtering on array typed columns with `contains`, `containedBy` and `overlaps`

## First/Offset pagination#

Since the earliest days of pg_graphql, [keyset
pagination](https://supabase.github.io/pg_graphql/api/#keyset-pagination) has
been supported. Keyset pagination allows for paging forwards and backwards
through a collection by specifying a number of records and the unique id of a
record within the collection. For example:

`  

_10

{

_10

blogCollection(

_10

first: 2,

_10

after: "Y3Vyc29yMQ=="

_10

) {

_10

...

_10

}

  
`

to retrieve the first 2 records after the record with unique id `Y3Vyc29yMQ==`
.

Starting in version `1.5.0` there is support for `offset` based pagination,
which is based on skipping `offset` number of records before returning the
results.

`  

_10

{

_10

blogCollection(

_10

first: 2,

_10

offset: 5

_10

) {

_10

...

_10

}

  
`

That is roughly equivalent to the SQL

`  

_10

select

_10

*

_10

from

_10

blog

_10

limit

_10

2

_10

offset

_10

5

  
`

In general as offset values increase, the performance of the query will
decrease. For that reason its important to use keyset pagination where
possible.

## Performance schema based multi-tennancy#

pg_graphql caches the database schema on first query and rebuilds that cache
any time the schema changes. The cache key is a combination of the postgres
role and the database schema's version number. Initially, the structure of all
schemas was loaded for all roles, and table/column visibility was filtered
down within `pg_graphql`.

In multi-tenant environments with 1 schema per tenant, that meant every time a
tenant updated their schema, all tenants had to rebuild the cache. When the
number of tenants gets large, that burdens the database if its under heavy
load.

Following version `1.5.2` each tenant's cache only loads the schemas that they
have `usage` permission for, which greatly reduces the query time in multi-
tenant environments and the size of the schema cache. At time of writing this
solution powers a project with >2200 tenants.

## Filtering array column types#

From `1.5.6` pg_graphql has added `contains`, `containedBy`, `overlaps` filter
operators for scalar array fields like `text[]` or `int[]`.

For example, given a table

`  

_10

create table blog (

_10

id int primary key,

_10

name text not null,

_10

tags text[] not null,

_10

created_at timestamp not null

_10

);

  
`

the `tags` column with type `text[]` can be filtered on.

`  

_12

{

_12

blogCollection(filter: { tags: { contains: ["tech", "innovation"] } }) {

_12

edges {

_12

cursor

_12

node {

_12

name

_12

tags

_12

createdAt

_12

}

_12

}

_12

}

_12

}

  
`

In this case, the result set is filtered to records where the `tags` column
contains both `tech` and `innovation`.

## Roadmap#

The headline features we aim to launch in coming releases of pg_graphql
include support for:

  * Insert on conflict / Upsert
  * Nested inserts

If you want to get started with GraphQL today, check out the
[Docs](/docs/guides/graphql) or the [source
code](https://github.com/supabase/pg_graphql/).

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

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fpg-
graphql-1-5-7&text=pg_graphql%201.5.7%3A%20pagination%20and%20multi-
tenancy%20support)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fpg-
graphql-1-5-7&text=pg_graphql%201.5.7%3A%20pagination%20and%20multi-
tenancy%20support)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fpg-
graphql-1-5-7&t=pg_graphql%201.5.7%3A%20pagination%20and%20multi-
tenancy%20support)

[Last postIntroducing Log Drains15 August 2024](/blog/log-drains)

[Next postSnaplet is now open source14 August 2024](/blog/snaplet-is-now-open-
source)

[launch-week](/blog/tags/launch-week)[graphql](/blog/tags/graphql)

On this page

  * What's new in pg_graphql 1.5.7
    * First/Offset pagination
    * Performance schema based multi-tennancy
    * Filtering array column types
    * Roadmap

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fpg-
graphql-1-5-7&text=pg_graphql%201.5.7%3A%20pagination%20and%20multi-
tenancy%20support)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fpg-
graphql-1-5-7&text=pg_graphql%201.5.7%3A%20pagination%20and%20multi-
tenancy%20support)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fpg-
graphql-1-5-7&t=pg_graphql%201.5.7%3A%20pagination%20and%20multi-
tenancy%20support)

## Build in a weekend, scale to millions

[Start your project](https://supabase.com/dashboard)[Request a
demo](/contact/sales)

