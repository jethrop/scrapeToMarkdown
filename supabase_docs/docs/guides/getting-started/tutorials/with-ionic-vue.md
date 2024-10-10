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
  4.   5. [Ionic Vue](/docs/guides/getting-started/tutorials/with-ionic-vue)
  6. 

# Build a User Management App with Ionic Vue

* * *

This tutorial demonstrates how to build a basic user management app. The app
authenticates and identifies the user, stores their profile information in the
database, and allows the user to log in, update their profile details, and
upload a profile photo. The app uses:

  * [Supabase Database](/docs/guides/database) \- a Postgres database for storing your user data and [Row Level Security](/docs/guides/auth#row-level-security) so data is protected and users can only access their own information.
  * [Supabase Auth](/docs/guides/auth) \- allow users to sign up and log in.
  * [Supabase Storage](/docs/guides/storage) \- users can upload a profile photo.

![Supabase User Management example](/docs/img/ionic-demos/ionic-angular-
account.png)

If you get stuck while working through this guide, refer to the [full example
on GitHub](https://github.com/mhartington/supabase-ionic-vue).

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

Let's start building the Vue app from scratch.

### Initialize an Ionic Vue app#

We can use the [Ionic CLI](https://ionicframework.com/docs/cli) to initialize
an app called `supabase-ionic-vue`:

`  

_10

npm install -g @ionic/cli

_10

ionic start supabase-ionic-vue blank --type vue

_10

cd supabase-ionic-vue

  
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

VUE_APP_SUPABASE_URL=YOUR_SUPABASE_URL

_10

VUE_APP_SUPABASE_ANON_KEY=YOUR_SUPABASE_ANON_KEY

  
`

Now that we have the API credentials in place, let's create a helper file to
initialize the Supabase client. These variables will be exposed on the
browser, and that's completely fine since we have [Row Level
Security](/docs/guides/auth#row-level-security) enabled on our Database.

src/supabase.ts"

`  

_10

import { createClient } from '@supabase/supabase-js';

_10

_10

const supabaseUrl = process.env.VUE_APP_SUPABASE_URL as string;

_10

const supabaseAnonKey = process.env.VUE_APP_SUPABASE_ANON_KEY as string;

_10

_10

export const supabase = createClient(supabaseUrl, supabaseAnonKey);

  
`

### Set up a login route#

Let's set up a Vue component to manage logins and sign ups. We'll use Magic
Links, so users can sign in with their email without using passwords.

/src/views/Login.vue

`  

_86

<template>

_86

<ion-page>

_86

<ion-header>

_86

<ion-toolbar>

_86

<ion-title>Login</ion-title>

_86

</ion-toolbar>

_86

</ion-header>

_86

_86

<ion-content>

_86

<div class="ion-padding">

_86

<h1>Supabase + Ionic Vue</h1>

_86

<p>Sign in via magic link with your email below</p>

_86

</div>

_86

<ion-list inset="true">

_86

<form @submit.prevent="handleLogin">

_86

<ion-item>

_86

<ion-label position="stacked">Email</ion-label>

_86

<ion-input v-model="email" name="email" autocomplete type="email"></ion-input>

_86

</ion-item>

_86

<div class="ion-text-center">

_86

<ion-button type="submit" fill="clear">Login</ion-button>

_86

</div>

_86

</form>

_86

</ion-list>

_86

<p>{{email}}</p>

_86

</ion-content>

_86

</ion-page>

_86

</template>

_86

_86

<script lang="ts">

_86

import { supabase } from '../supabase'

_86

import {

_86

IonContent,

_86

IonHeader,

_86

IonPage,

_86

IonTitle,

_86

IonToolbar,

_86

IonList,

_86

IonItem,

_86

IonLabel,

_86

IonInput,

_86

IonButton,

_86

toastController,

_86

loadingController,

_86

} from '@ionic/vue'

_86

import { defineComponent, ref } from 'vue'

_86

_86

export default defineComponent({

_86

name: 'LoginPage',

_86

components: {

_86

IonContent,

_86

IonHeader,

_86

IonPage,

_86

IonTitle,

_86

IonToolbar,

_86

IonList,

_86

IonItem,

_86

IonLabel,

_86

IonInput,

_86

IonButton,

_86

},

_86

setup() {

_86

const email = ref('')

_86

const handleLogin = async () => {

_86

const loader = await loadingController.create({})

_86

const toast = await toastController.create({ duration: 5000 })

_86

_86

try {

_86

await loader.present()

_86

const { error } = await supabase.auth.signIn({ email: email.value })

_86

_86

if (error) throw error

_86

_86

toast.message = 'Check your email for the login link!'

_86

await toast.present()

_86

} catch (error: any) {

_86

toast.message = error.error_description || error.message

_86

await toast.present()

_86

} finally {

_86

await loader.dismiss()

_86

}

_86

}

_86

return { handleLogin, email }

_86

},

_86

})

_86

</script>

  
`

### Account page#

After a user is signed in we can allow them to edit their profile details and
manage their account.

Let's create a new component for that called `Account.vue`.

src/views/Account.vue

`  

_152

<template>

_152

<ion-page>

_152

<ion-header>

_152

<ion-toolbar>

_152

<ion-title>Account</ion-title>

_152

</ion-toolbar>

_152

</ion-header>

_152

_152

<ion-content>

_152

<form @submit.prevent="updateProfile">

_152

<ion-item>

_152

<ion-label>

_152

<p>Email</p>

_152

<p>{{ session?.user?.email }}</p>

_152

</ion-label>

_152

</ion-item>

_152

_152

<ion-item>

_152

<ion-label position="stacked">Name</ion-label>

_152

<ion-input type="text" name="username" v-model="profile.username"></ion-input>

_152

</ion-item>

_152

_152

<ion-item>

_152

<ion-label position="stacked">Website</ion-label>

_152

<ion-input type="url" name="website" v-model="profile.website"></ion-input>

_152

</ion-item>

_152

<div class="ion-text-center">

_152

<ion-button fill="clear" type="submit">Update Profile</ion-button>

_152

</div>

_152

</form>

_152

_152

<div class="ion-text-center">

_152

<ion-button fill="clear" @click="signOut">Log Out</ion-button>

_152

</div>

_152

</ion-content>

_152

</ion-page>

_152

</template>

_152

_152

<script lang="ts">

_152

import { store } from '@/store'

_152

import { supabase } from '@/supabase'

_152

import {

_152

IonContent,

_152

IonHeader,

_152

IonPage,

_152

IonTitle,

_152

IonToolbar,

_152

toastController,

_152

loadingController,

_152

IonInput,

_152

IonItem,

_152

IonButton,

_152

IonLabel,

_152

} from '@ionic/vue'

_152

import { User } from '@supabase/supabase-js'

_152

import { defineComponent, onMounted, ref } from 'vue'

_152

export default defineComponent({

_152

name: 'AccountPage',

_152

components: {

_152

IonContent,

_152

IonHeader,

_152

IonPage,

_152

IonTitle,

_152

IonToolbar,

_152

IonInput,

_152

IonItem,

_152

IonButton,

_152

IonLabel,

_152

},

_152

setup() {

_152

const session = ref(supabase.auth.session())

_152

const profile = ref({

_152

username: '',

_152

website: '',

_152

avatar_url: '',

_152

})

_152

const user = store.user as User

_152

async function getProfile() {

_152

const loader = await loadingController.create({})

_152

const toast = await toastController.create({ duration: 5000 })

_152

await loader.present()

_152

try {

_152

const { data, error, status } = await supabase

_152

.from('profiles')

_152

.select(`username, website, avatar_url`)

_152

.eq('id', user.id)

_152

.single()

_152

_152

if (error && status !== 406) throw error

_152

_152

if (data) {

_152

console.log(data)

_152

profile.value = {

_152

username: data.username,

_152

website: data.website,

_152

avatar_url: data.avatar_url,

_152

}

_152

}

_152

} catch (error: any) {

_152

toast.message = error.message

_152

await toast.present()

_152

} finally {

_152

await loader.dismiss()

_152

}

_152

}

_152

_152

const updateProfile = async () => {

_152

const loader = await loadingController.create({})

_152

const toast = await toastController.create({ duration: 5000 })

_152

try {

_152

await loader.present()

_152

const updates = {

_152

id: user.id,

_152

...profile.value,

_152

updated_at: new Date(),

_152

}

_152

//

_152

const { error } = await supabase.from('profiles').upsert(updates, {

_152

returning: 'minimal', // Don't return the value after inserting

_152

})

_152

//

_152

if (error) throw error

_152

} catch (error: any) {

_152

toast.message = error.message

_152

await toast.present()

_152

} finally {

_152

await loader.dismiss()

_152

}

_152

}

_152

_152

async function signOut() {

_152

const loader = await loadingController.create({})

_152

const toast = await toastController.create({ duration: 5000 })

_152

await loader.present()

_152

try {

_152

const { error } = await supabase.auth.signOut()

_152

if (error) throw error

_152

} catch (error: any) {

_152

toast.message = error.message

_152

await toast.present()

_152

} finally {

_152

await loader.dismiss()

_152

}

_152

}

_152

_152

onMounted(() => {

_152

getProfile()

_152

})

_152

return { signOut, profile, session, updateProfile }

_152

},

_152

})

_152

</script>

  
`

### Launch!#

Now that we have all the components in place, let's update `App.vue` and our
routes:

src/router.index.ts

`  

_23

import { createRouter, createWebHistory } from '@ionic/vue-router'

_23

import { RouteRecordRaw } from 'vue-router'

_23

import LoginPage from '../views/Login.vue'

_23

import AccountPage from '../views/Account.vue'

_23

const routes: Array<RouteRecordRaw> = [

_23

{

_23

path: '/',

_23

name: 'Login',

_23

component: LoginPage,

_23

},

_23

{

_23

path: '/account',

_23

name: 'Account',

_23

component: AccountPage,

_23

},

_23

]

_23

_23

const router = createRouter({

_23

history: createWebHistory(process.env.BASE_URL),

_23

routes,

_23

})

_23

_23

export default router

  
`

src/App.vue

`  

_31

<template>

_31

<ion-app>

_31

<ion-router-outlet />

_31

</ion-app>

_31

</template>

_31

_31

<script lang="ts">

_31

import { IonApp, IonRouterOutlet, useIonRouter } from '@ionic/vue'

_31

import { defineComponent } from 'vue'

_31

_31

import { store } from './store'

_31

import { supabase } from './supabase'

_31

_31

export default defineComponent({

_31

name: 'App',

_31

components: {

_31

IonApp,

_31

IonRouterOutlet,

_31

},

_31

setup() {

_31

const router = useIonRouter()

_31

store.user = supabase.auth.user() ?? {}

_31

supabase.auth.onAuthStateChange((_, session) => {

_31

store.user = session?.user ?? {}

_31

if (session?.user) {

_31

router.replace('/account')

_31

}

_31

})

_31

},

_31

})

_31

</script>

  
`

Once that's done, run this in a terminal window:

`  

_10

ionic serve

  
`

And then open the browser to [localhost:3000](http://localhost:3000) and you
should see the completed app.

![Supabase Ionic Vue](/docs/img/ionic-demos/ionic-vue.png)

## Bonus: Profile photos#

Every Supabase project is configured with [Storage](/docs/guides/storage) for
managing large files like photos and videos.

### Create an upload widget#

First install two packages in order to interact with the user's camera.

`  

_10

npm install @ionic/pwa-elements @capacitor/camera

  
`

[CapacitorJS](https://capacitorjs.com) is a cross platform native runtime from
Ionic that enables web apps to be deployed through the app store and provides
access to native device API.

Ionic PWA elements is a companion package that will polyfill certain browser
APIs that provide no user interface with custom Ionic UI.

With those packages installed we can update our `main.ts` to include an
additional bootstrapping call for the Ionic PWA Elements.

src/main.tsx"

`  

_18

import { createApp } from 'vue'

_18

import App from './App.vue'

_18

import router from './router'

_18

_18

import { IonicVue } from '@ionic/vue'

_18

/* Core CSS required for Ionic components to work properly */

_18

import '@ionic/vue/css/ionic.bundle.css'

_18

_18

/* Theme variables */

_18

import './theme/variables.css'

_18

_18

import { defineCustomElements } from '@ionic/pwa-elements/loader'

_18

defineCustomElements(window)

_18

const app = createApp(App).use(IonicVue).use(router)

_18

_18

router.isReady().then(() => {

_18

app.mount('#app')

_18

})

  
`

Then create an **AvatarComponent**.

src/components/Avatar.vue

`  

_96

<template>

_96

<div class="avatar">

_96

<div class="avatar_wrapper" @click="uploadAvatar">

_96

<img v-if="avatarUrl" :src="avatarUrl" />

_96

<ion-icon v-else name="person" class="no-avatar"></ion-icon>

_96

</div>

_96

</div>

_96

</template>

_96

_96

<script lang="ts">

_96

import { ref, toRefs, watch, defineComponent } from 'vue'

_96

import { supabase } from '../supabase'

_96

import { Camera, CameraResultType } from '@capacitor/camera'

_96

import { IonIcon } from '@ionic/vue'

_96

import { person } from 'ionicons/icons'

_96

export default defineComponent({

_96

name: 'AppAvatar',

_96

props: { path: String },

_96

emits: ['upload', 'update:path'],

_96

components: { IonIcon },

_96

setup(prop, { emit }) {

_96

const { path } = toRefs(prop)

_96

const avatarUrl = ref('')

_96

_96

const downloadImage = async () => {

_96

try {

_96

const { data, error } = await
supabase.storage.from('avatars').download(path.value)

_96

if (error) throw error

_96

avatarUrl.value = URL.createObjectURL(data!)

_96

} catch (error: any) {

_96

console.error('Error downloading image: ', error.message)

_96

}

_96

}

_96

_96

const uploadAvatar = async () => {

_96

try {

_96

const photo = await Camera.getPhoto({

_96

resultType: CameraResultType.DataUrl,

_96

})

_96

if (photo.dataUrl) {

_96

const file = await fetch(photo.dataUrl)

_96

.then((res) => res.blob())

_96

.then((blob) => new File([blob], 'my-file', { type: `image/${photo.format}`
}))

_96

_96

const fileName = `${Math.random()}-${new Date().getTime()}.${photo.format}`

_96

const { error: uploadError } = await supabase.storage

_96

.from('avatars')

_96

.upload(fileName, file)

_96

if (uploadError) {

_96

throw uploadError

_96

}

_96

emit('update:path', fileName)

_96

emit('upload')

_96

}

_96

} catch (error) {

_96

console.log(error)

_96

}

_96

}

_96

_96

watch(path, () => {

_96

if (path.value) downloadImage()

_96

})

_96

_96

return { avatarUrl, uploadAvatar, person }

_96

},

_96

})

_96

</script>

_96

<style>

_96

.avatar {

_96

display: block;

_96

margin: auto;

_96

min-height: 150px;

_96

}

_96

.avatar .avatar_wrapper {

_96

margin: 16px auto 16px;

_96

border-radius: 50%;

_96

overflow: hidden;

_96

height: 150px;

_96

aspect-ratio: 1;

_96

background: var(--ion-color-step-50);

_96

border: thick solid var(--ion-color-step-200);

_96

}

_96

.avatar .avatar_wrapper:hover {

_96

cursor: pointer;

_96

}

_96

.avatar .avatar_wrapper ion-icon.no-avatar {

_96

width: 100%;

_96

height: 115%;

_96

}

_96

.avatar img {

_96

display: block;

_96

object-fit: cover;

_96

width: 100%;

_96

height: 100%;

_96

}

_96

</style>

  
`

### Add the new widget#

And then we can add the widget to the Account page:

src/views/Account.vue

`  

_22

<template>

_22

<ion-page>

_22

<ion-header>

_22

<ion-toolbar>

_22

<ion-title>Account</ion-title>

_22

</ion-toolbar>

_22

</ion-header>

_22

_22

<ion-content>

_22

<avatar v-model:path="profile.avatar_url" @upload="updateProfile"></avatar>

_22

...

_22

</template>

_22

<script lang="ts">

_22

import Avatar from '../components/Avatar.vue';

_22

export default defineComponent({

_22

name: 'AccountPage',

_22

components: {

_22

Avatar,

_22

....

_22

}

_22

_22

</script>

  
`

At this stage you have a fully functional application!

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/content/guides/getting-
started/tutorials/with-ionic-vue.mdx)

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

