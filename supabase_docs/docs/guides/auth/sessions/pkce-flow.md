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
  4.   5. [Sessions](/docs/guides/auth/sessions)
  6.   7. [PKCE flow](/docs/guides/auth/sessions/pkce-flow)
  8. 

# PKCE flow

## About authenticating with PKCE flow.

* * *

The Proof Key for Code Exchange (PKCE) flow is one of two ways that a user can
authenticate and your app can receive the necessary access and refresh tokens.

The flow is an implementation detail handled for you by Supabase Auth, but
understanding the difference between PKCE and [implicit
flow](/docs/guides/auth/sessions/implicit-flow) is important for understanding
the difference between client-only and server-side auth.

## How it works#

After a successful verification, the user is redirected to your app with a URL
that looks like this:

`  

_10

https://yourapp.com/...?code=<...>

  
`

The `code` parameter is commonly known as the Auth Code and can be exchanged
for an access token by calling `exchangeCodeForSession(code)`.

For security purposes, the code has a validity of 5 minutes and can only be
exchanged for an access token once. You will need to restart the
authentication flow from scratch if you wish to obtain a new access token.

As the flow is run server side, `localStorage` may not be available. You may
configure the client library to use a custom storage adapter and an alternate
backing storage such as cookies by setting the `storage` option to an object
with the following methods:

`  

_23

const customStorageAdapter: SupportedStorage = {

_23

getItem: (key) => {

_23

if (!supportsLocalStorage()) {

_23

// Configure alternate storage

_23

return null

_23

}

_23

return globalThis.localStorage.getItem(key)

_23

},

_23

setItem: (key, value) => {

_23

if (!supportsLocalStorage()) {

_23

// Configure alternate storage here

_23

return

_23

}

_23

globalThis.localStorage.setItem(key, value)

_23

},

_23

removeItem: (key) => {

_23

if (!supportsLocalStorage()) {

_23

// Configure alternate storage here

_23

return

_23

}

_23

globalThis.localStorage.removeItem(key)

_23

},

_23

}

  
`

You may also configure the client library to automatically exchange it for a
session after a successful redirect. This can be done by setting the
`detectSessionInUrl` option to `true`.

Putting it all together, your client library initialization may look like
this:

`  

_14

const supabase = createClient(

_14

'https://xyzcompany.supabase.co',

_14

'public-anon-key',

_14

{

_14

...

_14

auth: {

_14

...

_14

detectSessionInUrl: true,

_14

flowType: 'pkce',

_14

storage: customStorageAdapter,

_14

}

_14

...

_14

}

_14

)

  
`

## Limitations#

Behind the scenes, the code exchange requires a code verifier. Both the code
in the URL and the code verifier are sent back to the Auth server for a
successful exchange.

The code verifier is created and stored locally when the Auth flow is first
initiated. That means the code exchange must be initiated on the same browser
and device where the flow was started.

## Resources#

  * [OAuth 2.0 guide](https://oauth.net/2/pkce/) to PKCE flow

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/content/guides/auth/sessions/pkce-
flow.mdx)

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

