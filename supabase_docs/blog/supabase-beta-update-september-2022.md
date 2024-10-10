[Back](/blog)

[Blog](/blog)

# Supabase Beta September 2022

05 Oct 2022

•

4 minute read

[![Ant Wilson
avatar](/_next/image?url=https%3A%2F%2Fgithub.com%2Fawalias.png&w=96&q=75)Ant
WilsonCTO and Co-Founder](https://github.com/awalias)

![Supabase Beta September
2022](/_next/image?url=%2Fimages%2Fblog%2F2022-september%2Fmonthly-update-
september-2022.jpg&w=3840&q=100)

For September we made a huge effort to focus on crushing our backlog and
outstanding tickets amongst other things, here's the full list of updates for
the month...

## Kaizen Week#

Post Launch Week we did three subsequent weeks of
[Kaizen](https://en.wikipedia.org/wiki/Kaizen), a term we use internally to
deliver constant and incremental improvement. Each week had a different focus:

  * Week 1: QA and testing
  * Week 2: Documentation
  * Week 3: Issue Backlog and Automation

It's pretty rare for a company to stop feature development altogether, but
luckily we're just a bunch of developers so we all know the pain of technical
debt. After 5 Launch Weeks, working on testing and backlogs feels like a bit
of a relief.

We saw a lot of progress across our Open Issues - closing over 250 issues and
50 Pull Requests.

and we shipped a few things:

## Auth UI on Product Hunt#

We launched the new Auth UI on Product Hunt! Auth UI is a pre-built React
component for authenticating users with Supabase Auth. It supports custom
themes and extensible styles to match your brand and aesthetic.

[Check out the launch.](https://www.producthunt.com/posts/auth-ui-login-ui-
for-your-web-app)

## Postgres WASM#

If you've ever wondered, "can I run Postgres inside a browser, using an
embeddable Linux Virtual Machine?", wonder no longer. With our friends at
[Snaplet](https://www.snaplet.dev/?utm_campaign=Beta%20update%20emails&utm_source=hs_email&utm_medium=email&_hsenc=p2ANqtz-8u0x9grbiydYqh56hC_8Dta4ZiTdWbW0eXWkVCnUEUGWWoVDFXCpWzJWImkLfM-
lG-o2JX), we've released an open source Postgres WASM.

[Read the blog post](https://supabase.com/blog/postgres-wasm)  
[Comment on Hacker News](https://news.ycombinator.com/item?id=33067962)  
Visit the repo: [Snaplet](https://github.com/snaplet/postgres-wasm) | [Supabase](https://github.com/supabase-community/postgres-wasm)

## Security updates#

We're making some changes to the way the Dashboard interacts with your
database. These changes simplify the database permissions so that it's easier
for you to migrate in and out of Supabase, and they reduce the security
surface area considerably. The change will be applied automatically in
November, or you can run it today via the Dashboard.

[Review the Security
Notice](https://github.com/supabase/supabase/discussions/9314).

## Quick product updates#

  * Edge functions Free Plan script size is bumped to 2 MB
  * [functions-go](https://github.com/supabase-community/functions-go) was just contributed to supabase-community by [Zain Khan](https://twitter.com/Za1n_K)
  * A new [guide](https://supabase.com/docs/guides/auth/auth-captcha) to add captcha to your sign-in, sign-up, and password reset forms
  * New Postgres Extension for monitoring your PostgreSQL database network traffic: [pg_netstat](https://github.com/supabase/pg_netstat)
  * Added [docs](https://supabase.com/docs/guides/storage/cdn/fundamentals) for how caching works in Supabase

## Migrate from Heroku to Supabase#

In case you missed it, Heroku is shutting down their Free Plan. We're big fans
of Heroku and take a lot of inspiration from what they've built. Supabase is
compatible with Heroku's PostgreSQL product (because we're just Postgres too),
and if you have a free project running on Heroku we've created a [tool to help
migrate](https://migrate.supabase.com/) to our Free Plan.

## Made with Supabase#

[Supabase Schema](https://supabase-schema.vercel.app/): An open source, free,
login-less and secured Supabase Schema Visualizer. Simply plug in your URL and
anon key and see a visual representation of your database schema! Built by the
amazing [Zernonia](https://twitter.com/zernonia) using Vue 3, Viti, and
WindiCSS.

## Extended Community Highlights#

  * Building a viral application to visualize train routes. [Blog](https://vercel.com/blog/building-a-viral-application-to-visualize-train-routes)
  * OTP Authentication with Supabase and Twilio in React. [Tutorial](https://refine.dev/blog/supabase-twilio-otp-authentication-in-react/)
  * Join Vercel and us for [Next.js Conf](https://nextjs.org/conf).
  * Building $1K - $10K MRR Micro SaaS around Supabase. [Blog](https://microsaasidea.substack.com/p/micro-saas-products-around-supabase)
  * Watch How Netlify and Supabase Enables "Supa" DX. [Webinar](https://www.netlify.com/resources/webinars/how-netlify-supabase-enables-supa-dx/)
  * Postgres database functions are your next favorite feature! [Blog](https://mirror.xyz/0x7D15080A13c8128dBAf90a2c2326058b5c1D5eac/MaiOq5m1xSa9QfMuiLYq4bJdA0owWoTpOZNlQv76_so)
  * Create a blog with Vue, Tailwindcss & Supabase. [Part 1](https://youtube.com/watch?v=0NB9lgFcOT4) and [Part 2](https://youtube.com/watch?v=UP2mHUpcv6g)
  * Flutter Supabase Authentication. [Tutorial](https://www.sandromaglione.com/techblog/flutter-supabase-authentication-complete-tutorial)
  * Vue 3 + Pinia + Supabase Auth (Email). [Tutorial](https://towardsdev.com/vue-3-pinia-supabase-auth-email-1228f5f8502e)
  * Power up your ClickUp skills with Supabase, Figma, and DhiWise in a day. [Tutorial](https://dev.to/saloni137/power-up-your-clickup-skills-with-supabase-figma-and-dhiwise-in-a-day-3pak)
  * Creating an Email Authentication using Supabase in React. [Tutorial](https://dev.to/surajondev/creating-an-email-authentication-using-supabase-in-react-5883)

## Meme Zone#

If you made it this far in the blog post you deserve a treat. [Follow us on
Twitter](https://twitter.com/supabase) for more.

## Get started#

  * Start using Supabase today: **[supabase.com/dashboard](https://supabase.com/dashboard/)**
  * Make sure to **[star us on GitHub](https://github.com/supabase/supabase)**
  * Follow us **[on Twitter](https://twitter.com/supabase)**
  * Subscribe to our **[YouTube channel](https://www.youtube.com/c/supabase)**

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fsupabase-
beta-update-
september-2022&text=Supabase%20Beta%20September%202022)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fsupabase-
beta-update-
september-2022&text=Supabase%20Beta%20September%202022)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fsupabase-
beta-update-september-2022&t=Supabase%20Beta%20September%202022)

[Last postPostgres Full Text Search vs the rest14 October
2022](/blog/postgres-full-text-search-vs-the-rest)

[Next postPostgres WASM by Snaplet and Supabase3 October 2022](/blog/postgres-
wasm)

[release-notes](/blog/tags/release-notes)

On this page

  * Kaizen Week
  * Auth UI on Product Hunt
  * Postgres WASM
  * Security updates
  * Quick product updates
  * Migrate from Heroku to Supabase
  * Made with Supabase
  * Extended Community Highlights
  * Meme Zone
  * Get started

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fsupabase-
beta-update-
september-2022&text=Supabase%20Beta%20September%202022)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fsupabase-
beta-update-
september-2022&text=Supabase%20Beta%20September%202022)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fsupabase-
beta-update-september-2022&t=Supabase%20Beta%20September%202022)

## Build in a weekend, scale to millions

[Start your project](https://supabase.com/dashboard)[Request a
demo](/contact/sales)

