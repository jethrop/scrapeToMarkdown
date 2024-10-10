[Back](/blog)

[Blog](/blog)

# Supabase + Vercel Partnership

28 Aug 2024

•

4 minute read

[![Kamil Ogórek
avatar](/_next/image?url=https%3A%2F%2Fgithub.com%2Fkamilogorek.png&w=96&q=75)Kamil
OgórekIntegrations Lead](https://twitter.com/kamilogorek)

[![Jonny Summers-Muir
avatar](/_next/image?url=https%3A%2F%2Fgithub.com%2Fmildtomato.png&w=96&q=75)Jonny
Summers-MuirProduct Design](https://github.com/mildtomato)

![Supabase + Vercel Partnership](/_next/image?url=%2Fimages%2Fblog%2Fvercel-
supabase%2Fvercel-supa-thumb.png&w=3840&q=100)

Vercel just added official [First-Party
Integrations](https://vercel.com/blog/introducing-the-vercel-marketplace).
We're one of them.

This makes it _a lot_ easier to launch Postgres databases from Vercel with
full support for [Vercel
Templates](https://vercel.com/templates/next.js/supabase) and integrated
billing.

> Postgres is my favorite database—and Supabase makes Postgres _incredibly_
> easy. Plus, having first-party solutions for auth and vector search is so
> convenient when I'm trying to ship quickly. Now, I can have my Supabase
> database and my Vercel frontend together in one bill.
>
> ![Lee Robinson, VP of Product @ Vercel
> avatar](/_next/image?url=%2Fimages%2Fblog%2Favatars%2Flee-
> robinson.png&w=64&q=75)
>
> Lee Robinson, VP of Product @ Vercel

## What is the integration?#

This integration means that you can manage all your Supabase services directly
from the Vercel dashboard. You can create, manage, and delete databases and
all the credentials are automatically injected into your Vercel environment.

All the billing is unified in your Vercel bill.

## Pairing Vercel & Supabase#

Vercel + Supabase have a similar DNA - we're focused on making developers more
productive, without compromising on performance & scale. Vercel and Supabase
are #1 and #2 most popular for [developers shout
outs](https://www.producthunt.com/shoutouts/engineering-development) on
ProductHunt.

We've found that Supabase and Vercel has been a very popular pairing for scale
ups, YC companies, and large enterprises.

> I don't think we would have grown so quickly without Supabase and Vercel. We
> have used many different products since we started the company, but Supabase
> and Vercel are the few services that we still use today. Now, there are
> 180,000 Resend users sending millions of emails every single day, and even
> though we outgrew many other products, Supabase and Vercel continue to help
> scale our company despite our challenges evolving all the time.
>
> ![Zeno Rocha, CEO @ Resend
> avatar](/_next/image?url=%2Fimages%2Fblog%2Favatars%2Fzeno-
> rocha.png&w=64&q=75)
>
> Zeno Rocha, CEO @ Resend

## Features#

Check out some of these features that make Supabase + Vercel a great
combination:

### Pure, Dedicated Postgres#

When you launch a Postgres database on Supabase, you get a full instance on
dedicated hardware. It's safe, secure, and resilient to noisy neighbors.

### Extended, modular building blocks#

Supabase is a [modular platform](/docs/guides/getting-
started/architecture#everything-works-in-isolation), offering a number of
building blocks to extend Postgres. You get [AI/Vectors](/docs/guides/ai),
[Auth](https://supabase.com/docs/guides/auth), [File
Storage](/docs/guides/storage), [Realtime](/docs/guides/realtime), and [Edge
Functions](/docs/guides/functions).

### Templates#

The Vercel [template
marketplace](https://vercel.com/templates?search=supabase) is one of our
favorite features of the Vercel platform. With a single click you can
provision an entire stack in under a minute, and connect it to a GitHub repo
for further development. Try it now using our [starter
template](https://vercel.com/templates/next.js/supabase).

### Low latency & Read replicas#

Supabase runs in 16 different AWS regions, which means that you can choose to
run your database as close to your Vercel Functions (and users) as possible.
If you have users across the planet, check out [Read
Replicas](https://supabase.com/docs/guides/platform/read-replicas).

### Integrated billing#

With the new integration, everything is unified in your Vercel bill. All
Supabase services will be visible in a single monthly invoice.

## Costs & Pricing#

All services created through the Vercel integration are _exactly the same
price_ that you'd get on the Supabase platform - including the **2 free
databases** that we offer to all developers.

Supabase has [predictable pricing](/pricing) with [spend
caps](/docs/guides/platform/spend-cap) for developers who are worried about
becoming [too successful](https://i.kym-
cdn.com/photos/images/newsfeed/001/444/303/2b6.jpg) with their upcoming
launch.

At the time of publishing (28 August 2024), this integration is in Public
Alpha. Check the [docs](/docs/guides/platform/vercel-marketplace) for the
latest updates.

## Try it out#

The fastest way to get started is to try out the [**Supabase
Starter**](https://vercel.com/templates/next.js/supabase) on the Vercel
Template marketplace. With a few clicks you get a Next.js App Router template
configured with cookie-based auth using Supabase, Postgres, TypeScript, and
Tailwind CSS.

##### Deploy a Next.js app with Supabase Vercel Storage now

Uses the Next.js Supabase Starter Template

[![Deploy with
Vercel](https://vercel.com/button)](https://vercel.com/new/clone?demo-
description=This+starter+configures+Supabase+Auth+to+use+cookies%2C+making+the+user%27s+session+available+throughout+the+entire+Next.js+app+-+Client+Components%2C+Server+Components%2C+Route+Handlers%2C+Server+Actions+and+Middleware.&demo-
image=%2F%2Fimages.ctfassets.net%2Fe5382hct74si%2F7UG4Pvl9its0CqhrpX93n%2F262032f6e408308d3273f5883f369e97%2F68747470733a2f2f64656d6f2d6e6578746a732d776974682d73757061626173652e76657263656c2e6170702f6f70656e67726170682d696d6167652e70.png&demo-
title=nextjs-with-supabase&demo-url=https%3A%2F%2Fdemo-nextjs-with-
supabase.vercel.app%2F&external-
id=https%3A%2F%2Fgithub.com%2Fvercel%2Fnext.js%2Ftree%2Fcanary%2Fexamples%2Fwith-
supabase&project-name=nextjs-with-supabase&repository-name=nextjs-with-
supabase&repository-
url=https%3A%2F%2Fgithub.com%2Fvercel%2Fnext.js%2Ftree%2Fcanary%2Fexamples%2Fwith-
supabase&stores=%5B%7B%22type%22%3A%22integration%22%2C%22integrationSlug%22%3A%22supabase%22%2C%22productSlug%22%3A%22supabase%22%7D%5D&teamSlug=vercel)

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fsupabase-
vercel-
partnership&text=Supabase%20%2B%20Vercel%20Partnership)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fsupabase-
vercel-
partnership&text=Supabase%20%2B%20Vercel%20Partnership)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fsupabase-
vercel-partnership&t=Supabase%20%2B%20Vercel%20Partnership)

[Last postIn-Browser Semantic AI Search with PGlite and Transformers.js29
August 2024](/blog/in-browser-semantic-search-pglite)

[Next postSupabase Launch Week 12 Hackathon26 August 2024](/blog/supabase-
lw12-hackathon)

[product](/blog/tags/product)

On this page

  * What is the integration?
  * Pairing Vercel & Supabase
  * Features
    * Pure, Dedicated Postgres
    * Extended, modular building blocks
    * Templates
    * Low latency & Read replicas
    * Integrated billing
  * Costs & Pricing
  * Try it out

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fsupabase-
vercel-
partnership&text=Supabase%20%2B%20Vercel%20Partnership)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fsupabase-
vercel-
partnership&text=Supabase%20%2B%20Vercel%20Partnership)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fsupabase-
vercel-partnership&t=Supabase%20%2B%20Vercel%20Partnership)

## Build in a weekend, scale to millions

[Start your project](https://supabase.com/dashboard)[Request a
demo](/contact/sales)

