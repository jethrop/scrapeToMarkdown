[Back](/blog)

[Blog](/blog)

# Supabase Beta November 2023

05 Dec 2023

•

4 minute read

[![Ant Wilson
avatar](/_next/image?url=https%3A%2F%2Fgithub.com%2Fawalias.png&w=96&q=75)Ant
WilsonCTO and Co-Founder](https://github.com/awalias)

![Supabase Beta November 2023](/_next/image?url=%2Fimages%2Fblog%2Fbeta-
update-november-2023%2Fbeta-update-november.png&w=3840&q=100)

Launch Week X is next week! A lot has changed since our first Launch Week: we
are now a team of 70+ across more than 25 countries, shipping new features and
improving our platform faster than ever for almost 500k users.

But something hasn’t changed: our mission to be the best developer platform in
the world. Join us for another edition of the event that redefined the
launching playbook for devtools.

## Launch Week X#

Number 10! A week of launches, and this time we are shipping multiple things
every day. Make sure to get your ticket for the chance to snag some beautiful
LWX swag.

[Claim your ticket](https://supabase.com/launch-week)

## LWX Hackathon#

We can’t have a LW without a hackathon. You get ten days to build an open
source app and the chance to add your name to the Supabase Hackathon Hall of
Fame. Wanna get a team? Go check our Discord.

## Resumable Uploads for everyone#

With Resumable Uploads, you can continue uploading a file from where you left
off, even if you lose internet connectivity or accidentally close your browser
tab while uploading. We have now made Resumable Uploads available for all
projects on the Pro Plan. You can now upload files as large as 50GB.

[Read the docs](https://supabase.com/docs/guides/storage/uploads/resumable-
uploads)

## Automatic CLI login#

Logging in the CLI is as simple as typing `supabase login` . Using the browser
instead of copying the API keys from the dashboard manually. Small tweak to
the flow, huge DX improvement!

[Read how it works](https://supabase.com/blog/automatic-cli-login).

## libcluster_postgres an open source Elixir library for clustering nodes#

We needed a way for the Elixir servers to "discover" each other. Elixir has an
excellent library for this called "libcluster". We use Postgres as the common
substrate between all the nodes in our Realtime service and created a Postgres
strategy for libcluster.

[Check it out](https://github.com/supabase/libcluster_postgres)

## Quick product announcements#

  * [Edge Functions] Connecting to Postgres directly from an edge function (using a Postgres client) will use SSL by default. Users don’t need to configure anything. [[PR](https://github.com/orgs/supabase/discussions/18845)]
  * [Auth] Pro projects can now configure time-boxed sessions and inactivity timeouts. [[Doc](https://supabase.com/docs/guides/auth/sessions#limiting-session-lifetime-and-number-of-allowed-sessions-per-user)]
  * [Dashboard] Added wildcard hints for Storage bucket allowed MIME types in create/edit modal. [[PR](https://github.com/supabase/supabase/pull/19062)]

## The missing pieces to your AI app (pgvector + RAG in prod)#

Greg Richardson turned his acclaimed workshop from the AI Engineer Summit into
video so everyone could learn best practices to build AI apps and deploy
applications in the real world.

[Watch the video workshop](https://www.youtube.com/watch?v=ibzlEQmgPPY)

## Supabase and React Native resources#

Thor's been diving into the cross-platform mobile scene, showing off how
Supabase can be used with React Native to build powerful and scalable apps.
And of course, he has created some pretty cool content with all the secrets!

  * [Getting started guide](https://supabase.com/docs/guides/getting-started/tutorials/with-expo-react-native)
  * [React Native YouTube playlist](https://www.youtube.com/watch?v=AE7dKIKMJy4&list=PL5S4mPUpp4OsrbRTx21k34aACOgpqQGlx)
  * [React Native Authentication blog post](https://supabase.com/blog/react-native-authentication)

## Made with Supabase: Shotgun#

Discover how Supabase helped Shotgun, an event ticketing platform with over 3
million users, to reduce their database infrastructure costs by 83% and
streamline systems.

[Read the full story](https://supabase.com/customers/shotgun)

## Extended community highlights#

  * Build your own chatbot with Python, OpenAI, and Pipedream. [Tutorial](https://pipedream.com/blog/build-your-own-chat-bot-with-openai-and-pipedream/)
  * Why we replaced Pinecone with PGVector. [Article](https://dev.to/confidentai/why-we-replaced-pinecone-with-pgvector-2ofj)
  * How to Send Alerts from Supabase. [Tutorial](https://dev.to/patrikbraborec/how-to-send-alerts-from-supabase-3kl5)
  * FastAPI Template for LLM SaaS Part 1 — Auth and File Upload. [Tutorial](https://pub.towardsai.net/fastapi-template-for-llm-saas-part-1-auth-and-file-upload-6bada9778139)
  * SaaS Notion Clone with Realtime cursors, Nextjs 13, Stripe, Drizzle and more. [Video](https://www.youtube.com/watch?v=A3l6YYkXzzg)
  * How to Send Alerts from Supabase. [Article](https://dev.to/patrikbraborec/how-to-send-alerts-from-supabase-3kl5)
  * Building a full stack product with TypeScript. [Video](https://www.youtube.com/watch?v=b6yqVeUDDPU)
  * Flutter Flow: Use Supabase to show custom markers on Google Maps. [Tutorial](https://coffeebytez.medium.com/flutter-flow-use-supabase-to-show-custom-markers-on-google-maps-5758a69d7b7f)
  * Build a SaaS Markdown blog with Next.js 14, Stripe, Tailwind, Supabase, React. [Video](https://www.youtube.com/watch?v=293ZtCvxh90)
  * My Journey: Deploying a Django App on Vercel with Supabase. [Tutorial](https://medium.com/@kodiugos/my-journey-deploying-a-django-app-on-vercel-with-supabase-6cdb1901f724)

## We’re Hiring#

  * [Cloud Platform / Site Reliability Engineer](https://boards.greenhouse.io/supabase/jobs/5013075004)
  * [Customer Solution Architect](https://boards.greenhouse.io/supabase/jobs/5027144004)
  * [Data Engineer](https://boards.greenhouse.io/supabase/jobs/5017312004)
  * [Platform Engineer (Postgres team)](https://boards.greenhouse.io/supabase/jobs/5011466004)
  * [Revenue Operations Lead](https://boards.greenhouse.io/supabase/jobs/5006313004)
  * [Technical Product Marketer](https://boards.greenhouse.io/supabase/jobs/5005843004)

## ⚠️ Baking hot meme zone ⚠️#

**devs before going on holiday**

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fbeta-
update-
november-2023&text=Supabase%20Beta%20November%202023)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fbeta-
update-
november-2023&text=Supabase%20Beta%20November%202023)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fbeta-
update-november-2023&t=Supabase%20Beta%20November%202023)

[Last postPostgres Language Server: implementing the Parser8 December
2023](/blog/postgres-language-server-implementing-parser)

[Next postLaunch Week X Community Meetups5 December 2023](/blog/community-
meetups-lwx)

[release-notes](/blog/tags/release-notes)

On this page

  * Launch Week X
  * LWX Hackathon
  * Resumable Uploads for everyone
  * Automatic CLI login
  * libcluster_postgres an open source Elixir library for clustering nodes
  * Quick product announcements
  * The missing pieces to your AI app (pgvector + RAG in prod)
  * Supabase and React Native resources
  * Made with Supabase: Shotgun
  * Extended community highlights
  * We’re Hiring
  * ⚠️ Baking hot meme zone ⚠️

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fbeta-
update-
november-2023&text=Supabase%20Beta%20November%202023)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fbeta-
update-
november-2023&text=Supabase%20Beta%20November%202023)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fbeta-
update-november-2023&t=Supabase%20Beta%20November%202023)

## Build in a weekend, scale to millions

[Start your project](https://supabase.com/dashboard)[Request a
demo](/contact/sales)

