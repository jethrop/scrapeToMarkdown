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

Getting Started

  1. [Start with Supabase](/docs/guides/getting-started)
  2.   3. Web app demos
  4.   5. [SvelteKit](/docs/guides/getting-started/tutorials/with-sveltekit)
  6. 

# Build a User Management App with SvelteKit

* * *

This tutorial demonstrates how to build a basic user management app. The app
authenticates and identifies the user, stores their profile information in the
database, and allows the user to log in, update their profile details, and
upload a profile photo. The app uses:

  * [Supabase Database](/docs/guides/database) \- a Postgres database for storing your user data and [Row Level Security](/docs/guides/auth#row-level-security) so data is protected and users can only access their own information.
  * [Supabase Auth](/docs/guides/auth) \- allow users to sign up and log in.
  * [Supabase Storage](/docs/guides/storage) \- users can upload a profile photo.

![Supabase User Management example](/docs/img/user-management-demo.png)

If you get stuck while working through this guide, refer to the [full example
on GitHub](https://github.com/supabase/supabase/tree/master/examples/user-
management/sveltekit-user-management).

## Project setup#

Before we start building we're going to set up our Database and API. This is
as simple as starting a new Project in Supabase and then creating a "schema"
inside the database.

### Create a project#

  1. [Create a new project](https://supabase.com/dashboard) in the Supabase Dashboard.
  2. Enter your project details.
  3. Wait for the new database to launch.

### Set up the database schema#

Now we are going to set up the database schema. We can use the "User
Management Starter" quickstart in the SQL Editor, or you can just copy/paste
the SQL from below and run it yourself.

DashboardSQL

  1. Go to the [SQL Editor](https://supabase.com/dashboard/project/_/sql) page in the Dashboard.
  2. Click **User Management Starter**.
  3. Click **Run**.

You can easily pull the database schema down to your local project by running
the `db pull` command. Read the [local development
docs](/docs/guides/cli/local-development#link-your-project) for detailed
instructions.

`  

_10

supabase link --project-ref <project-id>

_10

# You can get <project-id> from your project's dashboard URL:
https://supabase.com/dashboard/project/<project-id>

_10

supabase db pull

  
`

### Get the API Keys#

Now that you've created some database tables, you are ready to insert data
using the auto-generated API. We just need to get the Project URL and `anon`
key from the API settings.

  1. Go to the [API Settings](https://supabase.com/dashboard/project/_/settings/api) page in the Dashboard.
  2. Find your Project `URL`, `anon`, and `service_role` keys on this page.

## Building the app#

Let's start building the Svelte app from scratch.

### Initialize a Svelte app#

We can use the [SvelteKit Skeleton Project](https://kit.svelte.dev/docs) to
initialize an app called `supabase-sveltekit` (for this tutorial we will be
using TypeScript):

`  

_10

npm create svelte@latest supabase-sveltekit

_10

cd supabase-sveltekit

_10

npm install

  
`

Then install the Supabase client library: [supabase-
js](https://github.com/supabase/supabase-js)

`  

_10

npm install @supabase/supabase-js

  
`

And finally we want to save the environment variables in a `.env`. All we need
are the `SUPABASE_URL` and the `SUPABASE_KEY` key that you copied earlier.

.env

`  

_10

PUBLIC_SUPABASE_URL="YOUR_SUPABASE_URL"

_10

PUBLIC_SUPABASE_ANON_KEY="YOUR_SUPABASE_KEY"

  
`

Optionally, add `src/styles.css` with the [CSS from the
example](https://raw.githubusercontent.com/supabase/supabase/master/examples/user-
management/sveltekit-user-management/src/styles.css).

### Creating a Supabase client for SSR#

The ssr package configures Supabase to use Cookies, which is required for
server-side languages and frameworks.

Install the Supabase packages:

`  

_10

npm install @supabase/ssr @supabase/supabase-js

  
`

Creating a Supabase client with the ssr package automatically configures it to
use Cookies. This means your user's session is available throughout the entire
SvelteKit stack - page, layout, server, hooks.

Add the code below to your `src/hooks.server.ts` to initialize the client on
the server:

src/hooks.server.ts

`  

_53

// src/hooks.server.ts

_53

import { PUBLIC_SUPABASE_URL, PUBLIC_SUPABASE_ANON_KEY } from
'$env/static/public'

_53

import { createServerClient } from '@supabase/ssr'

_53

import type { Handle } from '@sveltejs/kit'

_53

_53

export const handle: Handle = async ({ event, resolve }) => {

_53

event.locals.supabase = createServerClient(PUBLIC_SUPABASE_URL,
PUBLIC_SUPABASE_ANON_KEY, {

_53

cookies: {

_53

getAll: () => event.cookies.getAll(),

_53

/**

_53

* SvelteKit's cookies API requires `path` to be explicitly set in

_53

* the cookie options. Setting `path` to `/` replicates previous/

_53

* standard behavior.

_53

*/

_53

setAll: (cookiesToSet) => {

_53

cookiesToSet.forEach(({ name, value, options }) => {

_53

event.cookies.set(name, value, { ...options, path: '/' })

_53

})

_53

},

_53

},

_53

})

_53

_53

/**

_53

* Unlike `supabase.auth.getSession()`, which returns the session _without_

_53

* validating the JWT, this function also calls `getUser()` to validate the

_53

* JWT before returning the session.

_53

*/

_53

event.locals.safeGetSession = async () => {

_53

const {

_53

data: { session },

_53

} = await event.locals.supabase.auth.getSession()

_53

if (!session) {

_53

return { session: null, user: null }

_53

}

_53

_53

const {

_53

data: { user },

_53

error,

_53

} = await event.locals.supabase.auth.getUser()

_53

if (error) {

_53

// JWT validation has failed

_53

return { session: null, user: null }

_53

}

_53

_53

return { session, user }

_53

}

_53

_53

return resolve(event, {

_53

filterSerializedResponseHeaders(name) {

_53

return name === 'content-range' || name === 'x-supabase-api-version'

_53

},

_53

})

_53

}

  
`

Note that `auth.getSession` reads the auth token and the unencoded session
data from the local storage medium. It _doesn't_ send a request back to the
Supabase Auth server unless the local session is expired.

You should **never** trust the unencoded session data if you're writing server
code, since it could be tampered with by the sender. If you need verified,
trustworthy user data, call `auth.getUser` instead, which always makes a
request to the Auth server to fetch trusted data.

If you are using TypeScript the compiler might complain about
`event.locals.supabase` and `event.locals.safeGetSession`, this can be fixed
by updating your `src/app.d.ts` with the content below:

src/app.d.ts

`  

_18

// src/app.d.ts

_18

_18

import { SupabaseClient, Session } from '@supabase/supabase-js'

_18

_18

declare global {

_18

namespace App {

_18

interface Locals {

_18

supabase: SupabaseClient

_18

safeGetSession(): Promise<{ session: Session | null; user: User | null }>

_18

}

_18

interface PageData {

_18

session: Session | null

_18

user: User | null

_18

}

_18

// interface Error {}

_18

// interface Platform {}

_18

}

_18

}

  
`

Create a new `src/routes/+layout.server.ts` file to handle the session on the
server-side.

src/routes/+layout.server.ts

`  

_12

// src/routes/+layout.server.ts

_12

import type { LayoutServerLoad } from './$types'

_12

_12

export const load: LayoutServerLoad = async ({ locals: { safeGetSession },
cookies }) => {

_12

const { session, user } = await safeGetSession()

_12

_12

return {

_12

session,

_12

user,

_12

cookies: cookies.getAll(),

_12

}

_12

}

  
`

Start your dev server (`npm run dev`) in order to generate the `./$types`
files we are referencing in our project.

Create a new `src/routes/+layout.ts` file to handle the session and the
supabase object on the client-side.

src/routes/+layout.ts

`  

_36

// src/routes/+layout.ts

_36

import { createBrowserClient, createServerClient, isBrowser } from
'@supabase/ssr'

_36

import { PUBLIC_SUPABASE_ANON_KEY, PUBLIC_SUPABASE_URL } from
'$env/static/public'

_36

import type { LayoutLoad } from './$types'

_36

_36

export const load: LayoutLoad = async ({ fetch, data, depends }) => {

_36

depends('supabase:auth')

_36

_36

const supabase = isBrowser()

_36

? createBrowserClient(PUBLIC_SUPABASE_URL, PUBLIC_SUPABASE_ANON_KEY, {

_36

global: {

_36

fetch,

_36

},

_36

})

_36

: createServerClient(PUBLIC_SUPABASE_URL, PUBLIC_SUPABASE_ANON_KEY, {

_36

global: {

_36

fetch,

_36

},

_36

cookies: {

_36

getAll() {

_36

return data.cookies

_36

},

_36

},

_36

})

_36

_36

/**

_36

* It's fine to use `getSession` here, because on the client, `getSession` is

_36

* safe, and on the server, it reads `session` from the `LayoutData`, which

_36

* safely checked the session using `safeGetSession`.

_36

*/

_36

const {

_36

data: { session },

_36

} = await supabase.auth.getSession()

_36

_36

return { supabase, session }

_36

}

  
`

Update your `src/routes/+layout.svelte`:

src/routes/+layout.svelte

`  

_29

<!-- src/routes/+layout.svelte -->

_29

<script lang="ts">

_29

import '../styles.css'

_29

import { invalidate } from '$app/navigation'

_29

import { onMount } from 'svelte'

_29

_29

export let data

_29

_29

let { supabase, session } = data

_29

$: ({ supabase, session } = data)

_29

_29

onMount(() => {

_29

const { data } = supabase.auth.onAuthStateChange((event, newSession) => {

_29

if (newSession?.expires_at !== session?.expires_at) {

_29

invalidate('supabase:auth')

_29

}

_29

})

_29

_29

return () => data.subscription.unsubscribe()

_29

})

_29

</script>

_29

_29

<svelte:head>

_29

<title>User Management</title>

_29

</svelte:head>

_29

_29

<div class="container" style="padding: 50px 0 100px 0">

_29

<slot />

_29

</div>

  
`

## Set up a login page#

Create a magic link login/signup page for your application:

src/routes/+page.svelte

`  

_54

<!-- src/routes/+page.svelte -->

_54

<script lang="ts">

_54

import { enhance } from '$app/forms'

_54

import type { ActionData, SubmitFunction } from './$types.js'

_54

_54

export let form: ActionData;

_54

_54

let loading = false

_54

_54

const handleSubmit: SubmitFunction = () => {

_54

loading = true

_54

return async ({ update }) => {

_54

update()

_54

loading = false

_54

}

_54

}

_54

</script>

_54

_54

<svelte:head>

_54

<title>User Management</title>

_54

</svelte:head>

_54

_54

<form class="row flex flex-center" method="POST" use:enhance={handleSubmit}>

_54

<div class="col-6 form-widget">

_54

<h1 class="header">Supabase + SvelteKit</h1>

_54

<p class="description">Sign in via magic link with your email below</p>

_54

{#if form?.message !== undefined}

_54

<div class="success {form?.success ? '' : 'fail'}">

_54

{form?.message}

_54

</div>

_54

{/if}

_54

<div>

_54

<label for="email">Email address</label>

_54

<input

_54

id="email"

_54

name="email"

_54

class="inputField"

_54

type="email"

_54

placeholder="Your email"

_54

value={form?.email ?? ''}

_54

/>

_54

</div>

_54

{#if form?.errors?.email}

_54

<span class="flex items-center text-sm error">

_54

{form?.errors?.email}

_54

</span>

_54

{/if}

_54

<div>

_54

<button class="button primary block">

_54

{ loading ? 'Loading' : 'Send magic link' }

_54

</button>

_54

</div>

_54

</div>

_54

</form>

  
`

Create a `src/routes/+page.server.ts` file that will handle our magic link
form when submitted.

src/routes/+page.server.ts

`  

_46

// src/routes/+page.server.ts

_46

import { fail, redirect } from '@sveltejs/kit'

_46

import type { Actions, PageServerLoad } from './$types'

_46

_46

export const load: PageServerLoad = async ({ url, locals: { safeGetSession }
}) => {

_46

const { session } = await safeGetSession()

_46

_46

// if the user is already logged in return them to the account page

_46

if (session) {

_46

redirect(303, '/account')

_46

}

_46

_46

return { url: url.origin }

_46

}

_46

_46

export const actions: Actions = {

_46

default: async (event) => {

_46

const {

_46

url,

_46

request,

_46

locals: { supabase },

_46

} = event

_46

const formData = await request.formData()

_46

const email = formData.get('email') as string

_46

const validEmail = /^[\w-\.+]+@([\w-]+\.)+[\w-]{2,8}$/.test(email)

_46

_46

if (!validEmail) {

_46

return fail(400, { errors: { email: 'Please enter a valid email address' },
email })

_46

}

_46

_46

const { error } = await supabase.auth.signInWithOtp({ email })

_46

_46

if (error) {

_46

return fail(400, {

_46

success: false,

_46

email,

_46

message: `There was an issue, Please contact support.`,

_46

})

_46

}

_46

_46

return {

_46

success: true,

_46

message: 'Please check your email for a magic link to log into the website.',

_46

}

_46

},

_46

}

  
`

### Email template#

Change the email template to support a server-side authentication flow.

Before we proceed, let's change the email template to support sending a token
hash:

  * Go to the [Auth templates](/dashboard/project/_/auth/templates) page in your dashboard.
  * Select `Confirm signup` template.
  * Change `{{ .ConfirmationURL }}` to `{{ .SiteURL }}/auth/confirm?token_hash={{ .TokenHash }}&type=email`.
  * Repeat the previous step for `Magic link` template.

Did you know? You could also customize emails sent out to new users, including
the email's looks, content, and query parameters. Check out the [settings of
your project](/dashboard/project/_/auth/templates).

### Confirmation endpoint#

As we are working in a server-side rendering (SSR) environment, it is
necessary to create a server endpoint responsible for exchanging the
`token_hash` for a session.

In the following code snippet, we perform the following steps:

  * Retrieve the `token_hash` sent back from the Supabase Auth server using the `token_hash` query parameter.
  * Exchange this `token_hash` for a session, which we store in storage (in this case, cookies).
  * Finally, the user is redirected to the `account` page or the `error` page.

src/routes/auth/confirm/+server.ts

`  

_32

// src/routes/auth/confirm/+server.ts

_32

import type { EmailOtpType } from '@supabase/supabase-js'

_32

import { redirect } from '@sveltejs/kit'

_32

_32

import type { RequestHandler } from './$types'

_32

_32

export const GET: RequestHandler = async ({ url, locals: { supabase } }) => {

_32

const token_hash = url.searchParams.get('token_hash')

_32

const type = url.searchParams.get('type') as EmailOtpType | null

_32

const next = url.searchParams.get('next') ?? '/account'

_32

_32

/**

_32

* Clean up the redirect URL by deleting the Auth flow parameters.

_32

*

_32

* `next` is preserved for now, because it's needed in the error case.

_32

*/

_32

const redirectTo = new URL(url)

_32

redirectTo.pathname = next

_32

redirectTo.searchParams.delete('token_hash')

_32

redirectTo.searchParams.delete('type')

_32

_32

if (token_hash && type) {

_32

const { error } = await supabase.auth.verifyOtp({ type, token_hash })

_32

if (!error) {

_32

redirectTo.searchParams.delete('next')

_32

redirect(303, redirectTo)

_32

}

_32

}

_32

_32

redirectTo.pathname = '/auth/error'

_32

redirect(303, redirectTo)

_32

}

  
`

### Authentication error page#

If there is an error with confirming the token you will be redirect to this
error page.

src/routes/auth/error/+page.svelte

`  

_10

<p>Login error</p>

  
`

### Account page#

After a user is signed in, they need to be able to edit their profile details
and manage their account. Create a new `src/routes/account/+page.svelte` file
with the content below.

src/routes/account/+page.svelte

`  

_78

<!-- src/routes/account/+page.svelte -->

_78

<script lang="ts">

_78

import { enhance } from '$app/forms';

_78

import type { SubmitFunction } from '@sveltejs/kit';

_78

_78

export let data

_78

export let form

_78

_78

let { session, supabase, profile } = data

_78

$: ({ session, supabase, profile } = data)

_78

_78

let profileForm: HTMLFormElement

_78

let loading = false

_78

let fullName: string = profile?.full_name ?? ''

_78

let username: string = profile?.username ?? ''

_78

let website: string = profile?.website ?? ''

_78

let avatarUrl: string = profile?.avatar_url ?? ''

_78

_78

const handleSubmit: SubmitFunction = () => {

_78

loading = true

_78

return async () => {

_78

loading = false

_78

}

_78

}

_78

_78

const handleSignOut: SubmitFunction = () => {

_78

loading = true

_78

return async ({ update }) => {

_78

loading = false

_78

update()

_78

}

_78

}

_78

</script>

_78

_78

<div class="form-widget">

_78

<form

_78

class="form-widget"

_78

method="post"

_78

action="?/update"

_78

use:enhance={handleSubmit}

_78

bind:this={profileForm}

_78

>

_78

<div>

_78

<label for="email">Email</label>

_78

<input id="email" type="text" value={session.user.email} disabled />

_78

</div>

_78

_78

<div>

_78

<label for="fullName">Full Name</label>

_78

<input id="fullName" name="fullName" type="text" value={form?.fullName ??
fullName} />

_78

</div>

_78

_78

<div>

_78

<label for="username">Username</label>

_78

<input id="username" name="username" type="text" value={form?.username ??
username} />

_78

</div>

_78

_78

<div>

_78

<label for="website">Website</label>

_78

<input id="website" name="website" type="url" value={form?.website ?? website}
/>

_78

</div>

_78

_78

<div>

_78

<input

_78

type="submit"

_78

class="button block primary"

_78

value={loading ? 'Loading...' : 'Update'}

_78

disabled={loading}

_78

/>

_78

</div>

_78

</form>

_78

_78

<form method="post" action="?/signout" use:enhance={handleSignOut}>

_78

<div>

_78

<button class="button block" disabled={loading}>Sign Out</button>

_78

</div>

_78

</form>

_78

</div>

  
`

Now create the associated `src/routes/account/+page.server.ts` file that will
handle loading our data from the server through the `load` function and handle
all our form actions through the `actions` object.

`  

_62

import { fail, redirect } from '@sveltejs/kit'

_62

import type { Actions, PageServerLoad } from './$types'

_62

_62

export const load: PageServerLoad = async ({ locals: { supabase,
safeGetSession } }) => {

_62

const { session } = await safeGetSession()

_62

_62

if (!session) {

_62

redirect(303, '/')

_62

}

_62

_62

const { data: profile } = await supabase

_62

.from('profiles')

_62

.select(`username, full_name, website, avatar_url`)

_62

.eq('id', session.user.id)

_62

.single()

_62

_62

return { session, profile }

_62

}

_62

_62

export const actions: Actions = {

_62

update: async ({ request, locals: { supabase, safeGetSession } }) => {

_62

const formData = await request.formData()

_62

const fullName = formData.get('fullName') as string

_62

const username = formData.get('username') as string

_62

const website = formData.get('website') as string

_62

const avatarUrl = formData.get('avatarUrl') as string

_62

_62

const { session } = await safeGetSession()

_62

_62

const { error } = await supabase.from('profiles').upsert({

_62

id: session?.user.id,

_62

full_name: fullName,

_62

username,

_62

website,

_62

avatar_url: avatarUrl,

_62

updated_at: new Date(),

_62

})

_62

_62

if (error) {

_62

return fail(500, {

_62

fullName,

_62

username,

_62

website,

_62

avatarUrl,

_62

})

_62

}

_62

_62

return {

_62

fullName,

_62

username,

_62

website,

_62

avatarUrl,

_62

}

_62

},

_62

signout: async ({ locals: { supabase, safeGetSession } }) => {

_62

const { session } = await safeGetSession()

_62

if (session) {

_62

await supabase.auth.signOut()

_62

redirect(303, '/')

_62

}

_62

},

_62

}

  
`

### Launch!#

Now that we have all the pages in place, run this in a terminal window:

`  

_10

npm run dev

  
`

And then open the browser to [localhost:5173](http://localhost:5173) and you
should see the completed app.

![Supabase Svelte](/docs/img/supabase-svelte-demo.png)

## Bonus: Profile photos#

Every Supabase project is configured with [Storage](/docs/guides/storage) for
managing large files like photos and videos.

### Create an upload widget#

Let's create an avatar for the user so that they can upload a profile photo.
We can start by creating a new component called `Avatar.svelte` in the
`src/routes/account` directory:

src/routes/account/Avatar.svelte

`  

_94

<!-- src/routes/account/Avatar.svelte -->

_94

<script lang="ts">

_94

import type { SupabaseClient } from '@supabase/supabase-js'

_94

import { createEventDispatcher } from 'svelte'

_94

_94

export let size = 10

_94

export let url: string

_94

export let supabase: SupabaseClient

_94

_94

let avatarUrl: string | null = null

_94

let uploading = false

_94

let files: FileList

_94

_94

const dispatch = createEventDispatcher()

_94

_94

const downloadImage = async (path: string) => {

_94

try {

_94

const { data, error } = await supabase.storage.from('avatars').download(path)

_94

_94

if (error) {

_94

throw error

_94

}

_94

_94

const url = URL.createObjectURL(data)

_94

avatarUrl = url

_94

} catch (error) {

_94

if (error instanceof Error) {

_94

console.log('Error downloading image: ', error.message)

_94

}

_94

}

_94

}

_94

_94

const uploadAvatar = async () => {

_94

try {

_94

uploading = true

_94

_94

if (!files || files.length === 0) {

_94

throw new Error('You must select an image to upload.')

_94

}

_94

_94

const file = files[0]

_94

const fileExt = file.name.split('.').pop()

_94

const filePath = `${Math.random()}.${fileExt}`

_94

_94

const { error } = await supabase.storage.from('avatars').upload(filePath,
file)

_94

_94

if (error) {

_94

throw error

_94

}

_94

_94

url = filePath

_94

setTimeout(() => {

_94

dispatch('upload')

_94

}, 100)

_94

} catch (error) {

_94

if (error instanceof Error) {

_94

alert(error.message)

_94

}

_94

} finally {

_94

uploading = false

_94

}

_94

}

_94

_94

$: if (url) downloadImage(url)

_94

</script>

_94

_94

<div>

_94

{#if avatarUrl}

_94

<img

_94

src={avatarUrl}

_94

alt={avatarUrl ? 'Avatar' : 'No image'}

_94

class="avatar image"

_94

style="height: {size}em; width: {size}em;"

_94

/>

_94

{:else}

_94

<div class="avatar no-image" style="height: {size}em; width: {size}em;" />

_94

{/if}

_94

<input type="hidden" name="avatarUrl" value={url} />

_94

_94

<div style="width: {size}em;">

_94

<label class="button primary block" for="single">

_94

{uploading ? 'Uploading ...' : 'Upload'}

_94

</label>

_94

<input

_94

style="visibility: hidden; position:absolute;"

_94

type="file"

_94

id="single"

_94

accept="image/*"

_94

bind:files

_94

on:change={uploadAvatar}

_94

disabled={uploading}

_94

/>

_94

</div>

_94

</div>

  
`

### Add the new widget#

And then we can add the widget to the Account page:

src/routes/account/+page.svelte

`  

_27

<!-- src/routes/account/+page.svelte -->

_27

<script lang="ts">

_27

// Import the new component

_27

import Avatar from './Avatar.svelte'

_27

</script>

_27

_27

<div class="form-widget">

_27

<form

_27

class="form-widget"

_27

method="post"

_27

action="?/update"

_27

use:enhance={handleSubmit}

_27

bind:this={profileForm}

_27

>

_27

<!-- Add to body -->

_27

<Avatar

_27

{supabase}

_27

bind:url={avatarUrl}

_27

size={10}

_27

on:upload={() => {

_27

profileForm.requestSubmit();

_27

}}

_27

/>

_27

_27

<!-- Other form elements -->

_27

</form>

_27

</div>

  
`

At this stage you have a fully functional application!

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/content/guides/getting-
started/tutorials/with-sveltekit.mdx)

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

