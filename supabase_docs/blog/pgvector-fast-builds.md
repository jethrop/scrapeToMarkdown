[Back](/blog)

[Blog](/blog)

# pgvector 0.6.0: 30x faster with parallel index builds

30 Jan 2024

•

14 minute read

[![Egor Romanov avatar](/_next/image?url=https%3A%2F%2Fgithub.com%2Fegor-
romanov.png&w=96&q=75)Egor RomanovEngineering](https://github.com/egor-
romanov)

![pgvector 0.6.0: 30x faster with parallel index
builds](/_next/image?url=%2Fimages%2Fblog%2F2024-01-30-pgvector-fast-
builds%2Fpgvector6.png&w=3840&q=100)

pgvector 0.6.0 was released today, with a significant improvement: parallel
builds for HNSW indexes. Building an HNSW index is now up to 30x faster for
unlogged tables.

This release is a huge step forward for pgvector, making it easier to tune
HNSW build parameters and increase search accuracy and performance.

## HNSW indexes in pgvector#

We explored [how HNSW works](https://supabase.com/blog/increase-performance-
pgvector-hnsw#how-does-hnsw-work) in an earlier post, so as a quick recap:
HNSW is an algorithm for approximate nearest neighbor search. It uses
proximity graphs and consists of two parts: hierarchical and navigatable small
world. It operates over multiple layers with different densities or distances
between nodes, where layers represent different connection lengths between
nodes. Thus allowing HNSW to search, insert, and delete in linearithmic time.

## pgvector parallel index builds#

Prior to 0.6.0, pgvector only supported building indexes using a single thread
- a big bottleneck for large datasets. For example, building an index for 1
million vectors of 1536 dimensions would take around 1 hour and 27 minutes
(with `'m'=16, 'ef_construction'=200`).

With parallel index builds you can build an index for the same dataset in 9.5
minutes - 9 times faster:

## Performance comparison: pgvector 0.5 vs 0.6#

We tested index build time with the [dbpedia-entities-
openai-1M](https://huggingface.co/datasets/KShivendu/dbpedia-entities-
openai-1M) dataset (1 million vectors, 1536 dimensions) to compare the
performance of parallel and single-threaded index HNSW builds. At the same
time, we verified that the resulting indexes are the same in terms of accuracy
and queries per second (QPS).

We ran benchmarks on various database sizes to see the impact of parallel
builds:

  * 4XL instance (16 cores 64GB RAM)
  * 16XL instance (64 cores 256GB RAM)

### 4XL instance (16 cores 64GB RAM)#

This benchmark used the following parameters:

| 0.5.1| 0.6.0  
---|---|---  
mainenance_work_mem| 30GB| 30GB  
max_parallel_maintenance_workers| -| 15  
  
`max_parallel_maintenance_workers` controls how many parallel threads are used
to build an index. In further sections we will refer to the total number of
workers, including the leader.

Results

The index build time is 7-9 times faster for 0.6.0, while queries per second
and accuracy stay the same for both versions:

  * `v0.5.1`: averaged 938 QPS and 0.963 accuracy across all benchmarks.
  * `v0.6.0`: averaged 950 QPS and 0.963 accuracy across all benchmarks.

### 16XL instance (64 cores 256GB RAM)#

You can further improve index build performance using a more powerful instance
(up to 13.5x for these parameters).

Results

The index build time is not linearly proportional to the number of cores used.
A sensible default for `max_parallel_maintenance_workers` is `CPU count / 2` ,
the default we set on the Supabase platform. Accuracy and QPS are not affected
by `max_parallel_maintenance_workers`.

##### Pro tip: optimizing your bills

The trick is to use a large database while you build the index and then switch
back to a cheaper instance after the index is built.

### Embeddings with unlogged tables#

Building time can be reduced _even further_ using unlogged tables.

An unlogged table in Postgres is a table whose modifications are not recorded
in the write-ahead log (trading performance for data reliability). Unlogged
tables are a great option for embeddings because the raw data is often stored
separately and the embeddings can be recreated from the source data at any
time.

One of the steps of index creation is the final scan and WAL writing. This is
generally short but not parallelizable. Using unlogged tables allows you to
skip the WAL, with an impressive impact:

ef_construction| Build time: v0.5.1| Build time: v0.6.0 (unlogged)|
Improvement  
---|---|---|---  
64| 38m 08s| 1m 38s| 23x  
100| 1h 06m 59s| 2m 10s| 31x  
200| 1h 27m 45s| 3m 37s| 24x  
  
## Getting started#

pgvector 0.6.0 was [just
released](https://github.com/pgvector/pgvector/releases/tag/v0.6.0) and will
be available on Supabase projects soon. Again, a special shout out to Andrew
Kane and everyone else who [worked on parallel index
builds](https://github.com/pgvector/pgvector/issues/409).

## More pgvector and AI resources#

  * [pgvector v0.5.0: Faster semantic search with HNSW indexes](https://supabase.com/blog/increase-performance-pgvector-hnsw)
  * [How to build ChatGPT Plugin from scratch with Supabase Edge Runtime](https://supabase.com/blog/building-chatgpt-plugins-template)
  * [Docs pgvector: Embeddings and vector similarity](https://supabase.com/docs/guides/database/extensions/pgvector)
  * [Choosing Compute Add-on for AI workloads](https://supabase.com/docs/guides/ai/choosing-compute-addon)
  * [pgvector: Fewer dimensions are better](https://supabase.com/blog/fewer-dimensions-are-better-pgvector)

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fpgvector-
fast-
builds&text=pgvector%200.6.0%3A%2030x%20faster%20with%20parallel%20index%20builds)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fpgvector-
fast-
builds&text=pgvector%200.6.0%3A%2030x%20faster%20with%20parallel%20index%20builds)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fpgvector-
fast-
builds&t=pgvector%200.6.0%3A%2030x%20faster%20with%20parallel%20index%20builds)

[Last postNoSQL Postgres: Add MongoDB compatibility to your Supabase projects
with FerretDB31 January 2024](/blog/nosql-mongodb-compatibility-with-ferretdb-
and-flydotio)

[Next postGetting started with Ruby on Rails and Postgres on Supabase29
January 2024](/blog/ruby-on-rails-postgres)

[AI](/blog/tags/AI)[performance](/blog/tags/performance)[postgres](/blog/tags/postgres)

On this page

  * HNSW indexes in pgvector
  * pgvector parallel index builds
  * Performance comparison: pgvector 0.5 vs 0.6
    * 4XL instance (16 cores 64GB RAM)
    * 16XL instance (64 cores 256GB RAM)
    * Embeddings with unlogged tables
  * Getting started
  * More pgvector and AI resources

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fpgvector-
fast-
builds&text=pgvector%200.6.0%3A%2030x%20faster%20with%20parallel%20index%20builds)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fpgvector-
fast-
builds&text=pgvector%200.6.0%3A%2030x%20faster%20with%20parallel%20index%20builds)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fpgvector-
fast-
builds&t=pgvector%200.6.0%3A%2030x%20faster%20with%20parallel%20index%20builds)

## Build in a weekend, scale to millions

[Start your project](https://supabase.com/dashboard)[Request a
demo](/contact/sales)

