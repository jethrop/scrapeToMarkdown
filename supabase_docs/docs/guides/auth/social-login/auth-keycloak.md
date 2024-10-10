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
  6.   7. [Keycloak](/docs/guides/auth/social-login/auth-keycloak)
  8. 

# Login with Keycloak

* * *

To enable Keycloak Auth for your project, you need to set up an Keycloak OAuth
application and add the application credentials to your Supabase Dashboard.

## Overview#

To get started with Keycloak, you can run it in a docker container with:
`docker run -p 8080:8080 -e KEYCLOAK_ADMIN=admin -e
KEYCLOAK_ADMIN_PASSWORD=admin quay.io/keycloak/keycloak:latest start-dev`

This guide will be assuming that you are running keycloak in a docker
container as described in the command above.

Keycloak OAuth consists of five broad steps:

  * Create a new client in your specified keycloak realm.
  * Obtain the `issuer` from the "OpenID Endpoint Configuration". This will be used as the `Keycloak URL`.
  * Ensure that the new client has the "Client Protocol" set to "openid-connect" and the "Access Type" is set to "confidential".
  * The `Client ID` of the client created will be used as the `client id`.
  * Obtain the `Secret` from the credentials tab which will be used as the `client secret`.
  * Add the callback url of your application to your allowlist.

## Access your Keycloak admin console#

  * Login by visiting [`http://localhost:8080`](http://localhost:8080) and clicking on "Administration Console".

## Create a Keycloak realm#

  * Once you've logged in to the Keycloak console, you can add a realm from the side panel. The default realm should be named "Master".
  * After you've added a new realm, you can retrieve the `issuer` from the "OpenID Endpoint Configuration" endpoint. The `issuer` will be used as the `Keycloak URL`.
  * You can find this endpoint from the realm settings under the "General Tab" or visit [`http://localhost:8080/realms/my_realm_name/.well-known/openid-configuration`](http://localhost:8080/realms/my_realm_name/.well-known/openid-configuration)

![Add a Keycloak Realm.](/docs/img/guides/auth-keycloak/keycloak-create-
realm.png)

## Create a Keycloak client#

The "Client ID" of the created client will serve as the `client_id` when you
make API calls to authenticate the user.

![Add a Keycloak client](/docs/img/guides/auth-keycloak/keycloak-add-
client.png)

## Client settings#

After you've created the client successfully, ensure that you set the
following settings:

  1. The "Client Protocol" should be set to "openid-connect".
  2. The "Access Type" should be set to "confidential".
  3. The "Valid Redirect URIs" should be set to: `https://<project-ref>.supabase.co/auth/v1/callback`.

![Obtain the client id, set the client protocol and access
type](/docs/img/guides/auth-keycloak/keycloak-client-id.png) ![Set redirect
uri](/docs/img/guides/auth-keycloak/keycloak-redirect-uri.png)

## Obtain the client secret#

This will serve as the `client_secret` when you make API calls to authenticate
the user. Under the "Credentials" tab, the `Secret` value will be used as the
`client secret`.

![Obtain the client secret](/docs/img/guides/auth-keycloak/keycloak-client-
secret.png)

## Add login code to your client app#

Since Keycloak version 22, the `openid` scope must be passed. Add this to the
[`supabase.auth.signInWithOAuth()`](/docs/reference/javascript/auth-
signinwithoauth) method.

JavaScriptFlutterKotlin

Make sure you're using the right `supabase` client in the following code.

If you're not using Server-Side Rendering or cookie-based Auth, you can
directly use the `createClient` from `@supabase/supabase-js`. If you're using
Server-Side Rendering, see the [Server-Side Auth
guide](/docs/guides/auth/server-side/creating-a-client) for instructions on
creating your Supabase client.

When your user signs in, call
[signInWithOAuth()](/docs/reference/javascript/auth-signinwithoauth) with
`keycloak` as the `provider`:

`  

_10

async function signInWithKeycloak() {

_10

const { data, error } = await supabase.auth.signInWithOAuth({

_10

provider: 'keycloak',

_10

options: {

_10

scopes: 'openid',

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

## Resources#

  * You can find the keycloak openid endpoint configuration under the realm settings. ![Keycloak OpenID Endpoint Configuration](/docs/img/guides/auth-keycloak/keycloak-openid-endpoint-config.png)

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/content/guides/auth/social-
login/auth-keycloak.mdx)

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

