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
  4.   5. [Ionic React](/docs/guides/getting-started/tutorials/with-ionic-react)
  6. 

# Build a User Management App with Ionic React

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
on GitHub](https://github.com/mhartington/supabase-ionic-react).

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

Let's start building the React app from scratch.

### Initialize an Ionic React app#

We can use the [Ionic CLI](https://ionicframework.com/docs/cli) to initialize
an app called `supabase-ionic-react`:

`  

_10

npm install -g @ionic/cli

_10

ionic start supabase-ionic-react blank --type react

_10

cd supabase-ionic-react

  
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

REACT_APP_SUPABASE_URL=YOUR_SUPABASE_URL

_10

REACT_APP_SUPABASE_ANON_KEY=YOUR_SUPABASE_ANON_KEY

  
`

Now that we have the API credentials in place, let's create a helper file to
initialize the Supabase client. These variables will be exposed on the
browser, and that's completely fine since we have [Row Level
Security](/docs/guides/auth#row-level-security) enabled on our Database.

src/supabaseClient.js

`  

_10

import { createClient } from '@supabase/supabase-js'

_10

_10

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL

_10

const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY

_10

_10

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

  
`

### Set up a login route#

Let's set up a React component to manage logins and sign ups. We'll use Magic
Links, so users can sign in with their email without using passwords.

/src/pages/Login.tsx

`  

_70

import { useState } from 'react';

_70

import {

_70

IonButton,

_70

IonContent,

_70

IonHeader,

_70

IonInput,

_70

IonItem,

_70

IonLabel,

_70

IonList,

_70

IonPage,

_70

IonTitle,

_70

IonToolbar,

_70

useIonToast,

_70

useIonLoading,

_70

} from '@ionic/react';

_70

import { supabase } from '../supabaseClient';

_70

_70

export function LoginPage() {

_70

const [email, setEmail] = useState('');

_70

_70

const [showLoading, hideLoading] = useIonLoading();

_70

const [showToast ] = useIonToast();

_70

const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {

_70

console.log()

_70

e.preventDefault();

_70

await showLoading();

_70

try {

_70

await supabase.auth.signIn({ email });

_70

await showToast({ message: 'Check your email for the login link!' });

_70

} catch (e: any) {

_70

await showToast({ message: e.error_description || e.message , duration:
5000});

_70

} finally {

_70

await hideLoading();

_70

}

_70

};

_70

return (

_70

<IonPage>

_70

<IonHeader>

_70

<IonToolbar>

_70

<IonTitle>Login</IonTitle>

_70

</IonToolbar>

_70

</IonHeader>

_70

_70

<IonContent>

_70

<div className="ion-padding">

_70

<h1>Supabase + Ionic React</h1>

_70

<p>Sign in via magic link with your email below</p>

_70

</div>

_70

<IonList inset={true}>

_70

<form onSubmit={handleLogin}>

_70

<IonItem>

_70

<IonLabel position="stacked">Email</IonLabel>

_70

<IonInput

_70

value={email}

_70

name="email"

_70

onIonChange={(e) => setEmail(e.detail.value ?? '')}

_70

type="email"

_70

></IonInput>

_70

</IonItem>

_70

<div className="ion-text-center">

_70

<IonButton type="submit" fill="clear">

_70

Login

_70

</IonButton>

_70

</div>

_70

</form>

_70

</IonList>

_70

</IonContent>

_70

</IonPage>

_70

);

_70

}

  
`

### Account page#

After a user is signed in we can allow them to edit their profile details and
manage their account.

Let's create a new component for that called `Account.tsx`.

src/pages/Account.tsx

`  

_147

import {

_147

IonButton,

_147

IonContent,

_147

IonHeader,

_147

IonInput,

_147

IonItem,

_147

IonLabel,

_147

IonPage,

_147

IonTitle,

_147

IonToolbar,

_147

useIonLoading,

_147

useIonToast,

_147

useIonRouter

_147

} from '@ionic/react';

_147

import { useEffect, useState } from 'react';

_147

import { supabase } from '../supabaseClient';

_147

_147

export function AccountPage() {

_147

const [showLoading, hideLoading] = useIonLoading();

_147

const [showToast] = useIonToast();

_147

const [session] = useState(() => supabase.auth.session());

_147

const router = useIonRouter();

_147

const [profile, setProfile] = useState({

_147

username: '',

_147

website: '',

_147

avatar_url: '',

_147

});

_147

useEffect(() => {

_147

getProfile();

_147

}, [session]);

_147

const getProfile = async () => {

_147

console.log('get');

_147

await showLoading();

_147

try {

_147

const user = supabase.auth.user();

_147

const { data, error, status } = await supabase

_147

.from('profiles')

_147

.select(`username, website, avatar_url`)

_147

.eq('id', user!.id)

_147

.single();

_147

_147

if (error && status !== 406) {

_147

throw error;

_147

}

_147

_147

if (data) {

_147

setProfile({

_147

username: data.username,

_147

website: data.website,

_147

avatar_url: data.avatar_url,

_147

});

_147

}

_147

} catch (error: any) {

_147

showToast({ message: error.message, duration: 5000 });

_147

} finally {

_147

await hideLoading();

_147

}

_147

};

_147

const signOut = async () => {

_147

await supabase.auth.signOut();

_147

router.push('/', 'forward', 'replace');

_147

}

_147

const updateProfile = async (e?: any, avatar_url: string = '') => {

_147

e?.preventDefault();

_147

_147

console.log('update ');

_147

await showLoading();

_147

_147

try {

_147

const user = supabase.auth.user();

_147

_147

const updates = {

_147

id: user!.id,

_147

...profile,

_147

avatar_url: avatar_url,

_147

updated_at: new Date(),

_147

};

_147

_147

const { error } = await supabase.from('profiles').upsert(updates, {

_147

returning: 'minimal', // Don't return the value after inserting

_147

});

_147

_147

if (error) {

_147

throw error;

_147

}

_147

} catch (error: any) {

_147

showToast({ message: error.message, duration: 5000 });

_147

} finally {

_147

await hideLoading();

_147

}

_147

};

_147

return (

_147

<IonPage>

_147

<IonHeader>

_147

<IonToolbar>

_147

<IonTitle>Account</IonTitle>

_147

</IonToolbar>

_147

</IonHeader>

_147

_147

<IonContent>

_147

<form onSubmit={updateProfile}>

_147

<IonItem>

_147

<IonLabel>

_147

<p>Email</p>

_147

<p>{session?.user?.email}</p>

_147

</IonLabel>

_147

</IonItem>

_147

_147

<IonItem>

_147

<IonLabel position="stacked">Name</IonLabel>

_147

<IonInput

_147

type="text"

_147

name="username"

_147

value={profile.username}

_147

onIonChange={(e) =>

_147

setProfile({ ...profile, username: e.detail.value ?? '' })

_147

}

_147

></IonInput>

_147

</IonItem>

_147

_147

<IonItem>

_147

<IonLabel position="stacked">Website</IonLabel>

_147

<IonInput

_147

type="url"

_147

name="website"

_147

value={profile.website}

_147

onIonChange={(e) =>

_147

setProfile({ ...profile, website: e.detail.value ?? '' })

_147

}

_147

></IonInput>

_147

</IonItem>

_147

<div className="ion-text-center">

_147

<IonButton fill="clear" type="submit">

_147

Update Profile

_147

</IonButton>

_147

</div>

_147

</form>

_147

_147

<div className="ion-text-center">

_147

<IonButton fill="clear" onClick={signOut}>

_147

Log Out

_147

</IonButton>

_147

</div>

_147

</IonContent>

_147

</IonPage>

_147

);

_147

}

  
`

### Launch!#

Now that we have all the components in place, let's update `App.tsx`:

src/App.tsx

`  

_45

import { Redirect, Route } from 'react-router-dom'

_45

import { IonApp, IonRouterOutlet, setupIonicReact } from '@ionic/react'

_45

import { IonReactRouter } from '@ionic/react-router'

_45

import { supabase } from './supabaseClient'

_45

_45

import '@ionic/react/css/ionic.bundle.css'

_45

_45

/* Theme variables */

_45

import './theme/variables.css'

_45

import { LoginPage } from './pages/Login'

_45

import { AccountPage } from './pages/Account'

_45

import { useEffect, useState } from 'react'

_45

import { Session } from '@supabase/supabase-js'

_45

_45

setupIonicReact()

_45

_45

const App: React.FC = () => {

_45

const [session, setSession] = useState < Session > null

_45

useEffect(() => {

_45

setSession(supabase.auth.session())

_45

supabase.auth.onAuthStateChange((_event, session) => {

_45

setSession(session)

_45

})

_45

}, [])

_45

return (

_45

<IonApp>

_45

<IonReactRouter>

_45

<IonRouterOutlet>

_45

<Route

_45

exact

_45

path="/"

_45

render={() => {

_45

return session ? <Redirect to="/account" /> : <LoginPage />

_45

}}

_45

/>

_45

<Route exact path="/account">

_45

<AccountPage />

_45

</Route>

_45

</IonRouterOutlet>

_45

</IonReactRouter>

_45

</IonApp>

_45

)

_45

}

_45

_45

export default App

  
`

Once that's done, run this in a terminal window:

`  

_10

ionic serve

  
`

And then open the browser to [localhost:3000](http://localhost:3000) and you
should see the completed app.

![Supabase Ionic React](/docs/img/ionic-demos/ionic-react.png)

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

With those packages installed we can update our `index.tsx` to include an
additional bootstrapping call for the Ionic PWA Elements.

src/index.tsx

`  

_18

import React from 'react'

_18

import ReactDOM from 'react-dom'

_18

import App from './App'

_18

import * as serviceWorkerRegistration from './serviceWorkerRegistration'

_18

import reportWebVitals from './reportWebVitals'

_18

_18

import { defineCustomElements } from '@ionic/pwa-elements/loader'

_18

defineCustomElements(window)

_18

_18

ReactDOM.render(

_18

<React.StrictMode>

_18

<App />

_18

</React.StrictMode>,

_18

document.getElementById('root')

_18

)

_18

_18

serviceWorkerRegistration.unregister()

_18

reportWebVitals()

  
`

Then create an **AvatarComponent**.

src/components/Avatar.tsx

`  

_76

import { IonIcon } from '@ionic/react';

_76

import { person } from 'ionicons/icons';

_76

import { Camera, CameraResultType } from '@capacitor/camera';

_76

import { useEffect, useState } from 'react';

_76

import { supabase } from '../supabaseClient';

_76

import './Avatar.css'

_76

export function Avatar({

_76

url,

_76

onUpload,

_76

}: {

_76

url: string;

_76

onUpload: (e: any, file: string) => Promise<void>;

_76

}) {

_76

const [avatarUrl, setAvatarUrl] = useState<string | undefined>();

_76

_76

useEffect(() => {

_76

if (url) {

_76

downloadImage(url);

_76

}

_76

}, [url]);

_76

const uploadAvatar = async () => {

_76

try {

_76

const photo = await Camera.getPhoto({

_76

resultType: CameraResultType.DataUrl,

_76

});

_76

_76

const file = await fetch(photo.dataUrl!)

_76

.then((res) => res.blob())

_76

.then(

_76

(blob) =>

_76

new File([blob], 'my-file', { type: `image/${photo.format}` })

_76

);

_76

_76

const fileName = `${Math.random()}-${new Date().getTime()}.${

_76

photo.format

_76

}`;

_76

const { error: uploadError } = await supabase.storage

_76

.from('avatars')

_76

.upload(fileName, file);

_76

if (uploadError) {

_76

throw uploadError;

_76

}

_76

onUpload(null, fileName);

_76

} catch (error) {

_76

console.log(error);

_76

}

_76

};

_76

_76

const downloadImage = async (path: string) => {

_76

try {

_76

const { data, error } = await supabase.storage

_76

.from('avatars')

_76

.download(path);

_76

if (error) {

_76

throw error;

_76

}

_76

const url = URL.createObjectURL(data!);

_76

setAvatarUrl(url);

_76

} catch (error: any) {

_76

console.log('Error downloading image: ', error.message);

_76

}

_76

};

_76

_76

return (

_76

<div className="avatar">

_76

<div className="avatar_wrapper" onClick={uploadAvatar}>

_76

{avatarUrl ? (

_76

<img src={avatarUrl} />

_76

) : (

_76

<IonIcon icon={person} className="no-avatar" />

_76

)}

_76

</div>

_76

_76

</div>

_76

);

_76

}

  
`

### Add the new widget#

And then we can add the widget to the Account page:

src/pages/Account.tsx

`  

_15

// Import the new component

_15

_15

import { Avatar } from '../components/Avatar';

_15

_15

// ...

_15

return (

_15

<IonPage>

_15

<IonHeader>

_15

<IonToolbar>

_15

<IonTitle>Account</IonTitle>

_15

</IonToolbar>

_15

</IonHeader>

_15

_15

<IonContent>

_15

<Avatar url={profile.avatar_url} onUpload={updateProfile}></Avatar>

  
`

At this stage you have a fully functional application!

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/content/guides/getting-
started/tutorials/with-ionic-react.mdx)

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

