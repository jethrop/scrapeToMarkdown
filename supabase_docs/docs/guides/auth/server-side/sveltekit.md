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

Auth

  1. Auth
  2.   3. More
  4.   5. [Server-Side Rendering](/docs/guides/auth/server-side)
  6.   7. [SvelteKit guide](/docs/guides/auth/server-side/sveltekit)
  8. 

# Setting up Server-Side Auth for SvelteKit

* * *

Set up Server-Side Auth to use cookie-based authentication with SvelteKit.

1

### Install Supabase packages

Install the `@supabase/supabase-js` package and the helper `@supabase/ssr`
package.

`  

_10

npm install @supabase/supabase-js @supabase/ssr

  
`

2

### Set up environment variables

Create a `.env.local` file in your project root directory.

Fill in your `PUBLIC_SUPABASE_URL` and `PUBLIC_SUPABASE_ANON_KEY`:

###### Project URL

Loading...

###### Anon key

Loading...

.env.local

`  

_10

PUBLIC_SUPABASE_URL=<your_supabase_project_url>

_10

PUBLIC_SUPABASE_ANON_KEY=<your_supabase_anon_key>

  
`

3

### Set up server-side hooks

Set up server-side hooks in `src/hooks.server.ts`. The hooks:

  * Create a request-specific Supabase client, using the user credentials from the request cookie. This client is used for server-only code.
  * Check user authentication.
  * Guard protected pages.

src/hooks.server.ts

`  

_81

import { createServerClient } from '@supabase/ssr'

_81

import { type Handle, redirect } from '@sveltejs/kit'

_81

import { sequence } from '@sveltejs/kit/hooks'

_81

_81

import { PUBLIC_SUPABASE_URL, PUBLIC_SUPABASE_ANON_KEY } from
'$env/static/public'

_81

_81

const supabase: Handle = async ({ event, resolve }) => {

_81

/**

_81

* Creates a Supabase client specific to this server request.

_81

*

_81

* The Supabase client gets the Auth token from the request cookies.

_81

*/

_81

event.locals.supabase = createServerClient(PUBLIC_SUPABASE_URL,
PUBLIC_SUPABASE_ANON_KEY, {

_81

cookies: {

_81

getAll: () => event.cookies.getAll(),

_81

/**

_81

* SvelteKit's cookies API requires `path` to be explicitly set in

_81

* the cookie options. Setting `path` to `/` replicates previous/

_81

* standard behavior.

_81

*/

_81

setAll: (cookiesToSet) => {

_81

cookiesToSet.forEach(({ name, value, options }) => {

_81

event.cookies.set(name, value, { ...options, path: '/' })

_81

})

_81

},

_81

},

_81

})

_81

_81

/**

_81

* Unlike `supabase.auth.getSession()`, which returns the session _without_

_81

* validating the JWT, this function also calls `getUser()` to validate the

_81

* JWT before returning the session.

_81

*/

_81

event.locals.safeGetSession = async () => {

_81

const {

_81

data: { session },

_81

} = await event.locals.supabase.auth.getSession()

_81

if (!session) {

_81

return { session: null, user: null }

_81

}

_81

_81

const {

_81

data: { user },

_81

error,

_81

} = await event.locals.supabase.auth.getUser()

_81

if (error) {

_81

// JWT validation has failed

_81

return { session: null, user: null }

_81

}

_81

_81

return { session, user }

_81

}

_81

_81

return resolve(event, {

_81

filterSerializedResponseHeaders(name) {

_81

/**

_81

* Supabase libraries use the `content-range` and `x-supabase-api-version`

_81

* headers, so we need to tell SvelteKit to pass it through.

_81

*/

_81

return name === 'content-range' || name === 'x-supabase-api-version'

_81

},

_81

})

_81

}

_81

_81

const authGuard: Handle = async ({ event, resolve }) => {

_81

const { session, user } = await event.locals.safeGetSession()

_81

event.locals.session = session

_81

event.locals.user = user

_81

_81

if (!event.locals.session && event.url.pathname.startsWith('/private')) {

_81

redirect(303, '/auth')

_81

}

_81

_81

if (event.locals.session && event.url.pathname === '/auth') {

_81

redirect(303, '/private')

_81

}

_81

_81

return resolve(event)

_81

}

_81

_81

export const handle: Handle = sequence(supabase, authGuard)

  
`

4

### Create TypeScript definitions

To prevent TypeScript errors, add type definitions for the new `event.locals`
properties.

src/app.d.ts

`  

_20

import type { Session, SupabaseClient, User } from '@supabase/supabase-js'

_20

_20

declare global {

_20

namespace App {

_20

// interface Error {}

_20

interface Locals {

_20

supabase: SupabaseClient

_20

safeGetSession: () => Promise<{ session: Session | null; user: User | null }>

_20

session: Session | null

_20

user: User | null

_20

}

_20

interface PageData {

_20

session: Session | null

_20

}

_20

// interface PageState {}

_20

// interface Platform {}

_20

}

_20

}

_20

_20

export {}

  
`

5

### Create a Supabase client in your root layout

Create a Supabase client in your root `+layout.ts`. This client can be used to
access Supabase from the client or the server. In order to get access to the
Auth token on the server, use a `+layout.server.ts` file to pass in the
session from `event.locals`.

src/routes/+layout.ts

src/routes/+layout.server.ts

`  

_43

import { createBrowserClient, createServerClient, isBrowser } from
'@supabase/ssr'

_43

import { PUBLIC_SUPABASE_ANON_KEY, PUBLIC_SUPABASE_URL } from
'$env/static/public'

_43

import type { LayoutLoad } from './$types'

_43

_43

export const load: LayoutLoad = async ({ data, depends, fetch }) => {

_43

/**

_43

* Declare a dependency so the layout can be invalidated, for example, on

_43

* session refresh.

_43

*/

_43

depends('supabase:auth')

_43

_43

const supabase = isBrowser()

_43

? createBrowserClient(PUBLIC_SUPABASE_URL, PUBLIC_SUPABASE_ANON_KEY, {

_43

global: {

_43

fetch,

_43

},

_43

})

_43

: createServerClient(PUBLIC_SUPABASE_URL, PUBLIC_SUPABASE_ANON_KEY, {

_43

global: {

_43

fetch,

_43

},

_43

cookies: {

_43

getAll() {

_43

return data.cookies

_43

},

_43

},

_43

})

_43

_43

/**

_43

* It's fine to use `getSession` here, because on the client, `getSession` is

_43

* safe, and on the server, it reads `session` from the `LayoutData`, which

_43

* safely checked the session using `safeGetSession`.

_43

*/

_43

const {

_43

data: { session },

_43

} = await supabase.auth.getSession()

_43

_43

const {

_43

data: { user },

_43

} = await supabase.auth.getUser()

_43

_43

return { session, supabase, user }

_43

}

  
`

6

### Listen to Auth events

Set up a listener for Auth events on the client, to handle session refreshes
and signouts.

src/routes/+layout.svelte

`  

_19

<script>

_19

import { invalidate } from '$app/navigation';

_19

import { onMount } from 'svelte';

_19

_19

export let data;

_19

$: ({ session, supabase } = data);

_19

_19

onMount(() => {

_19

const { data } = supabase.auth.onAuthStateChange((_, newSession) => {

_19

if (newSession?.expires_at !== session?.expires_at) {

_19

invalidate('supabase:auth');

_19

}

_19

});

_19

_19

return () => data.subscription.unsubscribe();

_19

});

_19

</script>

_19

_19

<slot />

  
`

7

### Create your first page

Create your first page. This example page calls Supabase from the server to
get a list of countries from the database.

This is an example of a public page that uses publicly readable data.

To populate your database, run the [countries
quickstart](/dashboard/project/_/sql/quickstarts) from your dashboard.

src/routes/+page.server.ts

src/routes/+page.svelte

`  

_10

import type { PageServerLoad } from './$types'

_10

_10

export const load: PageServerLoad = async ({ locals: { supabase } }) => {

_10

const { data: countries } = await
supabase.from('countries').select('name').limit(5).order('name')

_10

return { countries: countries ?? [] }

_10

}

  
`

8

### Change the Auth confirmation path

If you have email confirmation turned on (the default), a new user will
receive an email confirmation after signing up.

Change the email template to support a server-side authentication flow.

Go to the [Auth
templates](https://supabase.com/dashboard/project/_/auth/templates) page in
your dashboard. In the `Confirm signup` template, change `{{ .ConfirmationURL
}}` to `{{ .SiteURL }}/auth/confirm?token_hash={{ .TokenHash }}&type=email`.

9

### Create a login page

Next, create a login page to let users sign up and log in.

src/routes/auth/+page.server.ts

src/routes/auth/+page.svelte

src/routes/auth/+layout.svelte

src/routes/auth/error/+page.svelte

`  

_32

import { redirect } from '@sveltejs/kit'

_32

_32

import type { Actions } from './$types'

_32

_32

export const actions: Actions = {

_32

signup: async ({ request, locals: { supabase } }) => {

_32

const formData = await request.formData()

_32

const email = formData.get('email') as string

_32

const password = formData.get('password') as string

_32

_32

const { error } = await supabase.auth.signUp({ email, password })

_32

if (error) {

_32

console.error(error)

_32

redirect(303, '/auth/error')

_32

} else {

_32

redirect(303, '/')

_32

}

_32

},

_32

login: async ({ request, locals: { supabase } }) => {

_32

const formData = await request.formData()

_32

const email = formData.get('email') as string

_32

const password = formData.get('password') as string

_32

_32

const { error } = await supabase.auth.signInWithPassword({ email, password })

_32

if (error) {

_32

console.error(error)

_32

redirect(303, '/auth/error')

_32

} else {

_32

redirect(303, '/private')

_32

}

_32

},

_32

}

  
`

10

### Create the signup confirmation route

Finish the signup flow by creating the API route to handle email verification.

src/routes/auth/confirm/+server.ts

`  

_31

import type { EmailOtpType } from '@supabase/supabase-js'

_31

import { redirect } from '@sveltejs/kit'

_31

_31

import type { RequestHandler } from './$types'

_31

_31

export const GET: RequestHandler = async ({ url, locals: { supabase } }) => {

_31

const token_hash = url.searchParams.get('token_hash')

_31

const type = url.searchParams.get('type') as EmailOtpType | null

_31

const next = url.searchParams.get('next') ?? '/'

_31

_31

/**

_31

* Clean up the redirect URL by deleting the Auth flow parameters.

_31

*

_31

* `next` is preserved for now, because it's needed in the error case.

_31

*/

_31

const redirectTo = new URL(url)

_31

redirectTo.pathname = next

_31

redirectTo.searchParams.delete('token_hash')

_31

redirectTo.searchParams.delete('type')

_31

_31

if (token_hash && type) {

_31

const { error } = await supabase.auth.verifyOtp({ type, token_hash })

_31

if (!error) {

_31

redirectTo.searchParams.delete('next')

_31

redirect(303, redirectTo)

_31

}

_31

}

_31

_31

redirectTo.pathname = '/auth/error'

_31

redirect(303, redirectTo)

_31

}

  
`

11

### Create private routes

Create private routes that can only be accessed by authenticated users. The
routes in the `private` directory are protected by the route guard in
`hooks.server.ts`.

To ensure that `hooks.server.ts` runs for every nested path, put a
`+layout.server.ts` file in the `private` directory. This file can be empty,
but must exist to protect routes that don't have their own
`+layout|page.server.ts`.

src/routes/private/+layout.server.ts

src/routes/private/+layout.svelte

SQL

src/routes/private/+page.server.ts

src/routes/private/+page.svelte

`  

_10

/**

_10

* This file is necessary to ensure protection of all routes in the `private`

_10

* directory. It makes the routes in this directory _dynamic_ routes, which

_10

* send a server request, and thus trigger `hooks.server.ts`.

_10

**/

  
`

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/content/guides/auth/server-
side/sveltekit.mdx)

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

