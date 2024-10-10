[Back](/blog)

[Blog](/blog)

# Oriole joins Supabase

15 Apr 2024

•

5 minute read

[![Paul Copplestone
avatar](/_next/image?url=https%3A%2F%2Fgithub.com%2Fkiwicopple.png&w=96&q=75)Paul
CopplestoneCEO and Co-Founder](https://github.com/kiwicopple)

![Oriole joins Supabase](/_next/image?url=%2Fimages%2Fblog%2Flaunch-
week-11%2Foriole%2Fthumb.png&w=3840&q=100)

[Oriole](https://github.com/orioledb/orioledb) is a **table storage extension
for Postgres**. It is designed to be a drop-in replacement for Postgres'
existing storage engine.

The Oriole team are joining Supabase to:

  1. Build a faster storage engine for Postgres.
  2. Help develop pluggable storage in Postgres.
  3. Work on decoupled storage and compute in Postgres.

Let's explore all of these below:

## Building a faster storage engine#

Oriole acts as a drop-in replacement for the default Postgres storage engine
using the Table Access Method APIs:

`  

_10

create extension orioledb; -- enable the extension

_10

_10

create table posts (

_10

id int8 not null,

_10

title text not null,

_10

body text not null,

_10

primary key (id)

_10

) using orioledb; -- Specify the storage format

  
`

The `using` clause might look familiar if you have used other storage engines
in Postgres like [Citus
columnar](https://docs.citusdata.com/en/v11.1/admin_guide/table_management.html#columnar-
storage), [Hydra](https://docs.hydra.so/concepts/using-hydra-columnar),
[ParadeDB](https://docs.paradedb.com/search/quickstart), or
[zheap](https://github.com/cybertec-postgresql/zheap). These all use the
[Table Access Method
API](https://www.postgresql.org/docs/current/tableam.html) \- a set of methods
that provide pluggable storage.

The `orioledb` storage engine changes the representation of table data on
disk. Its
[architecture](https://github.com/orioledb/orioledb/blob/main/doc/arch.md) is
designed to take advantage of modern hardware like SSDs and NVRAM.

It implements MVCC, the feature that allows multiple connected users to see
different versions of the data depending on when their transaction started,
via an UNDO log rather than tuple versioning. Orioles architecture prevents
bloat and provides several features and benefits:

  2. **Reduced IO** : It implements row-level WAL (Write-Ahead Log) and a non-persistent undo log. This significantly reduces IO operations for write transactions.
  3. **Scalability** : It implements lockless access for in-memory data. This helps to eliminate common bottlenecks found in traditional database engines.
  4. **Data Compression** : It implements page-level data compression, which can reduce the overall size of a typical database by approximately 4 to 5 times, saving storage space.
  5. **Bloat Reduction** : Efficiently manages updates in-place with an undo log, which contributes to reducing database bloat — a common issue where the database size grows due to unused or obsolete data occupying space.
  6. **Index-organized tables:** Oriole stores table rows in the leafs of primary key index making primary key lookups very cheap. In many cases, this saves significant storage space.

Reads and writes are significantly faster with Oriole

## Pluggable storage in Postgres#

We've [written previously](https://supabase.com/blog/postgres-pluggable-
strorage) about Pluggable Storage: it gives developers the ability to use
different storage engines for different tables _within the same database_.
This system is [available in
MySQL](https://en.wikipedia.org/wiki/Comparison_of_MySQL_database_engines),
which uses the [InnoDB](https://en.wikipedia.org/wiki/InnoDB) as the default
storage engine since MySQL 5.5 (replacing
[MyISAM](https://en.wikipedia.org/wiki/MyISAM)).

Oriole aims to be a drop-in replacement for Postgres' default storage engine
and supports similar use-cases with improved performance. Other storage
engines, to name a few possibilities, could implement columnar storage for
OLAP workloads, highly compressed timeseries storage for event data, or
compressed storage for minimizing disk usage.

In version 12, PostgreSQL introduced support for pluggable storage with the
goal of [adding ZHeap](https://anarazel.de/talks/2019-05-30-pgcon-pluggable-
table-storage/pluggable.pdf) \- a previous effort to solve some shortcomings
of Postgres' default storage format. We hope to contribute towards these
efforts.

OrioleDB currently requires a [set of patches to
Postgres](https://github.com/orioledb/postgres/commits/patches16/) to expand
on the type of features external storage engines extensions can implement. We
remain committed to open source we'll work with the Oriole team and Postgres
community with the goal of upstreaming patches so that Oriole can be used with
any Postgres installation. We have no timeline for this, but it's safe to
expect that it could be a few major Postgres versions away.

## Decoupled Storage and Compute#

The Oriole storage engine's reduction in disk IO is significant enough that it
unlocks performant databases backed by S3 compatible blob storage.

We've been working with the Oriole team for a few months to develop
[experimental support decoupled storage and
compute](https://github.com/orioledb/orioledb/blob/main/doc/usage.md#s3-database-
storage-experimental):

Local storage implements caching of the data most often accessed, ensuring
good performance, and then synced with S3 asynchronously.

You can connect an empty Postgres instance to an s3 bucket (using an [S3
loader
utility](https://github.com/orioledb/orioledb/blob/main/doc/usage.md#s3-loader-
utility)). The Oriole roadmap includes the ability to connect multiple read-
replicas to the same S3 bucket as leader.

## Oriole + Supabase#

[Portability](https://supabase.com/docs/guides/getting-
started/architecture#everything-is-portable) is a core principle at Supabase.
Because Oriole requires a few minimal patch sets on top of Postgres, we will
roll it out as an _option_ for developers in the future. Over time we hope
that it can become available for any Postgres installation and we will
continue to work with Oriole and the Postgres community to make this happen.

[![GA logo](/_next/image?url=%2Fimages%2Flaunchweek%2Fga%2Fga-
black.svg&w=64&q=75)![GA
logo](/_next/image?url=%2Fimages%2Flaunchweek%2Fga%2Fga-
white.svg&w=64&q=75)Week](/ga-week)

15-19 April

[Day 1 -Supabase is officially launching into General Availability](/ga)[Day 2
-Supabase Functions now supports AI models](/blog/ai-inference-now-available-
in-supabase-edge-functions)[Day 3 -Supabase Auth now supports Anonymous sign-
ins](/blog/anonymous-sign-ins)[Day 4 -Supabase Storage: now supports the S3
protocol](/blog/s3-compatible-storage)[Day 5 -Supabase Security Advisor &
Performance Advisor](/blog/security-performance-advisor)

Build Stage

[01 -PostgreSQL Index Advisor](https://github.com/supabase/index_advisor)[02
-Branching now Publicly Available](/blog/branching-publicly-available)[03
-Oriole joins Supabase](/blog/supabase-acquires-oriole)[04 -Supabase on AWS
Marketplace](/blog/supabase-aws-marketplace)[05 -Supabase
Bootstrap](/blog/supabase-bootstrap)[06 -Supabase Swift](/blog/supabase-
swift)[07 -Top 10 Launches from Supabase GA Week](/blog/ga-week-summary)[Open
Source Hackathon 2024](/blog/supabase-oss-hackathon)[Community Meetups](/ga-
week#meetups)

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fsupabase-
acquires-
oriole&text=Oriole%20joins%20Supabase)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fsupabase-
acquires-
oriole&text=Oriole%20joins%20Supabase)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fsupabase-
acquires-oriole&t=Oriole%20joins%20Supabase)

[Last postBranching now Publicly Available15 April 2024](/blog/branching-
publicly-available)

[Next postSupabase on the AWS Marketplace15 April 2024](/blog/supabase-aws-
marketplace)

[launch-week](/blog/tags/launch-week)[database](/blog/tags/database)

On this page

  * Building a faster storage engine
  * Pluggable storage in Postgres
  * Decoupled Storage and Compute
  * Oriole + Supabase

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fsupabase-
acquires-
oriole&text=Oriole%20joins%20Supabase)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fsupabase-
acquires-
oriole&text=Oriole%20joins%20Supabase)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fsupabase-
acquires-oriole&t=Oriole%20joins%20Supabase)

## Build in a weekend, scale to millions

[Start your project](https://supabase.com/dashboard)[Request a
demo](/contact/sales)

