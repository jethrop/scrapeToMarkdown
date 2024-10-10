[Back](/blog)

[Blog](/blog)

# Branching now Publicly Available

15 Apr 2024

•

3 minute read

[![Alaister Young
avatar](/_next/image?url=https%3A%2F%2Fgithub.com%2Falaister.png&w=96&q=75)Alaister
YoungEngineering](https://github.com/alaister)

[![Qiao Han
avatar](/_next/image?url=https%3A%2F%2Fgithub.com%2Fsweatybridge.png&w=96&q=75)Qiao
HanEngineering](https://github.com/sweatybridge)

![Branching now Publicly Available](/_next/image?url=%2Fimages%2Fblog%2Fga-
week%2Fbranching-publicly-available%2Fthumb.png&w=3840&q=100)

tl;dr: Supabase Branching is now in open beta! You can enable it on any
project that's Pro Plan or above.

## What is Branching?#

Branching is a seamless integration of Git with your development workflow,
extending beyond your local environment to a remote database. Leveraging Git,
particularly focusing on GitHub initially, each time a Pull Request is opened,
a corresponding "Preview Environment" is spawned.

Preview Branches are essentially full Supabase instances. Every push triggers
migrations from the `./supabase/migrations` folder, ensuring team
synchronization and a shared source of truth. When you merge a Pull Request,
your migrations are applied to the Production database.

We [announced Branching](https://supabase.com/blog/supabase-branching) a few
months ago in our previous Launch Week, with a deep dive on a few of the
features like data seeding, integrations with Vercel, and seamless handling of
environment variables. Since launching Branching for early-access we've worked
with early users of all sizes. Today we're making Branching available to
everyone.

## New Features#

Our open Beta introduces a number of requested features:

### Edge Function support#

Branching now deploys your Edge Functions along with your migrations. Any
Functions added or changed in your `./supabase/functions` will automatically
be deployed without any extra configuration.

### Monorepo support#

You can now set a custom Supabase directory path which allows for monorepo
support. You can also choose to only spin up new branches when there are
changes inside your Supabase directory. See all the configuration settings in
your projects
[here](https://supabase.com/dashboard/project/_/settings/integrations).

### Persistent branches#

We had quite a few users of branching request for long-running branches so we
added the concept of persistent branches. In persistent mode, a branch will
remain active even after the underlying PR merges or closes.

Please note that branches should still be treated as replaceable at any time.
Persistent or ephemeral Branches should not be used for production data.

## Feedback#

A special thank you to all our early-access branching users who provided lots
of actionable feedback. Our feature development was largely driven by the
direct feedback from our users.

We still have many features to add to branching before 1.0, so please continue
[sending us your
feedback](https://github.com/orgs/supabase/discussions/18937)!

## Getting Started#

You can easily get started with Branching by following our [Getting Started
Guide](https://supabase.com/docs/guides/platform/branching#how-to-use-
supabase-branching).

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

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fbranching-
publicly-
available&text=Branching%20now%20Publicly%20Available)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fbranching-
publicly-
available&text=Branching%20now%20Publicly%20Available)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fbranching-
publicly-available&t=Branching%20now%20Publicly%20Available)

[Last postAI Inference now available in Supabase Edge Functions16 April
2024](/blog/ai-inference-now-available-in-supabase-edge-functions)

[Next postOriole joins Supabase15 April 2024](/blog/supabase-acquires-oriole)

[launch-week](/blog/tags/launch-week)[database](/blog/tags/database)

On this page

  * What is Branching?
  * New Features
    * Edge Function support
    * Monorepo support
    * Persistent branches
  * Feedback
  * Getting Started

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fbranching-
publicly-
available&text=Branching%20now%20Publicly%20Available)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fbranching-
publicly-
available&text=Branching%20now%20Publicly%20Available)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fbranching-
publicly-available&t=Branching%20now%20Publicly%20Available)

## Build in a weekend, scale to millions

[Start your project](https://supabase.com/dashboard)[Request a
demo](/contact/sales)

