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
  4.   5. [Svelte](/docs/guides/getting-started/tutorials/with-svelte)
  6. 

# Build a User Management App with Svelte

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
management/svelte-user-management).

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

We can use the Vite Svelte TypeScript Template to initialize an app called
`supabase-svelte`:

`  

_10

npm create vite@latest supabase-svelte -- --template svelte-ts

_10

cd supabase-svelte

_10

npm install

  
`

Then let's install the only additional dependency: [supabase-
js](https://github.com/supabase/supabase-js)

`  

_10

npm install @supabase/supabase-js

  
`

And finally we want to save the environment variables in a `.env`. All we need
are the API URL and the `anon` key that you copied earlier.

.env

`  

_10

VITE_SUPABASE_URL=YOUR_SUPABASE_URL

_10

VITE_SUPABASE_ANON_KEY=YOUR_SUPABASE_ANON_KEY

  
`

Now that we have the API credentials in place, let's create a helper file to
initialize the Supabase client. These variables will be exposed on the
browser, and that's completely fine since we have [Row Level
Security](/docs/guides/auth#row-level-security) enabled on our Database.

src/supabaseClient.ts

`  

_10

import { createClient } from '@supabase/supabase-js'

_10

_10

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL

_10

const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

_10

_10

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

  
`

### App styling (optional)#

An optional step is to update the CSS file `src/app.css` to make the app look
nice. You can find the full contents of this file
[here](https://raw.githubusercontent.com/supabase/supabase/master/examples/user-
management/svelte-user-management/src/app.css).

### Set up a login component#

Let's set up a Svelte component to manage logins and sign ups. We'll use Magic
Links, so users can sign in with their email without using passwords.

src/lib/Auth.svelte

`  

_45

<script lang="ts">

_45

import { supabase } from '../supabaseClient'

_45

_45

let loading = false

_45

let email = ''

_45

_45

const handleLogin = async () => {

_45

try {

_45

loading = true

_45

const { error } = await supabase.auth.signInWithOtp({ email })

_45

if (error) throw error

_45

alert('Check your email for login link!')

_45

} catch (error) {

_45

if (error instanceof Error) {

_45

alert(error.message)

_45

}

_45

} finally {

_45

loading = false

_45

}

_45

}

_45

</script>

_45

_45

<div class="row flex-center flex">

_45

<div class="col-6 form-widget" aria-live="polite">

_45

<h1 class="header">Supabase + Svelte</h1>

_45

<p class="description">Sign in via magic link with your email below</p>

_45

<form class="form-widget" on:submit|preventDefault="{handleLogin}">

_45

<div>

_45

<label for="email">Email</label>

_45

<input

_45

id="email"

_45

class="inputField"

_45

type="email"

_45

placeholder="Your email"

_45

bind:value="{email}"

_45

/>

_45

</div>

_45

<div>

_45

<button type="submit" class="button block" aria-live="polite"
disabled="{loading}">

_45

<span>{loading ? 'Loading' : 'Send magic link'}</span>

_45

</button>

_45

</div>

_45

</form>

_45

</div>

_45

</div>

  
`

### Account page#

After a user is signed in we can allow them to edit their profile details and
manage their account. Let's create a new component for that called
`Account.svelte`.

src/lib/Account.svelte

`  

_89

<script lang="ts">

_89

import { onMount } from 'svelte'

_89

import type { AuthSession } from '@supabase/supabase-js'

_89

import { supabase } from '../supabaseClient'

_89

_89

export let session: AuthSession

_89

_89

let loading = false

_89

let username: string | null = null

_89

let website: string | null = null

_89

let avatarUrl: string | null = null

_89

_89

onMount(() => {

_89

getProfile()

_89

})

_89

_89

const getProfile = async () => {

_89

try {

_89

loading = true

_89

const { user } = session

_89

_89

const { data, error, status } = await supabase

_89

.from('profiles')

_89

.select('username, website, avatar_url')

_89

.eq('id', user.id)

_89

.single()

_89

_89

if (error && status !== 406) throw error

_89

_89

if (data) {

_89

username = data.username

_89

website = data.website

_89

avatarUrl = data.avatar_url

_89

}

_89

} catch (error) {

_89

if (error instanceof Error) {

_89

alert(error.message)

_89

}

_89

} finally {

_89

loading = false

_89

}

_89

}

_89

_89

const updateProfile = async () => {

_89

try {

_89

loading = true

_89

const { user } = session

_89

_89

const updates = {

_89

id: user.id,

_89

username,

_89

website,

_89

avatar_url: avatarUrl,

_89

updated_at: new Date().toISOString(),

_89

}

_89

_89

const { error } = await supabase.from('profiles').upsert(updates)

_89

_89

if (error) {

_89

throw error

_89

}

_89

} catch (error) {

_89

if (error instanceof Error) {

_89

alert(error.message)

_89

}

_89

} finally {

_89

loading = false

_89

}

_89

}

_89

</script>

_89

_89

<form on:submit|preventDefault="{updateProfile}" class="form-widget">

_89

<div>Email: {session.user.email}</div>

_89

<div>

_89

<label for="username">Name</label>

_89

<input id="username" type="text" bind:value="{username}" />

_89

</div>

_89

<div>

_89

<label for="website">Website</label>

_89

<input id="website" type="text" bind:value="{website}" />

_89

</div>

_89

<div>

_89

<button type="submit" class="button primary block" disabled="{loading}">

_89

{loading ? 'Saving ...' : 'Update profile'}

_89

</button>

_89

</div>

_89

<button type="button" class="button block" on:click={() =>
supabase.auth.signOut()}> Sign Out

_89

</button>

_89

</form>

  
`

### Launch!#

Now that we have all the components in place, let's update `App.svelte`:

src/App.svelte

`  

_27

<script lang="ts">

_27

import { onMount } from 'svelte'

_27

import { supabase } from './supabaseClient'

_27

import type { AuthSession } from '@supabase/supabase-js'

_27

import Account from './lib/Account.svelte'

_27

import Auth from './lib/Auth.svelte'

_27

_27

let session: AuthSession | null

_27

_27

onMount(() => {

_27

supabase.auth.getSession().then(({ data }) => {

_27

session = data.session

_27

})

_27

_27

supabase.auth.onAuthStateChange((_event, _session) => {

_27

session = _session

_27

})

_27

})

_27

</script>

_27

_27

<div class="container" style="padding: 50px 0 100px 0">

_27

{#if !session}

_27

<Auth />

_27

{:else}

_27

<Account {session} />

_27

{/if}

_27

</div>

  
`

Once that's done, run this in a terminal window:

`  

_10

npm run dev

  
`

And then open the browser to [localhost:5173](http://localhost:5173) and you
should see the completed app.

> ⚠️ WARNING: Svelte uses Vite and the default port is `5173`, Supabase uses
> `port 3000`. To change the redirection port for supabase go to:
> `Authentication > Settings` and change the `Site Url` to
> `http://localhost:5173/`

![Supabase Svelte](/docs/img/supabase-svelte-demo.png)

## Bonus: Profile photos#

Every Supabase project is configured with [Storage](/docs/guides/storage) for
managing large files like photos and videos.

### Create an upload widget#

Let's create an avatar for the user so that they can upload a profile photo.
We can start by creating a new component:

src/lib/Avatar.svelte

`  

_83

<script lang="ts">

_83

import { createEventDispatcher } from 'svelte'

_83

import { supabase } from '../supabaseClient'

_83

_83

export let size: number

_83

export let url: string | null = null

_83

_83

let avatarUrl: string | null = null

_83

let uploading = false

_83

let files: FileList

_83

_83

const dispatch = createEventDispatcher()

_83

_83

const downloadImage = async (path: string) => {

_83

try {

_83

const { data, error } = await supabase.storage.from('avatars').download(path)

_83

_83

if (error) {

_83

throw error

_83

}

_83

_83

const url = URL.createObjectURL(data)

_83

avatarUrl = url

_83

} catch (error) {

_83

if (error instanceof Error) {

_83

console.log('Error downloading image: ', error.message)

_83

}

_83

}

_83

}

_83

_83

const uploadAvatar = async () => {

_83

try {

_83

uploading = true

_83

_83

if (!files || files.length === 0) {

_83

throw new Error('You must select an image to upload.')

_83

}

_83

_83

const file = files[0]

_83

const fileExt = file.name.split('.').pop()

_83

const filePath = `${Math.random()}.${fileExt}`

_83

_83

const { error } = await supabase.storage.from('avatars').upload(filePath,
file)

_83

_83

if (error) {

_83

throw error

_83

}

_83

_83

url = filePath

_83

dispatch('upload')

_83

} catch (error) {

_83

if (error instanceof Error) {

_83

alert(error.message)

_83

}

_83

} finally {

_83

uploading = false

_83

}

_83

}

_83

_83

$: if (url) downloadImage(url)

_83

</script>

_83

_83

<div style="width: {size}px" aria-live="polite">

_83

{#if avatarUrl} <img src={avatarUrl} alt={avatarUrl ? 'Avatar' : 'No image'}
class="avatar image"

_83

style="height: {size}px, width: {size}px" /> {:else}

_83

<div class="avatar no-image" style="height: {size}px, width: {size}px" />

_83

{/if}

_83

<div style="width: {size}px">

_83

<label class="button primary block" for="single">

_83

{uploading ? 'Uploading ...' : 'Upload avatar'}

_83

</label>

_83

<span style="display:none">

_83

<input

_83

type="file"

_83

id="single"

_83

accept="image/*"

_83

bind:files

_83

on:change={uploadAvatar}

_83

disabled={uploading}

_83

/>

_83

</span>

_83

</div>

_83

</div>

  
`

### Add the new widget#

And then we can add the widget to the Account page:

src/lib/Account.svelte

`  

_11

<script lang="ts">

_11

// Import the new component

_11

import Avatar from './Avatar.svelte'

_11

</script>

_11

_11

<form on:submit|preventDefault="{updateProfile}" class="form-widget">

_11

<!-- Add to body -->

_11

<Avatar bind:url="{avatarUrl}" size="{150}" on:upload="{updateProfile}" />

_11

_11

<!-- Other form elements -->

_11

</form>

  
`

At this stage you have a fully functional application!

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/content/guides/getting-
started/tutorials/with-svelte.mdx)

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

