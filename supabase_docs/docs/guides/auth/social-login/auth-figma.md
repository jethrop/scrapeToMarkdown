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
  6.   7. [Figma](/docs/guides/auth/social-login/auth-figma)
  8. 

# Login with Figma

* * *

To enable Figma Auth for your project, you need to set up a Figma OAuth
application and add the application credentials to your Supabase Dashboard.

## Overview#

Setting up Figma logins for your application consists of 3 parts:

  * Create and configure a Figma App on the [Figma Developers page](https://www.figma.com/developers).
  * Add your Figma `client_id` and `client_secret` to your [Supabase Project](https://app.supabase.com).
  * Add the login code to your [Supabase JS Client App](https://github.com/supabase/supabase-js).

## Access the Figma Developers page#

  * Go to the [Figma Developers page](https://www.figma.com/developers)
  * Click on `My apps` at the top right
  * Log in (if necessary)

![Figma Developers page](/docs/img/guides/auth-
figma/figma_developers_page.png)

## Find your callback URL#

The next step requires a callback URL, which looks like this:
`https://<project-ref>.supabase.co/auth/v1/callback`

  * Go to your [Supabase Project Dashboard](https://supabase.com/dashboard)
  * Click on the `Authentication` icon in the left sidebar
  * Click on [`Providers`](https://supabase.com/dashboard/project/_/auth/providers) under the Configuration section
  * Click on **Figma** from the accordion list to expand and you'll find your **Callback URL** , you can click `Copy` to copy it to the clipboard

For testing OAuth locally with the Supabase CLI please see the [local
development docs](/docs/guides/cli/local-development#use-auth-locally).

## Create a Figma OAuth app#

  * Enter your `App name`, `Website URL` and upload your app logo
  * Click on `Add callback`
  * Add your `Callback URL`
  * Click on `Save`

![Create Figma app](/docs/img/guides/auth-figma/figma_create_app.png)

  * Copy and save your newly-generated `Client ID`
  * Copy and save your newly-generated `Client Secret`

![Get Figma app credentials](/docs/img/guides/auth-
figma/figma_app_credentials.png)

## Enter your Figma credentials into your Supabase project#

  * Go to your [Supabase Project Dashboard](https://supabase.com/dashboard)
  * In the left sidebar, click the `Authentication` icon (near the top)
  * Click on [`Providers`](https://supabase.com/dashboard/project/_/auth/providers) under the Configuration section
  * Click on **Figma** from the accordion list to expand and turn **Figma Enabled** to ON
  * Enter your **Figma Client ID** and **Figma Client Secret** saved in the previous step
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
`figma` as the `provider`:

`  

_10

async function signInWithFigma() {

_10

const { data, error } = await supabase.auth.signInWithOAuth({

_10

provider: 'figma',

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
  * [Figma Developers page](https://www.figma.com/developers)

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/content/guides/auth/social-
login/auth-figma.mdx)

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

