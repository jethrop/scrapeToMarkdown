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

Functions Server Reference

![](/docs/img/icons/menu/reference-analytics.svg)

# Self-Hosting Functions

A web server based on [Deno](https://deno.land) runtime, capable of running
JavaScript, TypeScript, and WASM services.

You can use it to:

  * Locally test and self-host Supabase's Edge Functions (or any Deno Edge Function)
  * As a programmable HTTP Proxy: You can intercept / route HTTP requests

##### Beta Version

Self hosted Edge functions are in beta. There will be breaking changes to APIs
/ Configuration Options.

## How to run locally#

`  

_10

./run.sh start --main-service /path/to/supabase/functions -p 9000

  
`

using Docker:

`  

_10

docker build -t edge-runtime .

_10

docker run -it --rm -p 9000:9000 -v /path/to/supabase/functions:/usr/services
supabase/edge-runtime start --main-service /usr/services

  
`

## How to update to a newer Deno version#

  * Select the Deno version to upgrade and visit its tag on GitHub (eg: <https://github.com/denoland/deno/blob/v1.30.3/Cargo.toml>)
  * Open the `Cargo.toml` at the root of this repo and modify all `deno_*` modules to match to the selected tag of Deno.

## Self hosting Edge Functions on Fly.io#

We have put together a demo on how to self-host edge functions on
[Fly.io](http://Fly.io) (you can also use other providers like Digital Ocean
or AWS).

To try it yourself,

  1. Sign up for an [Fly.io](http://Fly.io) account and install [flyctl](https://fly.io/docs/hands-on/install-flyctl/)
  2. Clone the demo repository to your machine - <https://github.com/supabase/self-hosted-edge-functions-demo>
  3. Copy your Edge Function into the `./functions` directory in the demo repo.
  4. Update the Dockerfile to pull the latest edge-runtime image (check [releases](https://github.com/supabase/edge-runtime/pkgs/container/edge-runtime))
  5. [Optional] Edit `./functions/main/index.ts`, adding any other request preprocessing logic (for example, you can enable JWT validation, handle CORS requests)
  6. Run `fly launch` to create a new app to serve your Edge Functions
  7. Access your Edge Function by visiting: `https://{your-app-name}.fly.dev/{your-function-name}`

You can view the logs for the Edge Runtime, by visiting Fly.io’s Dashboard >
Your App > Metrics. Also, you can serve edge-runtime from multiple regions by
running `fly regions add [REGION]`.

### Client libraries#

  * [JavaScript](https://supabase.com/docs/reference/javascript/functions-invoke)
  * [Dart](https://supabase.com/docs/reference/dart/functions-invoke)

### Additional Links#

  * [Source code](https://github.com/supabase/edge-runtime/)

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

