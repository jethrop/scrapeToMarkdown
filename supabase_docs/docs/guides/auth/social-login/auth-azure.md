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
  6.   7. [Azure (Microsoft)](/docs/guides/auth/social-login/auth-azure)
  8. 

# Login with Azure (Microsoft)

* * *

To enable Azure (Microsoft) Auth for your project, you need to set up an Azure
OAuth application and add the application credentials to your Supabase
Dashboard.

## Overview#

Setting up OAuth with Azure consists of four broad steps:

  * Create an OAuth application under Azure Entra ID.
  * Add a secret to the application.
  * Add the Supabase Auth callback URL to the allowlist in the OAuth application in Azure.
  * Configure the client ID and secret of the OAuth application within the Supabase Auth dashboard.

## Access your Azure Developer account#

  * Go to [portal.azure.com](https://portal.azure.com/#home).
  * Login and select Microsoft Entra ID under the list of Azure Services.

## Register an application#

  * Under Microsoft Entra ID, select _App registrations_ in the side panel and select _New registration._
  * Choose a name and select your preferred option for the supported account types.
  * Specify a _Web_ _Redirect URI_. It should should look like this: `https://<project-ref>.supabase.co/auth/v1/callback`
  * Finally, select _Register_ at the bottom of the screen.

![Register an application.](/docs/img/guides/auth-azure/azure-register-
app.png)

## Obtain a client ID and secret#

  * Once your app has been registered, the client ID can be found under the [list of app registrations](https://portal.azure.com/#blade/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/RegisteredApps) under the column titled _Application (client) ID_.
  * You can also find it in the app overview screen.
  * Place the Client ID in the Azure configuration screen in the Supabase Auth dashboard.

![Obtain the client ID](/docs/img/guides/auth-azure/azure-client-id.png)

  * Select _Add a certificate or secret_ in the app overview screen and open the _Client secrets_ tab.
  * Select _New client secret_ to create a new client secret.
  * Choose a preferred expiry time of the secret. Make sure you record this in your calendar days in advance so you have enough time to create a new one without suffering from any downtime.
  * Once the secret is generated place the _Value_ column (not _Secret ID_) in the Azure configuration screen in the Supabase Auth dashboard.

![Obtain the client secret](/docs/img/guides/auth-azure/azure-client-
secret.png)

## Guarding against unverified email domains#

Microsoft Entra ID can send out unverified email domains in certain cases.
This may open up your project to a vulnerability where a malicious user can
impersonate already existing accounts on your project.

This only applies in at least one of these cases:

  * You have configured the `authenticationBehaviors` setting of your OAuth application to allow unverified email domains
  * You are using an OAuth app configured as single-tenant in the supported account types
  * Your OAuth app was created before June 20th 2023 after Microsoft announced this vulnerability, and the app had used unverified emails prior

This means that most OAuth apps _are not susceptible_ to this vulnerability.

Despite this, we recommend configuring the [optional `xms_edov`
claim](https://learn.microsoft.com/en-us/azure/active-
directory/develop/migrate-off-email-claim-authorization#using-the-xms_edov-
optional-claim-to-determine-email-verification-status-and-migrate-users) on
the OAuth app. This claim allows Supabase Auth to identify with certainty
whether the email address sent over by Microsoft Entra ID is verified or not.

Configure this in the following way:

  * Select the _App registrations_ menu in Microsoft Entra ID on the Azure portal.
  * Select the OAuth app.
  * Select the _Manifest_ menu in the sidebar.
  * Make a backup of the JSON just in case.
  * Identify the `optionalClaims` key.
  * Edit it by specifying the following object:

`  

_25

"optionalClaims": {

_25

"idToken": [

_25

{

_25

"name": "xms_edov",

_25

"source": null,

_25

"essential": false,

_25

"additionalProperties": []

_25

},

_25

{

_25

"name": "email",

_25

"source": null,

_25

"essential": false,

_25

"additionalProperties": []

_25

}

_25

],

_25

"accessToken": [

_25

{

_25

"name": "xms_edov",

_25

"source": null,

_25

"essential": false,

_25

"additionalProperties": []

_25

}

_25

],

_25

"saml2Token": []

_25

},

  
`

  * Select _Save_ to apply the new configuration.

## Configure a tenant URL (optional)#

A Microsoft Entra tenant is the directory of users who are allowed to access
your project. This section depends on what your OAuth registration uses for
_Supported account types._

By default, Supabase Auth uses the _common_ Microsoft tenant
(`https://login.microsoftonline.com/common`) which generally allows any
Microsoft account to sign in to your project. Microsoft Entra further limits
what accounts can access your project depending on the type of OAuth
application you registered.

If your app is registered as _Personal Microsoft accounts only_ for the
_Supported account types_ set Microsoft tenant to _consumers_
(`https://login.microsoftonline.com/consumers`).

If your app is registered as _My organization only_ for the _Supported account
types_ you may want to configure Supabase Auth with the organization's tenant
URL. This will use the tenant's authorization flows instead, and will limit
access at the Supabase Auth level to Microsoft accounts arising from only the
specified tenant.

Configure this by storing a value under _Azure Tenant URL_ in the Supabase
Auth provider configuration page for Azure that has the following format
`https://login.microsoftonline.com/<tenant-id>`.

## Add login code to your client app#

Supabase Auth requires that Azure returns a valid email address. Therefore you
must request the `email` scope in the `signInWithOAuth` method.

JavaScriptFlutterKotlin

Make sure you're using the right `supabase` client in the following code.

If you're not using Server-Side Rendering or cookie-based Auth, you can
directly use the `createClient` from `@supabase/supabase-js`. If you're using
Server-Side Rendering, see the [Server-Side Auth
guide](/docs/guides/auth/server-side/creating-a-client) for instructions on
creating your Supabase client.

When your user signs in, call
[signInWithOAuth()](/docs/reference/javascript/auth-signinwithoauth) with
`azure` as the `provider`:

`  

_10

async function signInWithAzure() {

_10

const { data, error } = await supabase.auth.signInWithOAuth({

_10

provider: 'azure',

_10

options: {

_10

scopes: 'email',

_10

},

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

## Obtain the provider refresh token#

Azure OAuth2.0 doesn't return the `provider_refresh_token` by default. If you
need the `provider_refresh_token` returned, you will need to include the
following scope:

JavaScriptFlutterKotlin

`  

_10

async function signInWithAzure() {

_10

const { data, error } = await supabase.auth.signInWithOAuth({

_10

provider: 'azure',

_10

options: {

_10

scopes: 'offline_access',

_10

},

_10

})

_10

}

  
`

## Resources#

  * [Azure Developer Account](https://portal.azure.com)
  * [GitHub Discussion](https://github.com/supabase/gotrue/pull/54#issuecomment-757043573)
  * [Potential Risk of Privilege Escalation in Azure AD Applications](https://msrc.microsoft.com/blog/2023/06/potential-risk-of-privilege-escalation-in-azure-ad-applications/)

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/content/guides/auth/social-
login/auth-azure.mdx)

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

