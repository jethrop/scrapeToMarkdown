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
  4.   5. [Social Login (OAuth)](/docs/guides/auth/social-login)
  6.   7. [Slack](/docs/guides/auth/social-login/auth-slack)
  8. 

# Login with Slack

* * *

To enable Slack Auth for your project, you need to set up a Slack OAuth
application and add the application credentials to your Supabase Dashboard.

## Overview#

We will be replacing the existing Slack provider with a new Slack (OIDC)
provider. Developers with Slack OAuth Applications created prior to 24th June
2024 should create a new application and migrate their credentials from the
Slack provider to the Slack (OIDC) provider. Existing OAuth Applications built
with the old Slack provider will continue to work up till 10th October. You
can refer to the [**list of supported
scopes**](https://api.slack.com/scopes?filter=user) for the new Slack (OIDC)
User.

Setting up Slack logins for your application consists of 3 parts:

  * Create and configure a Slack Project and App on the [Slack Developer Dashboard](https://api.slack.com/apps).
  * Add your Slack `API Key` and `API Secret Key` to your [Supabase Project](https://supabase.com/dashboard).
  * Add the login code to your [Supabase JS Client App](https://github.com/supabase/supabase-js).

## Access your Slack Developer account#

  * Go to [api.slack.com](https://api.slack.com/apps).
  * Click on `Your Apps` at the top right to log in.

![Slack Developer Portal.](/docs/img/guides/auth-slack/slack-portal.png)

## Find your callback URL#

The next step requires a callback URL, which looks like this:
`https://<project-ref>.supabase.co/auth/v1/callback`

  * Go to your [Supabase Project Dashboard](https://supabase.com/dashboard)
  * Click on the `Authentication` icon in the left sidebar
  * Click on [`Providers`](https://supabase.com/dashboard/project/_/auth/providers) under the Configuration section
  * Click on **Slack** from the accordion list to expand and you'll find your **Callback URL** , you can click `Copy` to copy it to the clipboard

For testing OAuth locally with the Supabase CLI please see the [local
development docs](/docs/guides/cli/local-development#use-auth-locally).

## Create a Slack OAuth app#

  * Go to [api.slack.com](https://api.slack.com/apps).
  * Click on `Create New App`

Under `Create an app...`:

  * Click `From scratch`
  * Type the name of your app
  * Select your `Slack Workspace`
  * Click `Create App`

Under `App Credentials`:

  * Copy and save your newly-generated `Client ID`
  * Copy and save your newly-generated `Client Secret`

Under the sidebar, select `OAuth & Permissions` and look for `Redirect URLs`:

  * Click `Add New Redirect URL`
  * Paste your `Callback URL` then click `Add`
  * Click `Save URLs`

Under `Scopes`:

  * Add the following scopes under the `User Token Scopes`: `profile`, `email`, `openid`. These scopes are the default scopes that Supabase Auth uses to request for user information. Do not add other scopes as [Sign In With Slack only supports `profile`, `email`, `openid`](https://api.slack.com/authentication/sign-in-with-slack#request).

## Enter your Slack credentials into your Supabase project#

  * Go to your [Supabase Project Dashboard](https://supabase.com/dashboard)
  * In the left sidebar, click the `Authentication` icon (near the top)
  * Click on [`Providers`](https://supabase.com/dashboard/project/_/auth/providers) under the Configuration section
  * Click on **Slack** from the accordion list to expand and turn **Slack Enabled** to ON
  * Enter your **Slack Client ID** and **Slack Client Secret** saved in the previous step
  * Click `Save`

## Add login code to your client app#

JavaScriptFlutterKotlin

Make sure you're using the right `supabase` client in the following code.

If you're not using Server-Side Rendering or cookie-based Auth, you can
directly use the `createClient` from `@supabase/supabase-js`. If you're using
Server-Side Rendering, see the [Server-Side Auth
guide](/docs/guides/auth/server-side/creating-a-client) for instructions on
creating your Supabase client.

When your user signs in, call
[signInWithOAuth()](/docs/reference/javascript/auth-signinwithoauth) with
`slack_oidc` as the `provider`:

`  

_10

async function signInWithSlack() {

_10

const { data, error } = await supabase.auth.signInWithOAuth({

_10

provider: 'slack_oidc',

_10

})

_10

}

  
`

For a PKCE flow, for example in Server-Side Auth, you need an extra step to
handle the code exchange. When calling `signInWithOAuth`, provide a
`redirectTo` URL which points to a callback route. This redirect URL should be
added to your [redirect allow list](/docs/guides/auth/redirect-urls).

ClientServer

In the browser, `signInWithOAuth` automatically redirects to the OAuth
provider's authentication endpoint, which then redirects to your endpoint.

`  

_10

await supabase.auth.signInWithOAuth({

_10

provider,

_10

options: {

_10

redirectTo: `http://example.com/auth/callback`,

_10

},

_10

})

  
`

At the callback endpoint, handle the code exchange to save the user session.

Next.jsSvelteKitAstroRemixExpress

Create a new file at `app/auth/callback/route.ts` and populate with the
following:

app/auth/callback/route.ts

`  

_30

import { NextResponse } from 'next/server'

_30

// The client you created from the Server-Side Auth instructions

_30

import { createClient } from '@/utils/supabase/server'

_30

_30

export async function GET(request: Request) {

_30

const { searchParams, origin } = new URL(request.url)

_30

const code = searchParams.get('code')

_30

// if "next" is in param, use it as the redirect URL

_30

const next = searchParams.get('next') ?? '/'

_30

_30

if (code) {

_30

const supabase = createClient()

_30

const { error } = await supabase.auth.exchangeCodeForSession(code)

_30

if (!error) {

_30

const forwardedHost = request.headers.get('x-forwarded-host') // original
origin before load balancer

_30

const isLocalEnv = process.env.NODE_ENV === 'development'

_30

if (isLocalEnv) {

_30

// we can be sure that there is no load balancer in between, so no need to
watch for X-Forwarded-Host

_30

return NextResponse.redirect(`${origin}${next}`)

_30

} else if (forwardedHost) {

_30

return NextResponse.redirect(`https://${forwardedHost}${next}`)

_30

} else {

_30

return NextResponse.redirect(`${origin}${next}`)

_30

}

_30

}

_30

}

_30

_30

// return the user to an error page with instructions

_30

return NextResponse.redirect(`${origin}/auth/auth-code-error`)

_30

}

  
`

JavaScriptFlutterKotlin

When your user signs out, call [signOut()](/docs/reference/javascript/auth-
signout) to remove them from the browser session and any objects from
localStorage:

`  

_10

async function signOut() {

_10

const { error } = await supabase.auth.signOut()

_10

}

  
`

## Resources#

  * [Supabase - Get started for free](https://supabase.com)
  * [Supabase JS Client](https://github.com/supabase/supabase-js)
  * [Slack Developer Dashboard](https://api.slack.com/apps)

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/content/guides/auth/social-
login/auth-slack.mdx)

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

