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
  4.   5. [Ionic Angular](/docs/guides/getting-started/tutorials/with-ionic-angular)
  6. 

# Build a User Management App with Ionic Angular

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
on GitHub](https://github.com/mhartington/supabase-ionic-angular).

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

Let's start building the Angular app from scratch.

### Initialize an Ionic Angular app#

We can use the [Ionic CLI](https://ionicframework.com/docs/cli) to initialize
an app called `supabase-ionic-angular`:

`  

_10

npm install -g @ionic/cli

_10

ionic start supabase-ionic-angular blank --type angular

_10

cd supabase-ionic-angular

  
`

Then let's install the only additional dependency: [supabase-
js](https://github.com/supabase/supabase-js)

`  

_10

npm install @supabase/supabase-js

  
`

And finally, we want to save the environment variables in the
`src/environments/environment.ts` file. All we need are the API URL and the
`anon` key that you copied earlier. These variables will be exposed on the
browser, and that's completely fine since we have [Row Level
Security](/docs/guides/auth#row-level-security) enabled on our Database.

environment.ts

`  

_10

export const environment = {

_10

production: false,

_10

supabaseUrl: 'YOUR_SUPABASE_URL',

_10

supabaseKey: 'YOUR_SUPABASE_KEY',

_10

}

  
`

Now that we have the API credentials in place, let's create a
**SupabaseService** with `ionic g s supabase` to initialize the Supabase
client and implement functions to communicate with the Supabase API.

src/app/supabase.service.ts

`  

_80

import { Injectable } from '@angular/core'

_80

import { LoadingController, ToastController } from '@ionic/angular'

_80

import { AuthChangeEvent, createClient, Session, SupabaseClient } from
'@supabase/supabase-js'

_80

import { environment } from '../environments/environment'

_80

_80

export interface Profile {

_80

username: string

_80

website: string

_80

avatar_url: string

_80

}

_80

_80

@Injectable({

_80

providedIn: 'root',

_80

})

_80

export class SupabaseService {

_80

private supabase: SupabaseClient

_80

_80

constructor(

_80

private loadingCtrl: LoadingController,

_80

private toastCtrl: ToastController

_80

) {

_80

this.supabase = createClient(environment.supabaseUrl, environment.supabaseKey)

_80

}

_80

_80

get user() {

_80

return this.supabase.auth.getUser().then(({ data }) => data?.user)

_80

}

_80

_80

get session() {

_80

return this.supabase.auth.getSession().then(({ data }) => data?.session)

_80

}

_80

_80

get profile() {

_80

return this.user

_80

.then((user) => user?.id)

_80

.then((id) =>

_80

this.supabase.from('profiles').select(`username, website,
avatar_url`).eq('id', id).single()

_80

)

_80

}

_80

_80

authChanges(callback: (event: AuthChangeEvent, session: Session | null) => void) {

_80

return this.supabase.auth.onAuthStateChange(callback)

_80

}

_80

_80

signIn(email: string) {

_80

return this.supabase.auth.signInWithOtp({ email })

_80

}

_80

_80

signOut() {

_80

return this.supabase.auth.signOut()

_80

}

_80

_80

async updateProfile(profile: Profile) {

_80

const user = await this.user

_80

const update = {

_80

...profile,

_80

id: user?.id,

_80

updated_at: new Date(),

_80

}

_80

_80

return this.supabase.from('profiles').upsert(update)

_80

}

_80

_80

downLoadImage(path: string) {

_80

return this.supabase.storage.from('avatars').download(path)

_80

}

_80

_80

uploadAvatar(filePath: string, file: File) {

_80

return this.supabase.storage.from('avatars').upload(filePath, file)

_80

}

_80

_80

async createNotice(message: string) {

_80

const toast = await this.toastCtrl.create({ message, duration: 5000 })

_80

await toast.present()

_80

}

_80

_80

createLoader() {

_80

return this.loadingCtrl.create()

_80

}

_80

}

  
`

### Set up a login route#

Let's set up a route to manage logins and signups. We'll use Magic Links so
users can sign in with their email without using passwords. Create a
**LoginPage** with the `ionic g page login` Ionic CLI command.

This guide will show the template inline, but the example app will have
`templateUrl`s

src/app/login/login.page.ts

`  

_54

import { Component, OnInit } from '@angular/core'

_54

import { SupabaseService } from '../supabase.service'

_54

_54

@Component({

_54

selector: 'app-login',

_54

template: `

_54

<ion-header>

_54

<ion-toolbar>

_54

<ion-title>Login</ion-title>

_54

</ion-toolbar>

_54

</ion-header>

_54

_54

<ion-content>

_54

<div class="ion-padding">

_54

<h1>Supabase + Ionic Angular</h1>

_54

<p>Sign in via magic link with your email below</p>

_54

</div>

_54

<ion-list inset="true">

_54

<form (ngSubmit)="handleLogin($event)">

_54

<ion-item>

_54

<ion-label position="stacked">Email</ion-label>

_54

<ion-input [(ngModel)]="email" name="email" autocomplete type="email"></ion-
input>

_54

</ion-item>

_54

<div class="ion-text-center">

_54

<ion-button type="submit" fill="clear">Login</ion-button>

_54

</div>

_54

</form>

_54

</ion-list>

_54

</ion-content>

_54

`,

_54

styleUrls: ['./login.page.scss'],

_54

})

_54

export class LoginPage {

_54

email = ''

_54

_54

constructor(private readonly supabase: SupabaseService) {}

_54

_54

async handleLogin(event: any) {

_54

event.preventDefault()

_54

const loader = await this.supabase.createLoader()

_54

await loader.present()

_54

try {

_54

const { error } = await this.supabase.signIn(this.email)

_54

if (error) {

_54

throw error

_54

}

_54

await loader.dismiss()

_54

await this.supabase.createNotice('Check your email for the login link!')

_54

} catch (error: any) {

_54

await loader.dismiss()

_54

await this.supabase.createNotice(error.error_description || error.message)

_54

}

_54

}

_54

}

  
`

### Account page#

After a user is signed in, we can allow them to edit their profile details and
manage their account. Create an **AccountComponent** with `ionic g page
account` Ionic CLI command.

src/app/account.page.ts

`  

_99

import { Component, OnInit } from '@angular/core'

_99

import { Router } from '@angular/router'

_99

import { Profile, SupabaseService } from '../supabase.service'

_99

_99

@Component({

_99

selector: 'app-account',

_99

template: `

_99

<ion-header>

_99

<ion-toolbar>

_99

<ion-title>Account</ion-title>

_99

</ion-toolbar>

_99

</ion-header>

_99

_99

<ion-content>

_99

<form>

_99

<ion-item>

_99

<ion-label position="stacked">Email</ion-label>

_99

<ion-input type="email" name="email" [(ngModel)]="email" readonly></ion-input>

_99

</ion-item>

_99

_99

<ion-item>

_99

<ion-label position="stacked">Name</ion-label>

_99

<ion-input type="text" name="username" [(ngModel)]="profile.username"></ion-
input>

_99

</ion-item>

_99

_99

<ion-item>

_99

<ion-label position="stacked">Website</ion-label>

_99

<ion-input type="url" name="website" [(ngModel)]="profile.website"></ion-
input>

_99

</ion-item>

_99

<div class="ion-text-center">

_99

<ion-button fill="clear" (click)="updateProfile()">Update Profile</ion-button>

_99

</div>

_99

</form>

_99

_99

<div class="ion-text-center">

_99

<ion-button fill="clear" (click)="signOut()">Log Out</ion-button>

_99

</div>

_99

</ion-content>

_99

`,

_99

styleUrls: ['./account.page.scss'],

_99

})

_99

export class AccountPage implements OnInit {

_99

profile: Profile = {

_99

username: '',

_99

avatar_url: '',

_99

website: '',

_99

}

_99

_99

email = ''

_99

_99

constructor(

_99

private readonly supabase: SupabaseService,

_99

private router: Router

_99

) {}

_99

ngOnInit() {

_99

this.getEmail()

_99

this.getProfile()

_99

}

_99

_99

async getEmail() {

_99

this.email = await this.supabase.user.then((user) => user?.email || '')

_99

}

_99

_99

async getProfile() {

_99

try {

_99

const { data: profile, error, status } = await this.supabase.profile

_99

if (error && status !== 406) {

_99

throw error

_99

}

_99

if (profile) {

_99

this.profile = profile

_99

}

_99

} catch (error: any) {

_99

alert(error.message)

_99

}

_99

}

_99

_99

async updateProfile(avatar_url: string = '') {

_99

const loader = await this.supabase.createLoader()

_99

await loader.present()

_99

try {

_99

const { error } = await this.supabase.updateProfile({ ...this.profile,
avatar_url })

_99

if (error) {

_99

throw error

_99

}

_99

await loader.dismiss()

_99

await this.supabase.createNotice('Profile updated!')

_99

} catch (error: any) {

_99

await loader.dismiss()

_99

await this.supabase.createNotice(error.message)

_99

}

_99

}

_99

_99

async signOut() {

_99

console.log('testing?')

_99

await this.supabase.signOut()

_99

this.router.navigate(['/'], { replaceUrl: true })

_99

}

_99

}

  
`

### Launch!#

Now that we have all the components in place, let's update **AppComponent** :

src/app/app.component.ts

`  

_26

import { Component } from '@angular/core'

_26

import { Router } from '@angular/router'

_26

import { SupabaseService } from './supabase.service'

_26

_26

@Component({

_26

selector: 'app-root',

_26

template: `

_26

<ion-app>

_26

<ion-router-outlet></ion-router-outlet>

_26

</ion-app>

_26

`,

_26

styleUrls: ['app.component.scss'],

_26

})

_26

export class AppComponent {

_26

constructor(

_26

private supabase: SupabaseService,

_26

private router: Router

_26

) {

_26

this.supabase.authChanges((_, session) => {

_26

console.log(session)

_26

if (session?.user) {

_26

this.router.navigate(['/account'])

_26

}

_26

})

_26

}

_26

}

  
`

Then update the **AppRoutingModule**

src/app/app-routing.module.ts"

`  

_23

import { NgModule } from '@angular/core'

_23

import { PreloadAllModules, RouterModule, Routes } from '@angular/router'

_23

_23

const routes: Routes = [

_23

{

_23

path: '',

_23

loadChildren: () => import('./login/login.module').then((m) =>
m.LoginPageModule),

_23

},

_23

{

_23

path: 'account',

_23

loadChildren: () => import('./account/account.module').then((m) =>
m.AccountPageModule),

_23

},

_23

]

_23

_23

@NgModule({

_23

imports: [

_23

RouterModule.forRoot(routes, {

_23

preloadingStrategy: PreloadAllModules,

_23

}),

_23

],

_23

exports: [RouterModule],

_23

})

_23

export class AppRoutingModule {}

  
`

Once that's done, run this in a terminal window:

`  

_10

ionic serve

  
`

And the browser will automatically open to show the app.

![Supabase Angular](/docs/img/ionic-demos/ionic-angular.png)

## Bonus: Profile photos#

Every Supabase project is configured with [Storage](/docs/guides/storage) for
managing large files like photos and videos.

### Create an upload widget#

Let's create an avatar for the user so that they can upload a profile photo.

First, install two packages in order to interact with the user's camera.

`  

_10

npm install @ionic/pwa-elements @capacitor/camera

  
`

[CapacitorJS](https://capacitorjs.com) is a cross-platform native runtime from
Ionic that enables web apps to be deployed through the app store and provides
access to native device API.

Ionic PWA elements is a companion package that will polyfill certain browser
APIs that provide no user interface with custom Ionic UI.

With those packages installed, we can update our `main.ts` to include an
additional bootstrapping call for the Ionic PWA Elements.

src/main.ts

`  

_15

import { enableProdMode } from '@angular/core'

_15

import { platformBrowserDynamic } from '@angular/platform-browser-dynamic'

_15

_15

import { AppModule } from './app/app.module'

_15

import { environment } from './environments/environment'

_15

_15

import { defineCustomElements } from '@ionic/pwa-elements/loader'

_15

defineCustomElements(window)

_15

_15

if (environment.production) {

_15

enableProdMode()

_15

}

_15

platformBrowserDynamic()

_15

.bootstrapModule(AppModule)

_15

.catch((err) => console.log(err))

  
`

Then create an **AvatarComponent** with this Ionic CLI command:

`  

_10

ionic g component avatar --module=/src/app/account/account.module.ts --create-
module

  
`

src/app/avatar.component.ts

`  

_108

import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core'

_108

import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser'

_108

import { SupabaseService } from '../supabase.service'

_108

import { Camera, CameraResultType } from '@capacitor/camera'

_108

import { addIcons } from 'ionicons'

_108

import { person } from 'ionicons/icons'

_108

@Component({

_108

selector: 'app-avatar',

_108

template: `

_108

<div class="avatar_wrapper" (click)="uploadAvatar()">

_108

<img *ngIf="_avatarUrl; else noAvatar" [src]="_avatarUrl" />

_108

<ng-template #noAvatar>

_108

<ion-icon name="person" class="no-avatar"></ion-icon>

_108

</ng-template>

_108

</div>

_108

`,

_108

style: [

_108

`

_108

:host {

_108

display: block;

_108

margin: auto;

_108

min-height: 150px;

_108

}

_108

:host .avatar_wrapper {

_108

margin: 16px auto 16px;

_108

border-radius: 50%;

_108

overflow: hidden;

_108

height: 150px;

_108

aspect-ratio: 1;

_108

background: var(--ion-color-step-50);

_108

border: thick solid var(--ion-color-step-200);

_108

}

_108

:host .avatar_wrapper:hover {

_108

cursor: pointer;

_108

}

_108

:host .avatar_wrapper ion-icon.no-avatar {

_108

width: 100%;

_108

height: 115%;

_108

}

_108

:host img {

_108

display: block;

_108

object-fit: cover;

_108

width: 100%;

_108

height: 100%;

_108

}

_108

`,

_108

],

_108

})

_108

export class AvatarComponent {

_108

_avatarUrl: SafeResourceUrl | undefined

_108

uploading = false

_108

_108

@Input()

_108

set avatarUrl(url: string | undefined) {

_108

if (url) {

_108

this.downloadImage(url)

_108

}

_108

}

_108

_108

@Output() upload = new EventEmitter<string>()

_108

_108

constructor(

_108

private readonly supabase: SupabaseService,

_108

private readonly dom: DomSanitizer

_108

) {

_108

addIcons({ person })

_108

}

_108

_108

async downloadImage(path: string) {

_108

try {

_108

const { data, error } = await this.supabase.downLoadImage(path)

_108

if (error) {

_108

throw error

_108

}

_108

this._avatarUrl =
this.dom.bypassSecurityTrustResourceUrl(URL.createObjectURL(data!))

_108

} catch (error: any) {

_108

console.error('Error downloading image: ', error.message)

_108

}

_108

}

_108

_108

async uploadAvatar() {

_108

const loader = await this.supabase.createLoader()

_108

try {

_108

const photo = await Camera.getPhoto({

_108

resultType: CameraResultType.DataUrl,

_108

})

_108

_108

const file = await fetch(photo.dataUrl!)

_108

.then((res) => res.blob())

_108

.then((blob) => new File([blob], 'my-file', { type: `image/${photo.format}`
}))

_108

_108

const fileName = `${Math.random()}-${new Date().getTime()}.${photo.format}`

_108

_108

await loader.present()

_108

const { error } = await this.supabase.uploadAvatar(fileName, file)

_108

_108

if (error) {

_108

throw error

_108

}

_108

_108

this.upload.emit(fileName)

_108

} catch (error: any) {

_108

this.supabase.createNotice(error.message)

_108

} finally {

_108

loader.dismiss()

_108

}

_108

}

_108

}

  
`

### Add the new widget#

And then, we can add the widget on top of the **AccountComponent** HTML
template:

src/app/account.component.ts

`  

_15

template: `

_15

<ion-header>

_15

<ion-toolbar>

_15

<ion-title>Account</ion-title>

_15

</ion-toolbar>

_15

</ion-header>

_15

_15

<ion-content>

_15

<app-avatar

_15

[avatarUrl]="this.profile?.avatar_url"

_15

(upload)="updateProfile($event)"

_15

></app-avatar>

_15

_15

<!-- input fields -->

_15

`

  
`

At this stage, you have a fully functional application!

## See also#

  * [Authentication in Ionic Angular with Supabase](https://supabase.com/blog/authentication-in-ionic-angular)

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/content/guides/getting-
started/tutorials/with-ionic-angular.mdx)

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

