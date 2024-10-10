[Back](/blog)

[Blog](/blog)

# PostgREST 12.2: Prometheus metrics

16 Aug 2024

•

2 minute read

[![Steve Chavez avatar](/_next/image?url=https%3A%2F%2Fgithub.com%2Fsteve-
chavez.png&w=96&q=75)Steve ChavezEngineering & PostgREST
maintainer](https://github.com/steve-chavez)

![PostgREST 12.2: Prometheus
metrics](/_next/image?url=%2Fimages%2Fblog%2Flw12%2Fday-5%2Fthumb_postgREST.png&w=3840&q=100)

[PostgREST 12.2](https://github.com/PostgREST/postgrest/releases/tag/v12.2.0)
is out! It comes with Observability and API improvements. In this post, we'll
see what's new.

## Prometheus Metrics#

Version 12.2 ships with Prometheus-compatible metrics for PostgREST's schema
cache and connection pool. These are useful for troubleshooting, for example,
when PostgREST's pool is starved for connections.

`  

_10

curl localhost:3001/metrics

_10

_10

# HELP pgrst_db_pool_timeouts_total The total number of pool connection
timeouts

_10

# TYPE pgrst_db_pool_timeouts_total counter

_10

pgrst_db_pool_timeouts_total 7.0

_10

_10

# ....

  
`

A full list of supported metrics is available in the [PostgREST
documentation](https://postgrest.org/en/latest/references/observability.html#metrics).

## Hoisted Function Settings#

Sometimes it's handy to set a custom timeout per function. You can now do this
on 12.2 projects with:

`  

_10

create or replace function special_function()

_10

returns void as $$

_10

select pg_sleep(3); -- simulating some long-running process

_10

$$

_10

language sql

_10

set statement_timeout to '4s';

  
`

And calling the function with the [RPC
interface](https://supabase.com/docs/reference/javascript/rpc).

When doing `set statement_timeout`on the function, the `statement_timeout`
will be “hoisted” and applied per transaction.

By default this also works for other settings, namely
`plan_filter.statement_cost_limit` and `default_transaction_isolation`. The
list of hoisted settings can be extended by modifying the [db-hoisted-tx-
settings](https://postgrest.org/en/latest/references/configuration.html#db-
hoisted-tx-settings) configuration.

Before 12.2, this could be done by setting a `statement_timeout` on the API
roles, but this affected all the SQL statements executed by those roles.

## Max Affected#

In prior versions of PostgREST, users could limit the number of records
impacted by mutations (insert/update/delete) to 1 row using vendor media type
`application/vnd.pgrst.object+json`. That supports a common use case but is
not flexible enough to support user defined values.

12.2 introduces the `max-affected` preference to limit the affected rows up to
a custom value.

For example:

`  

_10

curl -i "http://localhost:3000/items?id=lt.15" -X DELETE \

_10

-H "Content-Type: application/json" \

_10

-H "Prefer: handling=strict, max-affected=10"

  
`

If the number of affected records exceeds `max-affected` , an error is
returned:

`  

_10

HTTP/1.1 400 Bad Request

_10

{

_10

"code": "PGRST124",

_10

"message": "Query result exceeds max-affected preference constraint",

_10

"details": "The query affects 14 rows",

_10

"hint": null

_10

}

  
`

## **Try it out** #

PostgREST v12.2 is already available on the Supabase platform on its latest
patch version
([v12.2.3](https://github.com/PostgREST/postgrest/releases/tag/v12.2.3)) for
new projects. Spin up a new project or upgrade your existing project to try it
out!

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

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fpostgrest-12-2&text=PostgREST%2012.2%3A%20Prometheus%20metrics)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fpostgrest-12-2&text=PostgREST%2012.2%3A%20Prometheus%20metrics)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fpostgrest-12-2&t=PostgREST%2012.2%3A%20Prometheus%20metrics)

[Last postPostgres Foreign Data Wrappers with Wasm16 August
2024](/blog/postgres-foreign-data-wrappers-with-wasm)

[Next postSupabase Python16 August 2024](/blog/python-support)

[launch-week](/blog/tags/launch-week)[release-notes](/blog/tags/release-
notes)[tech](/blog/tags/tech)

On this page

  * Prometheus Metrics
  * Hoisted Function Settings
  * Max Affected
  * **Try it out**

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fpostgrest-12-2&text=PostgREST%2012.2%3A%20Prometheus%20metrics)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fpostgrest-12-2&text=PostgREST%2012.2%3A%20Prometheus%20metrics)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fpostgrest-12-2&t=PostgREST%2012.2%3A%20Prometheus%20metrics)

## Build in a weekend, scale to millions

[Start your project](https://supabase.com/dashboard)[Request a
demo](/contact/sales)

