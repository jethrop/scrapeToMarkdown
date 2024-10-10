[Back](/blog)

[Blog](/blog)

# Supabase Auth

05 Aug 2020

•

4 minute read

[![Paul Copplestone
avatar](/_next/image?url=https%3A%2F%2Fgithub.com%2Fkiwicopple.png&w=96&q=75)Paul
CopplestoneCEO and Co-Founder](https://github.com/kiwicopple)

Supabase is an open source Firebase alternative. We are building the features
of Firebase using scalable, open source products.

Two months ago a developer discovered Supabase and (unexpectedly) [launched us
on Hacker News](https://news.ycombinator.com/item?id=23319901). Although we
had completed only 3 months of development the community support was both
incredible and humbling.

Developers were obviously excited about the prospect of an open source
Firebase alternative, but the comments were dominated by one emphatic feature
request: Auth.

> " _Just FYI, making a good auth solution in Supabase will instantly make me
> a customer._ "  
> @pdimitar

> " _For me the MVP, before I could use it for my commercial projects, would
> be: DB+auth. At that point, I could switch - and probably would._ "  
> @julianeon

> " _This looks great, however at first peek it doesn't mention anything about
> auth. Do you have any plans for that? For me this is the topic I most want
> to just delegate to the service._ "  
> @2mol

So we got to work, and today we're ecstatic to launch Supabase Auth. Let's dig
into some of the features of the Auth system.

## Supabase Auth#

Supabase Auth provides all the backend services you need to authenticate and
authorize your users.

### User management#

Supabase makes it simple to onboard your users with our new
`supabase.auth.signUp()` and `supabase.auth.signIn()`
[functions](/docs/guides/auth).

### Row Level Security#

Authentication only gets you so far. When you need granular authorization
rules, nothing beats PostgreSQL's [Row Level
Security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html).
Supabase makes it simple to turn RLS on and off.

### Policies#

[Policies](https://www.postgresql.org/docs/current/sql-createpolicy.html) are
PostgreSQL's rule engine. They are incredibly powerful and flexible, allowing
you to write complex SQL rules which fit your unique business needs.

With policies, your database becomes the rules engine. Instead of repetitively
filtering your queries, like this ...

`  

_10

const loggedInUserId = 'd0714948'

_10

let user = await supabase.from('users').select('user_id, name').eq('user_id',
loggedInUserId)\n

_10

// Returns { id: 'd0714948', name: 'Jane'

  
`

... you can simply define a rule on your database table, `(select auth.uid())
= user_id`, and your request will return the rows which pass the rule, even
when you remove the filter from your middleware:

`  

_10

let user = await supabase.from('users').select('user_id, name')\n

_10

// Still returns { id: 'd0714948', name: 'Jane' }

  
`

### Open source#

Building an open source Firebase alternative is difficult task, made possible
by an amazing suite of OSS tools that have forged the way for Supabase. We
spent many weeks building Auth POC's with existing OSS tools. Notable mentions
go to RedHat's [KeyCloak](https://www.keycloak.org/), and Ory's
[Kratos](https://github.com/ory/kratos).

Ultimately we landed on a system which utilises three amazing open source
products:

  * Authorization: [PostgreSQL](https://www.postgresql.org/) and [PostgREST](http://postgrest.org/en/v7.0.0/auth.html).
  * Authentication: Netlify's [GoTrue](https://github.com/netlify/gotrue) server, which we forked and will continue to contribute to.

### Next steps#

Supabase has a culture of shipping early and often. Our Auth release is
another example of this, and we still have a lot of work to do. Next month we
have more Auth features planned, including custom email templates and 3rd-
party OAuth providers. We also plan to simplify the Policy interface, enabling
non-technical users to get started with one of PostgreSQL's best features.

### Get started#

Supabase Auth is ready for you to start using today, free of charge:
[supabase.com/dashboard](https://supabase.com/dashboard)

To see the full power of our auth system, watch [this
demo](https://youtu.be/2oqIZW5S-lQ) where I deploy a secure, real-time slack
clone to Vercel in less than 3 minutes.

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fsupabase-
auth&text=Supabase%20Auth)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fsupabase-
auth&text=Supabase%20Auth)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fsupabase-
auth&t=Supabase%20Auth)

[Last postSupabase Alpha August 20203 September 2020](/blog/supabase-alpha-
august-2020)

[Next postContinuous PostgreSQL Backups using WAL-G2 August
2020](/blog/continuous-postgresql-backup-walg)

[supabase](/blog/tags/supabase)

On this page

  * Supabase Auth

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fsupabase-
auth&text=Supabase%20Auth)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fsupabase-
auth&text=Supabase%20Auth)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fsupabase-
auth&t=Supabase%20Auth)

## Build in a weekend, scale to millions

[Start your project](https://supabase.com/dashboard)[Request a
demo](/contact/sales)

