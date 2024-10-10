[Back](/blog)

[Blog](/blog)

# Top 10 Launches from Supabase GA Week

18 Apr 2024

•

5 minute read

[![Paul Copplestone
avatar](/_next/image?url=https%3A%2F%2Fgithub.com%2Fkiwicopple.png&w=96&q=75)Paul
CopplestoneCEO and Co-Founder](https://github.com/kiwicopple)

![Top 10 Launches from Supabase GA
Week](/_next/image?url=%2Fimages%2Fblog%2Fga-week%2Fga-week-
summary%2Fthumb.png&w=3840&q=100)

There's always a lot to cover in Launch Weeks. Here are a few highlights:

### #10: Bootstrap: the fastest way to launch a project#

Supabase Bootstrap is the fastest way to spin up a new hosted Supabase project
from existing starter templates. Just run `supabase bootstrap` with our CLI
and we'll help you launch a new application and attach a remote database to
get you started.

[Read more.](https://supabase.com/blog/supabase-bootstrap)

### #9: Branching is now Publicly available#

Supabase Branching is now in open beta. You can enable it on any project
that's Pro Plan or above. Branching is a seamless integration of Git with your
development workflow, extending beyond your local environment to a remote
database.

[Read more.](https://supabase.com/blog/branching-publicly-available)

### #8: Postgres Index Advisor#

We shipped a Postgres extension for recommending indexes to improve query
performance. It leans heavily on [HypoPG](https://github.com/HypoPG/hypopg),
an excellent extension to determine if Postgres will use a given index without
spending resources to create them.

[See the HN discussion.](https://github.com/supabase/index_advisor)

### #7: Official Swift support#

The Supabase Swift libraries are now officially supported by Supabase. This
makes it simple to interact with Supabase from applications on Apple's
platforms, including iOS, macOS, watchOS, tvOS, and visionOS.

[Read more.](https://supabase.com/blog/supabase-swift)

### #6: Security Advisor + Performance Advisor#

We're dropping some handy tools in Supabase Studio this week to help with
security and performance: a **Security Advisor** for detecting insecure
database configuration, and a **Performance Advisor** for suggesting database
optimizations.

[Read more.](https://supabase.com/blog/security-performance-advisor)

### #5: Native AI support in Edge Functions#

We're making it super easy to run AI models within Supabase Edge Functions. We
have a new API to generate embeddings and upcoming support for Large Language
Models like `llama3` and `mistral`.

[Read more.](https://supabase.com/blog/ai-inference-now-available-in-supabase-
edge-functions)

### #4: S3 compatibility in Supabase Storage#

Supabase Storage is now officially an S3-Compatible Storage Provider. With the
support of the S3 protocol, you can now connect Supabase Storage to thousands
of 3rd-party tools and services, and make it even easier to use Supabase for
data engineering.

[Read more.](https://supabase.com/blog/s3-compatible-storage)

### #3: Anonymous sign-ins#

Anonymous sign-ins can be used to create **temporary users** who haven't
signed up for your application yet. This lowers the friction for new users to
try out your product since they don't have to provide any signup credentials.
One of our [most-requested
features](https://github.com/supabase/auth/issues/68) by the community!

[Read more.](https://supabase.com/blog/anonymous-sign-ins)

### #2: Oriole joins Supabase#

[Oriole](https://github.com/orioledb/orioledb) is a table storage extension
for Postgres. It is designed to be a drop-in replacement for Postgres'
existing storage engine, and benchmarks show that it's significantly faster.
Over time we hope that it can become available for any Postgres installation
and we will continue to work with Oriole and the Postgres community to make
this happen.

[Read more.](https://supabase.com/blog/supabase-acquires-oriole)

### #1: General Availability#

Supabase is now GA. During the first year of Supabase we set ourselves a goal:
build a managed platform capable of securely running 1 million databases.
Today we've proven that metric and we're announcing the General Availability
of the platform that will serve the next 99 million.

[Check out the journey so far.](https://supabase.com/ga)

## More updates#

There's been a few other highlights this week:

### Supabase + Fly updates#

In the previous Launch Week we started working on [Fly Postgres, a managed
offering from Supabase](https://supabase.com/blog/postgres-on-fly-by-
supabase). We've received a lot of feedback from early testers, and we're
working hard to make the service available and as resilient for production
workloads.

Today we're opening up access to everyone **for testing**. Testers can also
try [Branching](/docs/guides/platform/branching), an opt-in feature which
creates an ephemeral test environment for your git branches. These instances
automatically pause when you aren't using them.

##### Testing only

The service is in public alpha. We don't recommend using it for production.

### Meetups in 27 cities#

We started GA Week with 10 confirmed community meetups. Over the week, more
community members volunteered to host meetups in their own cities. With 25
meetups across the world, some with just 3 people and some with over 50, the
Supabase community has truly made our team feel thankful. A huges shout out to
these organizers:

Rita & Ann (New York), Mansueli & Guilherme (Maringá), Florian (Seoul), Jose &
Aile (Miami), Philippe (Berlin), Tyler (Tokyo), Ivan (Tenerife), Thor
(Singapore), Jack (London), Fatuma (Nairobi), Emilio (Milan), Jay Raj Mishra
(Kathmandu), Bharat (New Delhi), Abdulhakeem Adams (Ilorin, Nigeria), Kyle
Rummens (Utah, USA), Laksh (Nagpur, India), Cam Blackwood (Edinburgh,
Scotland), Harry (Central Manchester), Guilleume (Dubai), Kristian (Bergen,
Norway), Andrei (Zagreb, Croatia), Misel (Serbia), Matthew (Toronto, Canada),
Charlie Coppinger (Wellington, NZ), Nicolas Montone (Buenos Aires, Argentina),
Ryan Griffin (Melbourne, Australia), Isheanesu (Cape Town, SA), Aileen
(Monterrey, Mexico), Martin (Hong Kong), Bilal Aamer (Hyderabad, India),
Gabriel Pan Gantes (Barcelona, Spain).

### Upcoming Meetup in SF#

We're also hosting a bigger meeting in San Fransisco in June, with a few
friends like [Fly.io](http://Fly.io), [Ollama](https://ollama.com/), and
[Tigris](https://www.tigrisdata.com/). If you want to hang out with Ant & I,
sign up for a full day of hacking at the a16z office:

[Register here](https://lu.ma/gvgaqkrt)

### Hackathon#

The 10-day hackathon is still going! If you want a chance to win a set of
Apple AirPods along with extremely limited edition Supabase swag check out
[all the details here](https://supabase.com/blog/supabase-oss-hackathon).

Until next Launch Week, keep building cool stuff.

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

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fga-
week-
summary&text=Top%2010%20Launches%20from%20Supabase%20GA%20Week)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fga-
week-
summary&text=Top%2010%20Launches%20from%20Supabase%20GA%20Week)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fga-
week-summary&t=Top%2010%20Launches%20from%20Supabase%20GA%20Week)

[Last postSupabase Storage: now supports the S3 protocol18 April
2024](/blog/s3-compatible-storage)

[Next postSupabase Security Advisor & Performance Advisor18 April
2024](/blog/security-performance-advisor)

[launch-week](/blog/tags/launch-week)

On this page

  * #10: Bootstrap: the fastest way to launch a project
  * #9: Branching is now Publicly available
  * #8: Postgres Index Advisor
  * #7: Official Swift support
  * #6: Security Advisor + Performance Advisor
  * #5: Native AI support in Edge Functions
  * #4: S3 compatibility in Supabase Storage
  * #3: Anonymous sign-ins
  * #2: Oriole joins Supabase
  * #1: General Availability

  * More updates
    * Supabase + Fly updates
    * Meetups in 27 cities
    * Upcoming Meetup in SF
    * Hackathon

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fga-
week-
summary&text=Top%2010%20Launches%20from%20Supabase%20GA%20Week)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fga-
week-
summary&text=Top%2010%20Launches%20from%20Supabase%20GA%20Week)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fga-
week-summary&t=Top%2010%20Launches%20from%20Supabase%20GA%20Week)

## Build in a weekend, scale to millions

[Start your project](https://supabase.com/dashboard)[Request a
demo](/contact/sales)

