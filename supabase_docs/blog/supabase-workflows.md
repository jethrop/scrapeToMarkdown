[Back](/blog)

[Blog](/blog)

# Workflows are coming to Supabase

02 Apr 2021

•

9 minute read

[![Francesco Ceccon
avatar](/_next/image?url=https%3A%2F%2Fgithub.com%2Ffracek.png&w=96&q=75)Francesco
CecconEngineering](https://github.com/fracek)

![Workflows are coming to
Supabase](/_next/image?url=%2Fimages%2Fblog%2Fworkflows%2Fworkflows-
thumb.jpg&w=3840&q=100)

This week we [launched Supabase Storage](/blog/supabase-storage), which leaves
one other huge piece of the stack that everyone is asking for: Functions.

## TLDR#

We're not releasing Functions today. Trust us, we know you want them. They are
coming, just not today.

But we are building something that we think you're going to like: Workflows.
We haven't finished building it yet, but Workflows are a "piece" of the
Function story and arguably an even more exciting feature.

## Firebase Functions#

Firebase functions are relatively simple. If you use Serverless, AWS Lambda,
Cloudflare Workers, Next.js API routes, or Netlify Functions, then you know
how they work. A Firebase function executes some code which you provide,
without you managing a server.

Specifically for Firebase, they have another key feature - they can be
triggered by database events. For example, you can trigger a function whenever
a Firestore Document is updated.

This is great, but it is still limited for a few real-world use cases. For
example, what if you want to send an email to a user one day after a user
signs up. Or one year? There is no queuing functionality in Firebase. You'd
have to manage a process like this yourself, probably using a cron-job.

## A better solution?#

We searched for some open source tools which we think are solving this problem
well. We looked at [NodeRed](/blog/supabase-storage#designing-the-storage-
middleware), [n8n](https://n8n.io/),
[Airflow](http://airflow.apache.org/blog/airflow-two-point-oh-is-here/), and
about 10 other tools. They are amazing tools on their own, but for the
Supabase Stack they ultimately had the [same shortcomings](/blog/supabase-
storage#integration-with-the-supabase-ecosystem) that we found with Storage
providers - most of them lacked deep Postgres integration.

We went back to the drawing board and asked, "if we could wave a wand and get
the perfect solution, what would it look like?". The tool that came very close
is [AWS Step Functions](https://aws.amazon.com/step-functions/). The only
problem: it's not open source. Luckily, their [state language](https://states-
language.net/spec.html) is.

Using this states language, we are [building an open source orchestration
engine](https://github.com/supabase/workflows) for managing very complex
Workflows with queueing, etc. It will be built with Elixir.

This engine won't execute code. Instead, it will coordinate and execute
existing functions wherever they live: AWS, GCP, Azure, OpenFaas, and of
course Postgres.

We plan to add "modules" which work natively: email services, notification
services, and other platforms.

The engine is deeply integrated with Postgres. `Jobs`, `queues`, and `logs`
will be stored and accessible by SQL. We'd like to give a shoutout to the
[Oban](https://getoban.pro) team here, their robust job processing was a big
missing piece for the engine. And most importantly, it's backed by Postgres!

Once ready, we will make this available in the Supabase Dashboard with a
Zapier-like interface.

## What are Workflows#

Workflows orchestrate and execute functions in response to a database event
(insert, update, delete) or a HTTP call (direct invocation).

You can use them to rapidly develop microservices (once we have functions)
without worrying about servers.

Workflows are stateless - the output of a state becomes the input of the next
state.

Workflows are defined using Amazon States Languages, so you can import your
workflows from AWS (although we are still building handlers for most AWS
resources).

Workflows can be _persistent_ (the default). This means they are tolerant to
server restarts, but it also means they need to use the database to store
their state.

Workers can be _transient._ These are fully in-memory if you don't want to
store the execution state (for example, IoT applications that trigger
workflows very often). Transient workflows are not restarted if the server
crashes or is restarted.

## Example#

A typical use-case for workflows is sending emails. For example, you might
want to send a user an email one day after they sign up. In database terms we
can say: "trigger an email workflow whenever there is an insert on the `users`
table."

Let's break this down into steps, then tie it all together at the end:

### Sending an email#

`  

_10

SendEmail:

_10

Type: Task

_10

Next: Complete

_10

Resource: my-email-service

_10

Parameters:

_10

api_key: my-api-key

_10

template_id: welcome-email

_10

payload:

_10

name.$: '$.record.name'

_10

email.$: '$.record.email'

  
`

Here we have a "Task" which triggers a call to an email service (like Mailgun
or Postmark). Specifically, it's telling the service to send the `welcome-
email` template, and it's providing it a `name` and an `email` as parameters.

### Waiting a day#

Since we don't want to send the email immediately, we need to tell Workflows
to wait one day

`  

_10

WaitOneDay:

_10

Type: Wait

_10

Next: SendEmail

_10

Seconds: 86400

  
`

Here "one day" is specified in seconds.

### Trigger on insert#

We mentioned that you could trigger a workflow whenever there is an "insert"
on the `users` table. But what if you insert multiple users at once? Not a
problem - we can loop through all the inserts with a `Map`:

`  

_14

EmailUsers:

_14

Type: Map

_14

End: true

_14

InputPath: '$.changes'

_14

Iterator:

_14

StartAt: CheckInsert

_14

States:

_14

CheckInsert:

_14

Type: Choice

_14

Default: Complete

_14

Choices:

_14

- Variable: '$.type'

_14

StringEquals: INSERT

_14

Next: WaitOneDay

  
`

In this part, we have a task "EmailUsers", which iterates through all the
database events (`$.changes`) and checks if they are INSERTs.

### Tying it all together#

Let's see how it looks all together:

`  

_34

---

_34

Comment: Email users after one day

_34

StartAt: EmailUsers

_34

States:

_34

EmailUsers:

_34

Type: Map

_34

End: true

_34

InputPath: '$.changes'

_34

Iterator:

_34

StartAt: CheckInsert

_34

States:

_34

CheckInsert:

_34

Type: Choice

_34

Default: Complete

_34

Choices:

_34

- Variable: '$.type'

_34

StringEquals: INSERT

_34

Next: WaitOneDay

_34

WaitOneDay:

_34

Type: Wait

_34

Next: SendEmail

_34

Seconds: 86400

_34

SendEmail:

_34

Type: Task

_34

Next: Complete

_34

Resource: send-templated-email

_34

Parameters:

_34

api_key: my-api-key

_34

template_id: welcome-email

_34

payload:

_34

name.$: '$.record.name'

_34

email.$: '$.record.email'

_34

Complete:

_34

Type: Succeed

  
`

The workflow receives the following JSON data from Supabase
[Realtime](https://github.com/supabase/realtime):

`  

_36

{

_36

"changes": [

_36

{

_36

"columns": [

_36

{

_36

"flags": ["key"],

_36

"name": "id",

_36

"type": "int8",

_36

"type_modifier": 4294967295

_36

},

_36

{

_36

"flags": [],

_36

"name": "name",

_36

"type": "text",

_36

"type_modifier": 4294967295

_36

},

_36

{

_36

"flags": [],

_36

"name": "email",

_36

"type": "text",

_36

"type_modifier": 4294967295

_36

}

_36

],

_36

"commit_timestamp": "2021-03-17T14:00:26Z",

_36

"record": {

_36

"id": "101492",

_36

"name": "Alfred",

_36

"email": "[[email protected]](/cdn-cgi/l/email-protection)"

_36

},

_36

"schema": "public",

_36

"table": "users",

_36

"type": "INSERT"

_36

}

_36

],

_36

"commit_timestamp": "2021-03-17T14:00:26Z"

_36

}

  
`

## Next Steps#

We've already open sourced the Workflow interpreter
[here](https://github.com/supabase/workflows). It's built with Elixir, so you
can find it on Hex [here](https://hexdocs.pm/workflows/Workflows.html).

After we've ironed out a few bugs we will integrate it into the Supabase
Stack. As with all Supabase features, we'll add a [nice
UI](https://ui.supabase.com/) to make prototyping extremely rapid. We'll
integrate the UI with the code (via Git) to make sure everything is version
controlled.

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fsupabase-
workflows&text=Workflows%20are%20coming%20to%20Supabase)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fsupabase-
workflows&text=Workflows%20are%20coming%20to%20Supabase)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fsupabase-
workflows&t=Workflows%20are%20coming%20to%20Supabase)

[Last postPgBouncer is now available in Supabase2 April 2021](/blog/supabase-
pgbouncer)

[Next postSupabase Launches NFT Marketplace1 April 2021](/blog/supabase-nft-
marketplace)

[functions](/blog/tags/functions)[workflows](/blog/tags/workflows)

On this page

  * TLDR
  * Firebase Functions
  * A better solution?
  * What are Workflows
  * Example
  * Next Steps

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fsupabase-
workflows&text=Workflows%20are%20coming%20to%20Supabase)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fsupabase-
workflows&text=Workflows%20are%20coming%20to%20Supabase)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fsupabase-
workflows&t=Workflows%20are%20coming%20to%20Supabase)

## Build in a weekend, scale to millions

[Start your project](https://supabase.com/dashboard)[Request a
demo](/contact/sales)

