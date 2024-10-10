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
  4.   5. [SolidJS](/docs/guides/getting-started/tutorials/with-solidjs)
  6. 

# Build a User Management App with SolidJS

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
management/solid-user-management).

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

Let's start building the SolidJS app from scratch.

### Initialize a SolidJS app#

We can use [Degit](https://github.com/Rich-Harris/degit) to initialize an app
called `supabase-solid`:

`  

_10

npx degit solidjs/templates/ts supabase-solid

_10

cd supabase-solid

  
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

src/supabaseClient.jsx

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

An optional step is to update the CSS file `src/index.css` to make the app
look nice. You can find the full contents of this file
[here](https://raw.githubusercontent.com/supabase/supabase/master/examples/user-
management/solid-user-management/src/index.css).

### Set up a login component#

Let's set up a SolidJS component to manage logins and sign ups. We'll use
Magic Links, so users can sign in with their email without using passwords.

src/Auth.tsx

`  

_51

import { createSignal } from 'solid-js'

_51

import { supabase } from './supabaseClient'

_51

_51

export default function Auth() {

_51

const [loading, setLoading] = createSignal(false)

_51

const [email, setEmail] = createSignal('')

_51

_51

const handleLogin = async (e: SubmitEvent) => {

_51

e.preventDefault()

_51

_51

try {

_51

setLoading(true)

_51

const { error } = await supabase.auth.signInWithOtp({ email: email() })

_51

if (error) throw error

_51

alert('Check your email for the login link!')

_51

} catch (error) {

_51

if (error instanceof Error) {

_51

alert(error.message)

_51

}

_51

} finally {

_51

setLoading(false)

_51

}

_51

}

_51

_51

return (

_51

<div class="row flex-center flex">

_51

<div class="col-6 form-widget" aria-live="polite">

_51

<h1 class="header">Supabase + SolidJS</h1>

_51

<p class="description">Sign in via magic link with your email below</p>

_51

<form class="form-widget" onSubmit={handleLogin}>

_51

<div>

_51

<label for="email">Email</label>

_51

<input

_51

id="email"

_51

class="inputField"

_51

type="email"

_51

placeholder="Your email"

_51

value={email()}

_51

onChange={(e) => setEmail(e.currentTarget.value)}

_51

/>

_51

</div>

_51

<div>

_51

<button type="submit" class="button block" aria-live="polite">

_51

{loading() ? <span>Loading</span> : <span>Send magic link</span>}

_51

</button>

_51

</div>

_51

</form>

_51

</div>

_51

</div>

_51

)

_51

}

  
`

### Account page#

After a user is signed in we can allow them to edit their profile details and
manage their account.

Let's create a new component for that called `Account.tsx`.

src/Account.tsx

`  

_112

import { AuthSession } from '@supabase/supabase-js'

_112

import { Component, createEffect, createSignal } from 'solid-js'

_112

import { supabase } from './supabaseClient'

_112

_112

interface Props {

_112

session: AuthSession

_112

}

_112

_112

const Account: Component<Props> = ({ session }) => {

_112

const [loading, setLoading] = createSignal(true)

_112

const [username, setUsername] = createSignal<string | null>(null)

_112

const [website, setWebsite] = createSignal<string | null>(null)

_112

const [avatarUrl, setAvatarUrl] = createSignal<string | null>(null)

_112

_112

createEffect(() => {

_112

getProfile()

_112

})

_112

_112

const getProfile = async () => {

_112

try {

_112

setLoading(true)

_112

const { user } = session

_112

_112

const { data, error, status } = await supabase

_112

.from('profiles')

_112

.select(`username, website, avatar_url`)

_112

.eq('id', user.id)

_112

.single()

_112

_112

if (error && status !== 406) {

_112

throw error

_112

}

_112

_112

if (data) {

_112

setUsername(data.username)

_112

setWebsite(data.website)

_112

setAvatarUrl(data.avatar_url)

_112

}

_112

} catch (error) {

_112

if (error instanceof Error) {

_112

alert(error.message)

_112

}

_112

} finally {

_112

setLoading(false)

_112

}

_112

}

_112

_112

const updateProfile = async (e: Event) => {

_112

e.preventDefault()

_112

_112

try {

_112

setLoading(true)

_112

const { user } = session

_112

_112

const updates = {

_112

id: user.id,

_112

username: username(),

_112

website: website(),

_112

avatar_url: avatarUrl(),

_112

updated_at: new Date().toISOString(),

_112

}

_112

_112

const { error } = await supabase.from('profiles').upsert(updates)

_112

_112

if (error) {

_112

throw error

_112

}

_112

} catch (error) {

_112

if (error instanceof Error) {

_112

alert(error.message)

_112

}

_112

} finally {

_112

setLoading(false)

_112

}

_112

}

_112

_112

return (

_112

<div aria-live="polite">

_112

<form onSubmit={updateProfile} class="form-widget">

_112

<div>Email: {session.user.email}</div>

_112

<div>

_112

<label for="username">Name</label>

_112

<input

_112

id="username"

_112

type="text"

_112

value={username() || ''}

_112

onChange={(e) => setUsername(e.currentTarget.value)}

_112

/>

_112

</div>

_112

<div>

_112

<label for="website">Website</label>

_112

<input

_112

id="website"

_112

type="text"

_112

value={website() || ''}

_112

onChange={(e) => setWebsite(e.currentTarget.value)}

_112

/>

_112

</div>

_112

<div>

_112

<button type="submit" class="button primary block" disabled={loading()}>

_112

{loading() ? 'Saving ...' : 'Update profile'}

_112

</button>

_112

</div>

_112

<button type="button" class="button block" onClick={() =>
supabase.auth.signOut()}>

_112

Sign Out

_112

</button>

_112

</form>

_112

</div>

_112

)

_112

}

_112

_112

export default Account

  
`

### Launch!#

Now that we have all the components in place, let's update `App.tsx`:

src/App.tsx

`  

_27

import { Component, createEffect, createSignal } from 'solid-js'

_27

import { supabase } from './supabaseClient'

_27

import { AuthSession } from '@supabase/supabase-js'

_27

import Account from './Account'

_27

import Auth from './Auth'

_27

_27

const App: Component = () => {

_27

const [session, setSession] = createSignal<AuthSession | null>(null)

_27

_27

createEffect(() => {

_27

supabase.auth.getSession().then(({ data: { session } }) => {

_27

setSession(session)

_27

})

_27

_27

supabase.auth.onAuthStateChange((_event, session) => {

_27

setSession(session)

_27

})

_27

})

_27

_27

return (

_27

<div class="container" style={{ padding: '50px 0 100px 0' }}>

_27

{!session() ? <Auth /> : <Account session={session()!} />}

_27

</div>

_27

)

_27

}

_27

_27

export default App

  
`

Once that's done, run this in a terminal window:

`  

_10

npm start

  
`

And then open the browser to [localhost:3000](http://localhost:3000) and you
should see the completed app.

![Supabase SolidJS](/docs/img/supabase-solidjs-demo.png)

## Bonus: Profile photos#

Every Supabase project is configured with [Storage](/docs/guides/storage) for
managing large files like photos and videos.

### Create an upload widget#

Let's create an avatar for the user so that they can upload a profile photo.
We can start by creating a new component:

src/Avatar.tsx

`  

_96

import { Component, createEffect, createSignal, JSX } from 'solid-js'

_96

import { supabase } from './supabaseClient'

_96

_96

interface Props {

_96

size: number

_96

url: string | null

_96

onUpload: (event: Event, filePath: string) => void

_96

}

_96

_96

const Avatar: Component<Props> = (props) => {

_96

const [avatarUrl, setAvatarUrl] = createSignal<string | null>(null)

_96

const [uploading, setUploading] = createSignal(false)

_96

_96

createEffect(() => {

_96

if (props.url) downloadImage(props.url)

_96

})

_96

_96

const downloadImage = async (path: string) => {

_96

try {

_96

const { data, error } = await supabase.storage.from('avatars').download(path)

_96

if (error) {

_96

throw error

_96

}

_96

const url = URL.createObjectURL(data)

_96

setAvatarUrl(url)

_96

} catch (error) {

_96

if (error instanceof Error) {

_96

console.log('Error downloading image: ', error.message)

_96

}

_96

}

_96

}

_96

_96

const uploadAvatar: JSX.EventHandler<HTMLInputElement, Event> = async (event)
=> {

_96

try {

_96

setUploading(true)

_96

_96

const target = event.currentTarget

_96

if (!target?.files || target.files.length === 0) {

_96

throw new Error('You must select an image to upload.')

_96

}

_96

_96

const file = target.files[0]

_96

const fileExt = file.name.split('.').pop()

_96

const fileName = `${Math.random()}.${fileExt}`

_96

const filePath = `${fileName}`

_96

_96

const { error: uploadError } = await
supabase.storage.from('avatars').upload(filePath, file)

_96

_96

if (uploadError) {

_96

throw uploadError

_96

}

_96

_96

props.onUpload(event, filePath)

_96

} catch (error) {

_96

if (error instanceof Error) {

_96

alert(error.message)

_96

}

_96

} finally {

_96

setUploading(false)

_96

}

_96

}

_96

_96

return (

_96

<div style={{ width: `${props.size}px` }} aria-live="polite">

_96

{avatarUrl() ? (

_96

<img

_96

src={avatarUrl()!}

_96

alt={avatarUrl() ? 'Avatar' : 'No image'}

_96

class="avatar image"

_96

style={{ height: `${props.size}px`, width: `${props.size}px` }}

_96

/>

_96

) : (

_96

<div

_96

class="avatar no-image"

_96

style={{ height: `${props.size}px`, width: `${props.size}px` }}

_96

/>

_96

)}

_96

<div style={{ width: `${props.size}px` }}>

_96

<label class="button primary block" for="single">

_96

{uploading() ? 'Uploading ...' : 'Upload avatar'}

_96

</label>

_96

<span style="display:none">

_96

<input

_96

type="file"

_96

id="single"

_96

accept="image/*"

_96

onChange={uploadAvatar}

_96

disabled={uploading()}

_96

/>

_96

</span>

_96

</div>

_96

</div>

_96

)

_96

}

_96

_96

export default Avatar

  
`

### Add the new widget#

And then we can add the widget to the Account page:

src/Account.tsx

`  

_19

// Import the new component

_19

import Avatar from './Avatar'

_19

_19

// ...

_19

_19

return (

_19

<form onSubmit={updateProfile} class="form-widget">

_19

{/* Add to the body */}

_19

<Avatar

_19

url={avatarUrl()}

_19

size={150}

_19

onUpload={(e: Event, url: string) => {

_19

setAvatarUrl(url)

_19

updateProfile(e)

_19

}}

_19

/>

_19

{/* ... */}

_19

</div>

_19

)

  
`

At this stage you have a fully functional application!

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/content/guides/getting-
started/tutorials/with-solidjs.mdx)

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

