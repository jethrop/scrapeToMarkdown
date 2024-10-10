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
  2.   3. Mobile tutorials
  4.   5. [Expo React Native](/docs/guides/getting-started/tutorials/with-expo-react-native)
  6. 

# Build a User Management App with Expo React Native

* * *

This tutorial demonstrates how to build a basic user management app. The app
authenticates and identifies the user, stores their profile information in the
database, and allows the user to log in, update their profile details, and
upload a profile photo. The app uses:

  * [Supabase Database](/docs/guides/database) \- a Postgres database for storing your user data and [Row Level Security](/docs/guides/auth#row-level-security) so data is protected and users can only access their own information.
  * [Supabase Auth](/docs/guides/auth) \- allow users to sign up and log in.
  * [Supabase Storage](/docs/guides/storage) \- users can upload a profile photo.

![Supabase User Management example](/docs/img/supabase-flutter-demo.png)

If you get stuck while working through this guide, refer to the [full example
on GitHub](https://github.com/supabase/supabase/tree/master/examples/user-
management/expo-user-management).

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

Let's start building the React Native app from scratch.

### Initialize a React Native app#

We can use [`expo`](https://docs.expo.dev/get-started/create-a-new-app/) to
initialize an app called `expo-user-management`:

`  

_10

npx create-expo-app -t expo-template-blank-typescript expo-user-management

_10

_10

cd expo-user-management

  
`

Then let's install the additional dependencies: [supabase-
js](https://github.com/supabase/supabase-js)

`  

_10

npx expo install @supabase/supabase-js @react-native-async-storage/async-
storage @rneui/themed

  
`

Now let's create a helper file to initialize the Supabase client. We need the
API URL and the `anon` key that you copied earlier. These variables are safe
to expose in your Expo app since Supabase has [Row Level
Security](/docs/guides/auth#row-level-security) enabled on your Database.

AsyncStorageSecureStore

lib/supabase.ts

`  

_14

import AsyncStorage from '@react-native-async-storage/async-storage'

_14

import { createClient } from '@supabase/supabase-js'

_14

_14

const supabaseUrl = YOUR_REACT_NATIVE_SUPABASE_URL

_14

const supabaseAnonKey = YOUR_REACT_NATIVE_SUPABASE_ANON_KEY

_14

_14

export const supabase = createClient(supabaseUrl, supabaseAnonKey, {

_14

auth: {

_14

storage: AsyncStorage,

_14

autoRefreshToken: true,

_14

persistSession: true,

_14

detectSessionInUrl: false,

_14

},

_14

})

  
`

### Set up a login component#

Let's set up a React Native component to manage logins and sign ups. Users
would be able to sign in with their email and password.

components/Auth.tsx

`  

_95

import React, { useState } from 'react'

_95

import { Alert, StyleSheet, View, AppState } from 'react-native'

_95

import { supabase } from '../lib/supabase'

_95

import { Button, Input } from '@rneui/themed'

_95

_95

// Tells Supabase Auth to continuously refresh the session automatically if

_95

// the app is in the foreground. When this is added, you will continue to
receive

_95

// `onAuthStateChange` events with the `TOKEN_REFRESHED` or `SIGNED_OUT` event

_95

// if the user's session is terminated. This should only be registered once.

_95

AppState.addEventListener('change', (state) => {

_95

if (state === 'active') {

_95

supabase.auth.startAutoRefresh()

_95

} else {

_95

supabase.auth.stopAutoRefresh()

_95

}

_95

})

_95

_95

export default function Auth() {

_95

const [email, setEmail] = useState('')

_95

const [password, setPassword] = useState('')

_95

const [loading, setLoading] = useState(false)

_95

_95

async function signInWithEmail() {

_95

setLoading(true)

_95

const { error } = await supabase.auth.signInWithPassword({

_95

email: email,

_95

password: password,

_95

})

_95

_95

if (error) Alert.alert(error.message)

_95

setLoading(false)

_95

}

_95

_95

async function signUpWithEmail() {

_95

setLoading(true)

_95

const {

_95

data: { session },

_95

error,

_95

} = await supabase.auth.signUp({

_95

email: email,

_95

password: password,

_95

})

_95

_95

if (error) Alert.alert(error.message)

_95

if (!session) Alert.alert('Please check your inbox for email verification!')

_95

setLoading(false)

_95

}

_95

_95

return (

_95

<View style={styles.container}>

_95

<View style={[styles.verticallySpaced, styles.mt20]}>

_95

<Input

_95

label="Email"

_95

leftIcon={{ type: 'font-awesome', name: 'envelope' }}

_95

onChangeText={(text) => setEmail(text)}

_95

value={email}

_95

placeholder="[[email protected]](/cdn-cgi/l/email-protection)"

_95

autoCapitalize={'none'}

_95

/>

_95

</View>

_95

<View style={styles.verticallySpaced}>

_95

<Input

_95

label="Password"

_95

leftIcon={{ type: 'font-awesome', name: 'lock' }}

_95

onChangeText={(text) => setPassword(text)}

_95

value={password}

_95

secureTextEntry={true}

_95

placeholder="Password"

_95

autoCapitalize={'none'}

_95

/>

_95

</View>

_95

<View style={[styles.verticallySpaced, styles.mt20]}>

_95

<Button title="Sign in" disabled={loading} onPress={() => signInWithEmail()}
/>

_95

</View>

_95

<View style={styles.verticallySpaced}>

_95

<Button title="Sign up" disabled={loading} onPress={() => signUpWithEmail()}
/>

_95

</View>

_95

</View>

_95

)

_95

}

_95

_95

const styles = StyleSheet.create({

_95

container: {

_95

marginTop: 40,

_95

padding: 12,

_95

},

_95

verticallySpaced: {

_95

paddingTop: 4,

_95

paddingBottom: 4,

_95

alignSelf: 'stretch',

_95

},

_95

mt20: {

_95

marginTop: 20,

_95

},

_95

})

  
`

By default Supabase Auth requires email verification before a session is
created for the users. To support email verification you need to [implement
deep link handling](/docs/guides/auth/native-mobile-deep-
linking?platform=react-native)!

While testing, you can disable email confirmation in your [project's email
auth provider settings](/dashboard/project/_/auth/providers).

### Account page#

After a user is signed in we can allow them to edit their profile details and
manage their account.

Let's create a new component for that called `Account.tsx`.

components/Account.tsx

`  

_120

import { useState, useEffect } from 'react'

_120

import { supabase } from '../lib/supabase'

_120

import { StyleSheet, View, Alert } from 'react-native'

_120

import { Button, Input } from '@rneui/themed'

_120

import { Session } from '@supabase/supabase-js'

_120

_120

export default function Account({ session }: { session: Session }) {

_120

const [loading, setLoading] = useState(true)

_120

const [username, setUsername] = useState('')

_120

const [website, setWebsite] = useState('')

_120

const [avatarUrl, setAvatarUrl] = useState('')

_120

_120

useEffect(() => {

_120

if (session) getProfile()

_120

}, [session])

_120

_120

async function getProfile() {

_120

try {

_120

setLoading(true)

_120

if (!session?.user) throw new Error('No user on the session!')

_120

_120

const { data, error, status } = await supabase

_120

.from('profiles')

_120

.select(`username, website, avatar_url`)

_120

.eq('id', session?.user.id)

_120

.single()

_120

if (error && status !== 406) {

_120

throw error

_120

}

_120

_120

if (data) {

_120

setUsername(data.username)

_120

setWebsite(data.website)

_120

setAvatarUrl(data.avatar_url)

_120

}

_120

} catch (error) {

_120

if (error instanceof Error) {

_120

Alert.alert(error.message)

_120

}

_120

} finally {

_120

setLoading(false)

_120

}

_120

}

_120

_120

async function updateProfile({

_120

username,

_120

website,

_120

avatar_url,

_120

}: {

_120

username: string

_120

website: string

_120

avatar_url: string

_120

}) {

_120

try {

_120

setLoading(true)

_120

if (!session?.user) throw new Error('No user on the session!')

_120

_120

const updates = {

_120

id: session?.user.id,

_120

username,

_120

website,

_120

avatar_url,

_120

updated_at: new Date(),

_120

}

_120

_120

const { error } = await supabase.from('profiles').upsert(updates)

_120

_120

if (error) {

_120

throw error

_120

}

_120

} catch (error) {

_120

if (error instanceof Error) {

_120

Alert.alert(error.message)

_120

}

_120

} finally {

_120

setLoading(false)

_120

}

_120

}

_120

_120

return (

_120

<View style={styles.container}>

_120

<View style={[styles.verticallySpaced, styles.mt20]}>

_120

<Input label="Email" value={session?.user?.email} disabled />

_120

</View>

_120

<View style={styles.verticallySpaced}>

_120

<Input label="Username" value={username || ''} onChangeText={(text) =>
setUsername(text)} />

_120

</View>

_120

<View style={styles.verticallySpaced}>

_120

<Input label="Website" value={website || ''} onChangeText={(text) =>
setWebsite(text)} />

_120

</View>

_120

_120

<View style={[styles.verticallySpaced, styles.mt20]}>

_120

<Button

_120

title={loading ? 'Loading ...' : 'Update'}

_120

onPress={() => updateProfile({ username, website, avatar_url: avatarUrl })}

_120

disabled={loading}

_120

/>

_120

</View>

_120

_120

<View style={styles.verticallySpaced}>

_120

<Button title="Sign Out" onPress={() => supabase.auth.signOut()} />

_120

</View>

_120

</View>

_120

)

_120

}

_120

_120

const styles = StyleSheet.create({

_120

container: {

_120

marginTop: 40,

_120

padding: 12,

_120

},

_120

verticallySpaced: {

_120

paddingTop: 4,

_120

paddingBottom: 4,

_120

alignSelf: 'stretch',

_120

},

_120

mt20: {

_120

marginTop: 20,

_120

},

_120

})

  
`

### Launch!#

Now that we have all the components in place, let's update `App.tsx`:

App.tsx

`  

_26

import { useState, useEffect } from 'react'

_26

import { supabase } from './lib/supabase'

_26

import Auth from './components/Auth'

_26

import Account from './components/Account'

_26

import { View } from 'react-native'

_26

import { Session } from '@supabase/supabase-js'

_26

_26

export default function App() {

_26

const [session, setSession] = useState<Session | null>(null)

_26

_26

useEffect(() => {

_26

supabase.auth.getSession().then(({ data: { session } }) => {

_26

setSession(session)

_26

})

_26

_26

supabase.auth.onAuthStateChange((_event, session) => {

_26

setSession(session)

_26

})

_26

}, [])

_26

_26

return (

_26

<View>

_26

{session && session.user ? <Account key={session.user.id} session={session} />
: <Auth />}

_26

</View>

_26

)

_26

}

  
`

Once that's done, run this in a terminal window:

`  

_10

npm start

  
`

And then press the appropriate key for the environment you want to test the
app in and you should see the completed app.

## Bonus: Profile photos#

Every Supabase project is configured with [Storage](/docs/guides/storage) for
managing large files like photos and videos.

### Additional dependency installation#

You will need an image picker that works on the environment you will build the
project for, we will use `expo-image-picker` in this example.

`  

_10

npx expo install expo-image-picker

  
`

### Create an upload widget#

Let's create an avatar for the user so that they can upload a profile photo.
We can start by creating a new component:

components/Avatar.tsx

`  

_130

import { useState, useEffect } from 'react'

_130

import { supabase } from '../lib/supabase'

_130

import { StyleSheet, View, Alert, Image, Button } from 'react-native'

_130

import * as ImagePicker from 'expo-image-picker'

_130

_130

interface Props {

_130

size: number

_130

url: string | null

_130

onUpload: (filePath: string) => void

_130

}

_130

_130

export default function Avatar({ url, size = 150, onUpload }: Props) {

_130

const [uploading, setUploading] = useState(false)

_130

const [avatarUrl, setAvatarUrl] = useState<string | null>(null)

_130

const avatarSize = { height: size, width: size }

_130

_130

useEffect(() => {

_130

if (url) downloadImage(url)

_130

}, [url])

_130

_130

async function downloadImage(path: string) {

_130

try {

_130

const { data, error } = await supabase.storage.from('avatars').download(path)

_130

_130

if (error) {

_130

throw error

_130

}

_130

_130

const fr = new FileReader()

_130

fr.readAsDataURL(data)

_130

fr.onload = () => {

_130

setAvatarUrl(fr.result as string)

_130

}

_130

} catch (error) {

_130

if (error instanceof Error) {

_130

console.log('Error downloading image: ', error.message)

_130

}

_130

}

_130

}

_130

_130

async function uploadAvatar() {

_130

try {

_130

setUploading(true)

_130

_130

const result = await ImagePicker.launchImageLibraryAsync({

_130

mediaTypes: ImagePicker.MediaTypeOptions.Images, // Restrict to only images

_130

allowsMultipleSelection: false, // Can only select one image

_130

allowsEditing: true, // Allows the user to crop / rotate their photo before
uploading it

_130

quality: 1,

_130

exif: false, // We don't want nor need that data.

_130

})

_130

_130

if (result.canceled || !result.assets || result.assets.length === 0) {

_130

console.log('User cancelled image picker.')

_130

return

_130

}

_130

_130

const image = result.assets[0]

_130

console.log('Got image', image)

_130

_130

if (!image.uri) {

_130

throw new Error('No image uri!') // Realistically, this should never happen,
but just in case...

_130

}

_130

_130

const arraybuffer = await fetch(image.uri).then((res) => res.arrayBuffer())

_130

_130

const fileExt = image.uri?.split('.').pop()?.toLowerCase() ?? 'jpeg'

_130

const path = `${Date.now()}.${fileExt}`

_130

const { data, error: uploadError } = await supabase.storage

_130

.from('avatars')

_130

.upload(path, arraybuffer, {

_130

contentType: image.mimeType ?? 'image/jpeg',

_130

})

_130

_130

if (uploadError) {

_130

throw uploadError

_130

}

_130

_130

onUpload(data.path)

_130

} catch (error) {

_130

if (error instanceof Error) {

_130

Alert.alert(error.message)

_130

} else {

_130

throw error

_130

}

_130

} finally {

_130

setUploading(false)

_130

}

_130

}

_130

_130

return (

_130

<View>

_130

{avatarUrl ? (

_130

<Image

_130

source={{ uri: avatarUrl }}

_130

accessibilityLabel="Avatar"

_130

style={[avatarSize, styles.avatar, styles.image]}

_130

/>

_130

) : (

_130

<View style={[avatarSize, styles.avatar, styles.noImage]} />

_130

)}

_130

<View>

_130

<Button

_130

title={uploading ? 'Uploading ...' : 'Upload'}

_130

onPress={uploadAvatar}

_130

disabled={uploading}

_130

/>

_130

</View>

_130

</View>

_130

)

_130

}

_130

_130

const styles = StyleSheet.create({

_130

avatar: {

_130

borderRadius: 5,

_130

overflow: 'hidden',

_130

maxWidth: '100%',

_130

},

_130

image: {

_130

objectFit: 'cover',

_130

paddingTop: 0,

_130

},

_130

noImage: {

_130

backgroundColor: '#333',

_130

borderWidth: 1,

_130

borderStyle: 'solid',

_130

borderColor: 'rgb(200, 200, 200)',

_130

borderRadius: 5,

_130

},

_130

})

  
`

### Add the new widget#

And then we can add the widget to the Account page:

components/Account.tsx

`  

_21

// Import the new component

_21

import Avatar from './Avatar'

_21

_21

// ...

_21

return (

_21

<View>

_21

{/* Add to the body */}

_21

<View>

_21

<Avatar

_21

size={200}

_21

url={avatarUrl}

_21

onUpload={(url: string) => {

_21

setAvatarUrl(url)

_21

updateProfile({ username, website, avatar_url: url })

_21

}}

_21

/>

_21

</View>

_21

{/* ... */}

_21

</View>

_21

)

_21

// ...

  
`

Now you will need to run the prebuild command to get the application working
on your chosen platform.

`  

_10

npx expo prebuild

  
`

At this stage you have a fully functional application!

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/content/guides/getting-
started/tutorials/with-expo-react-native.mdx)

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

