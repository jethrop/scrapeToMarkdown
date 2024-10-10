[Back](/blog)

[Blog](/blog)

# Edge Functions are now 2x smaller and boot 3x faster

12 Sep 2024

•

7 minute read

[![Nyannyacha
avatar](/_next/image?url=https%3A%2F%2Fgithub.com%2Fnyannyacha.png&w=96&q=75)NyannyachaEngineering](https://github.com/nyannyacha)

![Edge Functions are now 2x smaller and boot 3x
faster](/_next/image?url=%2Fimages%2Fblog%2Fedge-functions-faster-
smaller%2Fedge-fns-faster-thumb.png&w=3840&q=100)

We’ve rolled out some exciting updates to Edge Functions which bring
significant reductions to function size and boot time. If you’re using [npm
modules](https://supabase.com/blog/edge-functions-node-npm) in your functions,
you should see function sizes being halved and boot time reduced by 300% in
most cases.

To take advantage of these performance improvements, you can redeploy your
functions using the Supabase CLI v1.192.5 or later.

Let’s compare the bundle size and boot time using some popular examples.

## Benchmarks#

**Supabase JavaScript Client:**

| **CLI 1.190.0**| **CLI 1.192.5**| **Change**  
---|---|---|---  
Bundle size| 1.487MB| 640.4KB| -232.34%  
Boot time| 275ms| 25ms| -1100%  
  
`  

_24

import { createClient } from 'npm:@supabase/supabase-js@2'

_24

_24

Deno.serve(async (_req) => {

_24

try {

_24

const supabase = createClient(

_24

Deno.env.get('SUPABASE_URL') ?? '',

_24

Deno.env.get('SUPABASE_ANON_KEY') ?? '',

_24

{ global: { headers: { Authorization: req.headers.get('Authorization')! } } }

_24

)

_24

_24

const { data, error } = await supabase.from('countries').select('*')

_24

_24

if (error) {

_24

throw error

_24

}

_24

_24

return new Response(JSON.stringify({ data }), {

_24

headers: { 'Content-Type': 'application/json' },

_24

status: 200,

_24

})

_24

} catch (err) {

_24

return new Response(String(err?.message ?? err), { status: 500 })

_24

}

_24

})

  
`

**OpenAI:**

| **CLI 1.190.0**| **CLI 1.192.5**| **Change**  
---|---|---|---  
Bundle size| 2.533MB| 1.045MB| -242.39%  
Boot time| 459ms| 57ms| -805.26%  
  
`  

_16

import OpenAI from 'npm:[[email protected]](/cdn-cgi/l/email-protection)'

_16

_16

const client = new OpenAI({

_16

apiKey: Deno.env.get('OPEN_AI_KEY'),

_16

})

_16

_16

Deno.serve(async (req) => {

_16

const { query } = await req.json()

_16

_16

const chatCompletion = await client.chat.completions.create({

_16

messages: [{ role: 'user', content: 'Say this is a test' }],

_16

model: 'gpt-3.5-turbo',

_16

})

_16

_16

return new Response(chatCompletion)

_16

})

  
`

**Drizzle / node-postgres:**

| **CLI 1.190.0**| **CLI 1.192.5**|  Change  
---|---|---|---  
Bundle size| 929.5kB| 491.3kB| -189.19%  
Boot time| 301ms| 83ms| -362.65%  
  
`  

_25

import { drizzle } from 'npm:[[email protected]](/cdn-cgi/l/email-
protection)/node-postgres'

_25

import pg from 'npm:[[email protected]](/cdn-cgi/l/email-protection)'

_25

const { Client } = pg

_25

_25

import { pgTable, serial, text, varchar } from 'npm:[[email protected]](/cdn-
cgi/l/email-protection)/pg-core'

_25

_25

export const users = pgTable('users', {

_25

id: serial('id').primaryKey(),

_25

fullName: text('full_name'),

_25

phone: varchar('phone', { length: 256 }),

_25

})

_25

_25

const client = new Client({

_25

connectionString: Deno.env.get('SUPABASE_DB_URL'),

_25

})

_25

_25

await client.connect()

_25

const db = drizzle(client)

_25

_25

Deno.serve(async (req) => {

_25

const allUsers = await db.select().from(users)

_25

console.log(allUsers)

_25

_25

return new Response('ok')

_25

})

  
`

## How did we achieve these gains?#

Let’s dive into the technical details.

### Lazy evaluating dependencies and reducing npm package section size#

We use [eszip format](https://github.com/denoland/eszip) to bundle your
function code and its dependencies when you deploy a function.

This binary format extracts the dependencies a function references from Deno's
module graph and serializes them into a single file. It eliminates network
requests at run time and avoids conflicts between dependencies.

This approach worked reasonably well until we added npm support. When
functions started using npm modules, bundle sizes and boot times increased.

When a function is invoked, Edge Runtime loads the eszip binary for the
function and passes it to a JavaScript worker (ie. isolate). The worker then
loads the necessary modules from the eszip.

In the original implementation, before passing an eszip binary to the worker's
module loader, we first checked the integrity of its contents. Each entry in
it will have a checksum computed with the SHA-256 function immediately
following the body bytes. By reading this and comparing it, we ensure that the
eszip binary isn’t corrupted.

The problem is that calculating a checksum for every entry using SHA-256 is
quite expensive, and we were pre-checking the integrity of all entries at a
time when the worker doesn't even need that particular entry.

It is possible that some items that have been checked for integrity will not
be referenced even if the worker reaches the end of its lifetime and reaches
the end state.

Instead of performing the costly integrity check of all entries before passing
it to the module loader, edge runtime lazily performs the integrity check
whenever there is a request to load a specific entry from the eszip by the
module loader.

This helped to significantly to reduce the boot times.

Another issue was that while serializing npm packages for embedding into eszip
binaries, we used the JSON format. The entries in individual npm packages,
which were already represented as bytes (`Vec<u8>`), were encoded as an array
representation in JSON format (`[255, 216, 255, 224, 0, ...]`) instead of
passing on as bytes, causing the outputs to bloat by up to 2x or more.

We refactored the serialization using the [`rkyv`
crate](https://github.com/rkyv/rkyv) to encode this to lower to the byte
level, which helped reducing the bundle sizes of eszip binaries containing npm
packages.

You can find full details of the implementation in this PR
<https://github.com/supabase/edge-runtime/pull/343>

### Using a more computationally efficient hashing function#

There was a [recent change](https://github.com/denoland/eszip/pull/181) in the
eszip crate, which allowed the configuration of the source checksum.

This allowed us to switch to xxHash-3 over SHA_256 for the source checksums.
Given that the checksums are used to ensure the integrity of sources in eszip,
we could rely on a non-cryptographic hash algorithm that’s more
computationally efficient.

## How to redeploy your functions#

To get the advantage of these optimizations, follow these steps:

  * [Update Supabase CLI](https://supabase.com/docs/guides/cli/getting-started#updating-the-supabase-cli) to version is v1.195.2 or later.
  * Then, redeploy your functions by running `supabase functions deploy [FUNCTION_NAME]`

## Getting Help#

[Supabase Edge Runtime](https://github.com/supabase/edge-runtime) is fully
open-source, and we value community contributions. If you would like to make
any improvements, feel free to dive into the source and [create an
issue](https://github.com/supabase/edge-runtime/issues).

If you have any issues with Edge Functions in your hosted project, please
request support via [superbase.help](http://supabase.help).

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fedge-
functions-faster-
smaller&text=Edge%20Functions%20are%20now%202x%20smaller%20and%20boot%203x%20faster)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fedge-
functions-faster-
smaller&text=Edge%20Functions%20are%20now%202x%20smaller%20and%20boot%203x%20faster)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fedge-
functions-faster-
smaller&t=Edge%20Functions%20are%20now%202x%20smaller%20and%20boot%203x%20faster)

[Last postLocal-first Realtime Apps with Expo and Legend-State23 September
2024](/blog/local-first-expo-legend-state)

[Next postBuilding an Uber Clone with Flutter and Supabase5 September
2024](/blog/flutter-uber-clone)

[functions](/blog/tags/functions)

On this page

  * Benchmarks
  * How did we achieve these gains?
    * Lazy evaluating dependencies and reducing npm package section size
    * Using a more computationally efficient hashing function
  * How to redeploy your functions
  * Getting Help

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fedge-
functions-faster-
smaller&text=Edge%20Functions%20are%20now%202x%20smaller%20and%20boot%203x%20faster)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fedge-
functions-faster-
smaller&text=Edge%20Functions%20are%20now%202x%20smaller%20and%20boot%203x%20faster)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fedge-
functions-faster-
smaller&t=Edge%20Functions%20are%20now%202x%20smaller%20and%20boot%203x%20faster)

## Build in a weekend, scale to millions

[Start your project](https://supabase.com/dashboard)[Request a
demo](/contact/sales)

