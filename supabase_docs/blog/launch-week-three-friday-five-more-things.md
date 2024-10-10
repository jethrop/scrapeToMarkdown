[Back](/blog)

[Blog](/blog)

# Five more things

03 Dec 2021

•

5 minute read

[![Ant Wilson
avatar](/_next/image?url=https%3A%2F%2Fgithub.com%2Fawalias.png&w=96&q=75)Ant
WilsonCTO and Co-Founder](https://github.com/awalias)

![Five more things](/_next/image?url=%2Fimages%2Fblog%2Flaunch-week-
three%2Ffive-more-things%2Ffive-more-things-thumb.png&w=3840&q=100)

## Open source GraphQL PostgreSQL Extension#

Today we're open sourcing
[pg_graphql](https://github.com/supabase/pg_graphql), a work-in-progress
native PostgreSQL extension adding GraphQL support. The extension keeps schema
generation, query parsing, and resolvers all neatly contained on your database
server requiring no external services.

`pg_graphql` inspects an existing PostgreSQL schema and reflects a GraphQL
schema with resolvers that are:

  * performant
  * always up-to-date
  * compliant with best practices
  * serverless
  * open source

Interested? Read more about the technical implementation here.

## Supabase CDN#

Today we are launching Supabase CDN for all projects. All requests are routed
through global network of more than 250 cities.

Assets stored in Supabase Storage benefit the most from this feature since
they have a default cache time of 1 hour. They load an order of magnitude
faster, usually in just tens of ms! After the initial request, the asset will
be cached at the edge and doesn't hit your Supabase server. This frees up more
resources in your project to handle other requests.

Our Postgrest, Gotrue and Realtime APIs are also faster since SSL is
terminated at the edge. This is a brief overview of some of our other
performance enhancements we have enabled under the hood.

### TLS 1.3#

Usually, negotiating a new SSL connection requires at least 3 round trips
between the client and the server. This leads to a degraded experience for
users with high latencies. TLS1.3 reduces the number of roundtrips to
negotiate an SSL connection from 3 to 2. It also supports Zero Round Trip Time
(0-RTT) session resumption. This lets repeat users to resume a connection
without any additional roundtrips!

### HTTP/3#

HTTP/3 or HTTP over QUIC is the successor to HTTP/2. This protocol is based on
UDP instead of TCP. HTTP/3 is faster than HTTP/2 (conditions apply), is more
secure, future proof.

### Brotli#

Brotli is a new compression algorithm that performs better than gzip. All text
based responses from Supabase (including the massive amount of Javascript
required to render websites these days) are compressed with Brotli.

We can also ensure a higher degree of reliability of your Supabase APIs with a
CDN by defending against Denial of Service Attacks and bots.

## (Yet another) Supabase Functions update#

It's been four months since our [last Functions
update](https://supabase.com/blog/supabase-functions-updates) and (as it's
becoming a tradition at the end of Launch Week) we have another update for
you.

Unfortunately we're still not in a position to release anything. There are a
few reasons for this - mainly it's because we've been hyper focused on a
couple major milestones:

Since our last Functions update we've [raised our Series
A,](https://supabase.com/blog/supabase-series-a) [acquired a
company](https://supabase.com/blog/supabase-acquires-logflare), built
[Realtime Row Level Security](https://supabase.com/blog/realtime-row-level-
security-in-postgresql), [open sourced the
dashboard](https://supabase.com/blog/supabase-studio), built a GraphQL
extension for PostgreSQL, and added four Auth providers, all while growing the
community, supporting open-source tools, and delivering a few other things
that the community felt was important.

That being said, we _have_ been working on Functions, iterating through
different designs to figure out what's going to have the biggest impact for
Supabase developers. So today we are going to open up our ideas and designs
through our [RFC repo](https://github.com/supabase/rfcs) (request for
comments).

There are two important RFCs related to functions:

  * [[RFC: 0004]: Functions](https://github.com/supabase/rfcs/blob/rfc/functions/rfc/0004-functions.md) \- Outlines various options for implementing Supabase Functions.
  * [[RFC: 0005]: Functions with containers](https://github.com/supabase/rfcs/pull/5) \- Outlines our design of Functions with containers, the implementation that we are heavily leaning towards.

## Free Supabase egghead.io course#

We've partnered with the fine folks at [egghead.io](http://egghead.io) to
bring you a free, in-depth course where you'll learn how to ["Build a SaaS
product with Next.js, Supabase and Stripe"](https://egghead.io/courses/build-
a-saas-product-with-next-js-supabase-and-stripe-61f2bc20).

You will learn how to build a subscription-based billing project from scratch,
and by the end of the course, have something deployed to production that can
make you very real money!

[Check it out](https://egghead.io/courses/build-a-saas-product-with-next-js-
supabase-and-stripe-61f2bc20) entirely free on egghead, and build something
that can generate some income, while you enjoy your holidays!

## Kicking off the Holiday Hackdays#

While not everyone will be celebrating the holidays this December, we can all
be united in celebrating open-source software, and to do so we're kicking off
the "Holiday Hackdays" (loosely inspired by the [12 Pubs of
Christmas](https://www.irelandbeforeyoudie.com/12-pubs-of-christmas-rules-
tips-everything-you-need-for-a-great-night/) only a bit healthier).

Starting today at 7am PT we'll be hacking together for the next 10 days until
23:59pm PT on Sunday December 12th. And because we've launched [row-level
security for our Realtime API](https://supabase.com/blog/realtime-row-level-
security-in-postgresql) earlier this week, we'd love for you to use it in your
Hackathon project. May it be to build a [Santa
Tracker](https://www.freecodecamp.org/news/create-your-own-santa-tracker-with-
gatsby-and-react-leaflet/) or that secure family chat app to bring all your
relatives together for the festive season, be creative and most importantly
have fun 🥳

[As always](https://supabase.com/blog/hacktoberfest-hackathon-
winners-2021#the-prizes), we'll have some extremely limited edition swag to
give away that can only be won by participating in the Hackathon!

The Supabase team will be participating as well, for example
[Jon](https://twitter.com/_dijonmusters) and Thor, inspired by [Egghead's
"Holiday Course Release Extravaganza"](https://egghead.io/20-days), will be
building an Advent Calendar for all the [awesome community
content](https://supabase.com/blog/community-day#new-tutorials-and-
integration-guides) you've been creating. Get ready for a cool open-source
project which will be using a lot of the hottest Supabase features! To make
sure you don't miss this one, follow us on
[Twitter](https://twitter.com/supabase) and subscribe to our [YouTube
channel](https://www.youtube.com/supabase). We'll see you there.

Find the full hackathon details and rules in the [blog
post](https://supabase.com/blog/supabase-holiday-hackdays-hackathon).

That's it, that's another Launch Week wrapped. See you at the next one, or in
the meantime on Discord, and until then, happy hacking!

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Flaunch-
week-three-friday-five-more-
things&text=Five%20more%20things)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Flaunch-
week-three-friday-five-more-
things&text=Five%20more%20things)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Flaunch-
week-three-friday-five-more-things&t=Five%20more%20things)

[Last postSupabase Beta November 2021: Launch Week Recap15 December
2021](/blog/beta-november-2021-launch-week-recap)

[Next postpg_graphql: A GraphQL extension for PostgreSQL3 December
2021](/blog/pg-graphql)

[launch-week](/blog/tags/launch-
week)[graphql](/blog/tags/graphql)[CDN](/blog/tags/CDN)[functions](/blog/tags/functions)

On this page

  * Open source GraphQL PostgreSQL Extension
  * Supabase CDN
    * TLS 1.3
    * HTTP/3
    * Brotli
  * (Yet another) Supabase Functions update
  * Free Supabase egghead.io course
  * Kicking off the Holiday Hackdays

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Flaunch-
week-three-friday-five-more-
things&text=Five%20more%20things)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Flaunch-
week-three-friday-five-more-
things&text=Five%20more%20things)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Flaunch-
week-three-friday-five-more-things&t=Five%20more%20things)

## Build in a weekend, scale to millions

[Start your project](https://supabase.com/dashboard)[Request a
demo](/contact/sales)

