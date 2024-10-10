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
  6.   7. [Notion](/docs/guides/auth/social-login/auth-notion)
  8. 

# Login with Notion

* * *

To enable Notion Auth for your project, you need to set up a Notion
Application and add the Application OAuth credentials to your Supabase
Dashboard.

## Overview#

Setting up Notion logins for your application consists of 3 parts:

  * Create and configure a Notion Application [Notion Developer Portal](https://www.notion.so/my-integrations)
  * Retrieve your OAuth client ID and OAuth client secret and add them to your [Supabase Project](https://supabase.com/dashboard)
  * Add the login code to your [Supabase JS Client App](https://github.com/supabase/supabase-js)

## Create your notion integration#

  * Go to [developers.notion.com](https://developers.notion.com/).
  * Click "View my integrations" and login.

![notion.so](/docs/img/guides/auth-notion/notion.png)

  * Once logged in, go to [notion.so/my-integrations](https://notion.so/my-integrations) and create a new integration.
  * When creating your integration, ensure that you select "Public integration" under "Integration type" and "Read user information including email addresses" under "Capabilities".
  * You will need to add a redirect uri, see Add the redirect uri
  * Once you've filled in the necessary fields, click "Submit" to finish creating the integration.

![notion.so](/docs/img/guides/auth-notion/notion-developer.png)

## Add the redirect URI#

  * After selecting "Public integration", you should see an option to add "Redirect URIs".

![notion.so](/docs/img/guides/auth-notion/notion-redirect-uri.png)

The next step requires a callback URL, which looks like this:
`https://<project-ref>.supabase.co/auth/v1/callback`

  * Go to your [Supabase Project Dashboard](https://supabase.com/dashboard)
  * Click on the `Authentication` icon in the left sidebar
  * Click on [`Providers`](https://supabase.com/dashboard/project/_/auth/providers) under the Configuration section
  * Click on **Notion** from the accordion list to expand and you'll find your **Callback URL** , you can click `Copy` to copy it to the clipboard

For testing OAuth locally with the Supabase CLI please see the [local
development docs](/docs/guides/cli/local-development#use-auth-locally).

## Add your Notion credentials into your Supabase project#

  * Once you've created your notion integration, you should be able to retrieve the "OAuth client ID" and "OAuth client secret" from the "OAuth Domain and URIs" tab.

![notion.so](/docs/img/guides/auth-notion/notion-creds.png)

  * Go to your [Supabase Project Dashboard](https://supabase.com/dashboard)
  * In the left sidebar, click the `Authentication` icon (near the top)
  * Click on [`Providers`](https://supabase.com/dashboard/project/_/auth/providers) under the Configuration section
  * Click on **Notion** from the accordion list to expand and turn **Notion Enabled** to ON
  * Enter your **Notion Client ID** and **Notion Client Secret** saved in the previous step
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
`notion` as the `provider`:

`  

_10

async function signInWithNotion() {

_10

const { data, error } = await supabase.auth.signInWithOAuth({

_10

provider: 'notion',

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
  * [Notion Account](https://notion.so)
  * [Notion Developer Portal](https://www.notion.so/my-integrations)

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/content/guides/auth/social-
login/auth-notion.mdx)

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

