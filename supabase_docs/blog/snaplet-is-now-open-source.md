[Back](/blog)

[Blog](/blog)

# Snaplet is now open source

14 Aug 2024

•

3 minute read

[![Paul Copplestone
avatar](/_next/image?url=https%3A%2F%2Fgithub.com%2Fkiwicopple.png&w=96&q=75)Paul
CopplestoneCEO and Co-Founder](https://github.com/kiwicopple)

![Snaplet is now open
source](/_next/image?url=%2Fimages%2Fblog%2Flw12%2Fday-3%2Fthumb-
snaplet.png&w=3840&q=100)

Startups are hard. One of our favorite startups, Snaplet, is [shutting
down](https://www.snaplet.dev/post/snaplet-is-shutting-down). Despite that,
they built an amazing team (some who now work at Supabase) and some incredible
products.

One way to ensure that your products out-live your business is to open source
what you've built. I'm a huge fan of what Snaplet built so I reached out to
[Peter](https://x.com/appfactory/) to see if Snaplet were interested in open
sourcing. He said yes:

> I built Snaplet because I believe developers write better software when they
> have access to production-like data. Although the company is closing, my
> belief remains strong, so we are open-sourcing the tools we've built.
>
> ![Peter Pistorius, Founder of Snaplet
> avatar](/_next/image?url=%2Fimages%2Fblog%2Favatars%2Fpeter-
> snaplet.webp&w=64&q=75)
>
> Peter Pistorius, Founder of Snaplet

## Open source products#

There are 3 main tools that they are releasing under the MIT license:

### Copycat#

Copycat generates fake data. It's like faker.js, but deterministic: for any
given input it'll always produce the same output. For example, if you generate
an email with the user ID `user_1234`, the next time you generate an email
with that email it will be the same, _guaranteed:_

  * Repo: [github.com/snaplet/copycat](https://github.com/snaplet/copycat)

### Snaplet Seed#

Seed generates realistic synthetic data based off a database schema. It
automatically determines the values in your database so you don't have to
define each value. For example, if you want to generate a 3 `comments` for one
of your `posts` you simply point it at your schema and let it handle the rest:

  * Repo: [github.com/snaplet/seed](https://github.com/snaplet/seed)
  * Docs: [docs.snaplet.dev/seed](https://snaplet-seed.netlify.app/seed)

### Snapshot#

Snapshot is for capturing, transforming, and restoring snapshots of your
database. It's like an advanced version of pg_dump/pg_restore. It has a
particularly neat feature called “subsetting”. Point it at a database table
and it tell it how much data you need. To maintain referential integrity,
subsetting traverses tables, selecting all the rows that are connected to the
target table through foreign key relationships:

  * Repo: [github.com/snaplet/snapshot](https://github.com/snaplet/snapshot)
  * Docs: [docs.snaplet.dev/snapshot](https://snaplet-snapshot.netlify.app/snapshot)

## The future of Snaplet tech#

The Snaplet team who joined Supabase have been helping Peter to migrate these
projects to open source. Over the next few weeks we'll move these into the
Supabase GitHub org and pick up the ongoing maintenance.

We prefer to keep products decoupled (it's one of our
[Principles](/docs/guides/getting-started/architecture#everything-works-in-
isolation)), so you'll always be able to use these tools independently from
Supabase. We can also see a lot of value providing a deep integration, so
we've already started adding their [Snaplet Seed](/docs/guides/cli/seeding-
your-database#generating-seed-data) to our official docs. This is just a
start, watch this space!

## Where's Peter now?#

Peter is back at [RedwoodJS](https://redwoodjs.com/), which he co-founded
before Snaplet. He's been working on React Server Components, coming soon to
Redwood.

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

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fsnaplet-
is-now-open-
source&text=Snaplet%20is%20now%20open%20source)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fsnaplet-
is-now-open-
source&text=Snaplet%20is%20now%20open%20source)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fsnaplet-
is-now-open-source&t=Snaplet%20is%20now%20open%20source)

[Last postpg_graphql 1.5.7: pagination and multi-tenancy support15 August
2024](/blog/pg-graphql-1-5-7)

[Next postSupabase Auth: Bring-your-own Auth0, Cognito, or Firebase14 August
2024](/blog/third-party-auth-mfa-phone-send-hooks)

[engineering](/blog/tags/engineering)

On this page

  * Open source products
    * Copycat
    * Snaplet Seed
    * Snapshot
  * The future of Snaplet tech
  * Where's Peter now?

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fsnaplet-
is-now-open-
source&text=Snaplet%20is%20now%20open%20source)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fsnaplet-
is-now-open-
source&text=Snaplet%20is%20now%20open%20source)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fsnaplet-
is-now-open-source&t=Snaplet%20is%20now%20open%20source)

## Build in a weekend, scale to millions

[Start your project](https://supabase.com/dashboard)[Request a
demo](/contact/sales)

