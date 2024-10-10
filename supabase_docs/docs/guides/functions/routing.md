[![Supabase wordmark](/docs/_next/image?url=%2Fdocs%2Fsupabase-
dark.svg&w=256&q=75&dpl=dpl_BJ9ShNdrRifaAcUSP15Lr1pJVtdF)![Supabase
wordmark](/docs/_next/image?url=%2Fdocs%2Fsupabase-
light.svg&w=256&q=75&dpl=dpl_BJ9ShNdrRifaAcUSP15Lr1pJVtdF)DOCS](/docs)

  * [Start](/docs/guides/getting-started)
  * Products
  * Build
  * Manage
  * Reference
  * Resources

[![Supabase wordmark](/docs/_next/image?url=%2Fdocs%2Fsupabase-
dark.svg&w=256&q=75&dpl=dpl_BJ9ShNdrRifaAcUSP15Lr1pJVtdF)![Supabase
wordmark](/docs/_next/image?url=%2Fdocs%2Fsupabase-
light.svg&w=256&q=75&dpl=dpl_BJ9ShNdrRifaAcUSP15Lr1pJVtdF)DOCS](/docs)

Search docs...

K

Edge Functions

  1. [Edge Functions](/docs/guides/functions)
  2.   3. Guides
  4.   5. [Handling Routing in Functions](/docs/guides/functions/routing)
  6. 

# Handling Routing in Functions

## How to handle custom routing within Edge Functions.

* * *

Usually, an Edge Function is written to perform a single action (eg: write a
record to the database). However, if your app's logic is split into multiple
Edge Functions requests to each action may seem slower. This is because each
Edge Function needs to be booted before serving a request (known as cold
starts). If an action is performed less frequently (eg: deleting a record),
there is a high-chance of that function experiencing a cold-start.

One way to reduce the cold starts and increase performance of your app is to
combine multiple actions into a single Edge Function. This way only one
instance of the Edge Function needs to be booted and it can handle multiple
requests to different actions. For example, we can use a single Edge Function
to create a typical CRUD API (create, read, update, delete records).

To combine multiple endpoints into a single Edge Function, you can use web
application frameworks such as [Express](https://expressjs.com/),
[Oak](https://oakserver.github.io/oak/), or [Hono](https://hono.dev).

Let's dive into some examples.

## Routing with Frameworks#

Here's a simple hello world example using some popular web frameworks.

Create a new function called `hello-world` using Supabase CLI:

`  

_10

supabase functions new hello-world

  
`

Copy and paste the following code:

ExpressOakHonoDeno

`  

_14

import { Hono } from 'jsr:@hono/hono';

_14

_14

const app = new Hono();

_14

_14

app.post('/hello-world', async (c) => {

_14

const { name } = await c.req.json();

_14

return new Response(`Hello ${name}!`)

_14

});

_14

_14

app.get('/hello-world', (c) => {

_14

return new Response('Hello World!')

_14

});

_14

_14

Deno.serve(app.fetch);

  
`

You will notice in the above example, we created two routes - `GET` and
`POST`. The path for both routes are defined as `/hello-world`. If you run a
server outside of Edge Functions, you'd usually set the root path as `/` .
However, within Edge Functions, paths should always be prefixed with the
function name (in this case `hello-world`).

You can deploy the function to Supabase via:

`  

_10

supabase functions deploy hello-world

  
`

Once the function is deployed, you can try to call the two endpoints using
cURL (or Postman).

`  

_10

# https://supabase.com/docs/guides/functions/deploy#invoking-remote-functions

_10

curl --request GET 'https://<project_ref>.supabase.co/functions/v1/hello-
world' \

_10

--header 'Authorization: Bearer ANON_KEY' \

  
`

This should print the response as `Hello World!`, meaning it was handled by
the `GET` route.

Similarly, we can make a request to the `POST` route.

cURL

`  

_10

# https://supabase.com/docs/guides/functions/deploy#invoking-remote-functions

_10

curl --request POST 'https://<project_ref>.supabase.co/functions/v1/hello-
world' \

_10

--header 'Authorization: Bearer ANON_KEY' \

_10

--header 'Content-Type: application/json' \

_10

--data '{ "name":"Foo" }'

  
`

We should see a response printing `Hello Foo!`.

## Using Route Parameters#

We can use route parameters to capture values at specific URL segments (eg:
`/tasks/:taskId/notes/:noteId`).

Here's an example Edge Function implemented using the Framework for managing
tasks using route parameters. Keep in mind paths must be prefixed by function
name (ie. `tasks` in this example). Route parameters can only be used after
the function name prefix.

ExpressOakHonoDeno

## URL Patterns API#

If you prefer not to use a web framework, you can directly use [URLPattern
API](https://developer.mozilla.org/en-US/docs/Web/API/URL_Pattern_API) within
your Edge Functions to implement routing. This is ideal for small apps with
only couple of routes and you want to have a custom matching algorithm.

Here is an example Edge Function using URL Patterns API:
<https://github.com/supabase/supabase/blob/master/examples/edge-
functions/supabase/functions/restful-tasks/index.ts>

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/content/guides/functions/routing.mdx)

  * Need some help?

[Contact support](https://supabase.com/support)

  * Latest product updates?

[See Changelog](https://supabase.com/changelog)

  * Something's not right?

[Check system status](https://status.supabase.com/)

* * *

[© Supabase
Inc](https://supabase.com/)—[Contributing](https://github.com/supabase/supabase/blob/master/apps/docs/DEVELOPERS.md)[Author
Styleguide](https://github.com/supabase/supabase/blob/master/apps/docs/CONTRIBUTING.md)[Open
Source](https://supabase.com/open-
source)[SupaSquad](https://supabase.com/supasquad)Privacy Settings

[GitHub](https://github.com/supabase/supabase)[Twitter](https://twitter.com/supabase)[Discord](https://discord.supabase.com/)

