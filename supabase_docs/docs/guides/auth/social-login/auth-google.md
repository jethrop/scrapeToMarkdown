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
  6.   7. [Google](/docs/guides/auth/social-login/auth-google)
  8. 

# Login with Google

* * *

Supabase Auth supports Sign in with Google for the web, native Android
applications, and Chrome extensions.

## Prerequisites#

  * A Google Cloud project. Go to the [Google Cloud Platform](https://console.cloud.google.com/home/dashboard) and create a new project if necessary.

## Configuration#

To support Sign In with Google, you need to configure the Google provider for
your Supabase project.

WebExpo React NativeFlutterSwiftAndroid (Kotlin)Chrome Extensions

For web applications, you can set up your signin button two different ways:

  * Use your own application code for the button.
  * Use Google's pre-built sign-in or OneTap flows.

### Application code configuration#

To use your own application code:

  1. In the Google Cloud console, go to the [Consent Screen configuration page](https://console.cloud.google.com/apis/credentials/consent). The consent screen is the view shown to your users when they consent to signing in to your app.

  2. Under **Authorized domains** , add your Supabase project's domain, which has the form `<PROJECT_ID>.supabase.co`.

  3. Configure the following non-sensitive scopes:

     * `.../auth/userinfo.email`
     * `...auth/userinfo.profile`
     * `openid`
  4. Go to the [API Credentials page](https://console.cloud.google.com/apis/credentials).

  5. Click `Create credentials` and choose `OAuth Client ID`.

  6. For application type, choose `Web application`.

  7. Under **Authorized JavaScript origins** , add your site URL.

  8. Under **Authorized redirect URLs** , enter the callback URL from the [Supabase dashboard](/dashboard/project/_/auth/providers). Expand the Google Auth Provider section to display it.

The redirect URL is visible to your users. You can customize it by configuring
[custom domains](/docs/guides/platform/custom-domains).

  9. When you finish configuring your credentials, you will be shown your client ID and secret. Add these to the [Google Auth Provider section of the Supabase Dashboard](/dashboard/project/_/auth/providers).

In local development, you can add the client ID and secret to your
`config.toml` file.

### Google pre-built configuration#

To use Google's pre-built signin buttons:

  1. In the Google Cloud console, go to the [Consent Screen configuration page](https://console.cloud.google.com/apis/credentials/consent). The consent screen is the view shown to your users when they consent to signing in to your app.
  2. Configure the screen to your liking, making sure you add links to your app's privacy policy and terms of service.
  3. Go to the [API Credentials page](https://console.cloud.google.com/apis/credentials).
  4. Click `Create credentials` and choose `OAuth Client ID`.
  5. For application type, choose `Web application`.
  6. Under **Authorized JavaScript origins** and **Authorized redirect URLs** , add your site URL. This is the URL of the website where the signin button will appear, _not_ your Supabase project domain. If you're testing in localhost, ensure that you have `http://localhost` set in the **Authorized JavaScript origins** section as well. This is important when integrating with Google One-Tap to ensure you can use it locally.
  7. When you finish configuring your credentials, you will be shown your client ID. Add this to the **Authorized Client IDs** field in the [Google Auth Provider section of the Supabase Dashboard](/dashboard/project/_/auth/providers). Leave the OAuth client ID and secret blank. You don't need them when using Google's pre-built approach.

## Signing users in#

WebExpo React NativeFlutterAndroid (Kotlin)Chrome Extensions

### Application code#

To use your own application code for the signin button, call the
`signInWithOAuth` method (or the equivalent for your language).

Make sure you're using the right `supabase` client in the following code.

If you're not using Server-Side Rendering or cookie-based Auth, you can
directly use the `createClient` from `@supabase/supabase-js`. If you're using
Server-Side Rendering, see the [Server-Side Auth
guide](/docs/guides/auth/server-side/creating-a-client) for instructions on
creating your Supabase client.

`  

_10

supabase.auth.signInWithOAuth({

_10

provider: 'google',

_10

})

  
`

For an implicit flow, that's all you need to do. The user will be taken to
Google's consent screen, and finally redirected to your app with an access and
refresh token pair representing their session.

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

After a successful code exchange, the user's session will be saved to cookies.

### Saving Google tokens#

The tokens saved by your application are the Supabase Auth tokens. Your app
might additionally need the Google OAuth 2.0 tokens to access Google services
on the user's behalf.

On initial login, you can extract the `provider_token` from the session and
store it in a secure storage medium. The session is available in the returned
data from `signInWithOAuth` (implicit flow) and `exchangeCodeForSession` (PKCE
flow).

Google does not send out a refresh token by default, so you will need to pass
parameters like these to `signInWithOAuth()` in order to extract the
`provider_refresh_token`:

`  

_10

const { data, error } = await supabase.auth.signInWithOAuth({

_10

provider: 'google',

_10

options: {

_10

queryParams: {

_10

access_type: 'offline',

_10

prompt: 'consent',

_10

},

_10

},

_10

})

  
`

### Google pre-built#

Most web apps and websites can utilize Google's [personalized sign-in
buttons](https://developers.google.com/identity/gsi/web/guides/personalized-
button), [One
Tap](https://developers.google.com/identity/gsi/web/guides/features) or
[automatic sign-
in](https://developers.google.com/identity/gsi/web/guides/automatic-sign-in-
sign-out) for the best user experience.

  1. Load the Google client library in your app by including the third-party script:

`  

_10

<script src="https://accounts.google.com/gsi/client" async></script>

  
`

  2. Use the [HTML Code Generator](https://developers.google.com/identity/gsi/web/tools/configurator) to customize the look, feel, features and behavior of the Sign in with Google button.

  3. Pick the _Swap to JavaScript callback_ option, and input the name of your callback function. This function will receive a [`CredentialResponse`](https://developers.google.com/identity/gsi/web/reference/js-reference#CredentialResponse) when sign in completes.

To make your app compatible with Chome's third-party-cookie phase-out, make
sure to set `data-use_fedcm_for_prompt` to `true`.

Your final HTML code might look something like this:

`  

_21

<div

_21

id="g_id_onload"

_21

data-client_id="<client ID>"

_21

data-context="signin"

_21

data-ux_mode="popup"

_21

data-callback="handleSignInWithGoogle"

_21

data-nonce=""

_21

data-auto_select="true"

_21

data-itp_support="true"

_21

data-use_fedcm_for_prompt="true"

_21

></div>

_21

_21

<div

_21

class="g_id_signin"

_21

data-type="standard"

_21

data-shape="pill"

_21

data-theme="outline"

_21

data-text="signin_with"

_21

data-size="large"

_21

data-logo_alignment="left"

_21

></div>

  
`

  4. Create a `handleSignInWithGoogle` function that takes the `CredentialResponse` and passes the included token to Supabase. The function needs to be available in the global scope for Google's code to find it.

`  

_10

async function handleSignInWithGoogle(response) {

_10

const { data, error } = await supabase.auth.signInWithIdToken({

_10

provider: 'google',

_10

token: response.credential,

_10

})

_10

}

  
`

  5. _(Optional)_ Configure a nonce. The use of a nonce is recommended for extra security, but optional. The nonce should be generated randomly each time, and it must be provided in both the `data-nonce` attribute of the HTML code and the options of the callback function.

`  

_10

async function handleSignInWithGoogle(response) {

_10

const { data, error } = await supabase.auth.signInWithIdToken({

_10

provider: 'google',

_10

token: response.credential,

_10

nonce: '<NONCE>',

_10

})

_10

}

  
`

Note that the nonce should be the same in both places, but because Supabase
Auth expects the provider to hash it (SHA-256, hexadecimal representation),
you need to provide a hashed version to Google and a non-hashed version to
`signInWithIdToken`.

You can get both versions by using the in-built `crypto` library:

`  

_12

// Adapted from https://developer.mozilla.org/en-
US/docs/Web/API/SubtleCrypto/digest#converting_a_digest_to_a_hex_string

_12

_12

const nonce = btoa(String.fromCharCode(...crypto.getRandomValues(new
Uint8Array(32))))

_12

const encoder = new TextEncoder()

_12

const encodedNonce = encoder.encode(nonce)

_12

crypto.subtle.digest('SHA-256', encodedNonce).then((hashBuffer) => {

_12

const hashArray = Array.from(new Uint8Array(hashBuffer))

_12

const hashedNonce = hashArray.map((b) => b.toString(16).padStart(2,
'0')).join('')

_12

})

_12

_12

// Use 'hashedNonce' when making the authentication request to Google

_12

// Use 'nonce' when invoking the supabase.auth.signInWithIdToken() method

  
`

### One-tap with NextJS#

If you're integrating Google One-Tap with your NextJS application, you can
refer to the example below to get started:

`  

_83

'use client'

_83

_83

import Script from 'next/script'

_83

import { createClient } from '@/utils/supabase/client'

_83

import { CredentialResponse } from 'google-one-tap'

_83

import { useRouter } from 'next/navigation'

_83

import { useEffect } from 'react'

_83

_83

const OneTapComponent = () => {

_83

const supabase = createClient()

_83

const router = useRouter()

_83

_83

// generate nonce to use for google id token sign-in

_83

const generateNonce = async (): Promise<string[]> => {

_83

const nonce = btoa(String.fromCharCode(...crypto.getRandomValues(new
Uint8Array(32))))

_83

const encoder = new TextEncoder()

_83

const encodedNonce = encoder.encode(nonce)

_83

const hashBuffer = await crypto.subtle.digest('SHA-256', encodedNonce)

_83

const hashArray = Array.from(new Uint8Array(hashBuffer))

_83

const hashedNonce = hashArray.map((b) => b.toString(16).padStart(2,
'0')).join('')

_83

_83

return [nonce, hashedNonce]

_83

}

_83

_83

useEffect(() => {

_83

const initializeGoogleOneTap = () => {

_83

console.log('Initializing Google One Tap')

_83

window.addEventListener('load', async () => {

_83

const [nonce, hashedNonce] = await generateNonce()

_83

console.log('Nonce: ', nonce, hashedNonce)

_83

_83

// check if there's already an existing session before initializing the one-
tap UI

_83

const { data, error } = await supabase.auth.getSession()

_83

if (error) {

_83

console.error('Error getting session', error)

_83

}

_83

if (data.session) {

_83

router.push('/')

_83

return

_83

}

_83

_83

/* global google */

_83

google.accounts.id.initialize({

_83

client_id: process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID,

_83

callback: async (response: CredentialResponse) => {

_83

try {

_83

// send id token returned in response.credential to supabase

_83

const { data, error } = await supabase.auth.signInWithIdToken({

_83

provider: 'google',

_83

token: response.credential,

_83

nonce,

_83

})

_83

_83

if (error) throw error

_83

console.log('Session data: ', data)

_83

console.log('Successfully logged in with Google One Tap')

_83

_83

// redirect to protected page

_83

router.push('/')

_83

} catch (error) {

_83

console.error('Error logging in with Google One Tap', error)

_83

}

_83

},

_83

nonce: hashedNonce,

_83

// with chrome's removal of third-party cookiesm, we need to use FedCM instead
(https://developers.google.com/identity/gsi/web/guides/fedcm-migration)

_83

use_fedcm_for_prompt: true,

_83

})

_83

google.accounts.id.prompt() // Display the One Tap UI

_83

})

_83

}

_83

initializeGoogleOneTap()

_83

return () => window.removeEventListener('load', initializeGoogleOneTap)

_83

}, [])

_83

_83

return (

_83

<>

_83

<Script src="https://accounts.google.com/gsi/client" />

_83

<div id="oneTap" className="fixed top-0 right-0 z-[100]" />

_83

</>

_83

)

_83

}

_83

_83

export default OneTapComponent

  
`

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/content/guides/auth/social-
login/auth-google.mdx)

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

