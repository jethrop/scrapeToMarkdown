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
  4.   5. [Server-Side Rendering](/docs/guides/auth/server-side)
  6.   7. [Advanced guide](/docs/guides/auth/server-side/advanced-guide)
  8. 

# Advanced guide

## Details about SSR Auth flows and implementation for advanced users.

* * *

When a user authenticates with Supabase Auth, two pieces of information are
issued by the server:

  1. **Access token** in the form of a JWT.
  2. **Refresh token** which is a randomly generated string.

The default behavior if you're not using SSR is to store this information in
local storage. Local storage isn't accessible by the server, so for SSR, the
tokens instead need to be stored in a secure cookie. The cookie can then be
passed back and forth between your app code in the client and your app code in
the server.

If you're not using SSR, you might also be using the [implicit
flow](/docs/guides/auth/sessions/implicit-flow) to get the access and refresh
tokens. The server can't access the tokens in this flow, so for SSR, you
should change to the [PKCE flow](/docs/guides/auth/sessions/pkce-flow). You
can change the flow type when initiating your Supabase client if your client
library provides this option.

In the `@supabase/ssr` package, Supabase clients are initiated to use the PKCE
flow by default. They are also automatically configured to handle the saving
and retrieval of session information in cookies.

## How it works#

In the PKCE flow, a redirect is made to your app, with an Auth Code contained
in the URL. When you exchange this code using `exchangeCodeForSession`, you
receive the session information, which contains the access and refresh tokens.

To maintain the session, these tokens must be stored in a storage medium
securely shared between client and server, which is traditionally cookies.
Whenever the session is refreshed, the auth and refresh tokens in the shared
storage medium must be updated. Supabase client libraries provide a
customizable `storage` option when a client is initiated, allowing you to
change where tokens are stored.

For an implementation example, see the
[@supabase/ssr](https://github.com/supabase/auth-
helpers/blob/main/packages/ssr/src/index.ts) package.

## Frequently asked questions#

### No session on the server side with Next.js route prefetching?#

When you use route prefetching in Next.js using `<Link href="/...">`
components or the `Router.push()` APIs can send server-side requests before
the browser processes the access and refresh tokens. This means that those
requests may not have any cookies set and your server code will render
unauthenticated content.

To improve experience for your users, we recommend redirecting users to one
specific page after sign-in that does not include any route prefetching from
Next.js. Once the Supabase client library running in the browser has obtained
the access and refresh tokens from the URL fragment, you can send users to any
pages that use prefetching.

### How do I make the cookies `HttpOnly`?#

This is not necessary. Both the access token and refresh token are designed to
be passed around to different components in your application. The browser-
based side of your application needs access to the refresh token to properly
maintain a browser session anyway.

### My server is getting invalid refresh token errors. What's going on?#

It is likely that the refresh token sent from the browser to your server is
stale. Make sure the `onAuthStateChange` listener callback is free of bugs and
is registered relatively early in your application's lifetime

When you receive this error on the server-side, try to defer rendering to the
browser where the client library can access an up-to-date refresh token and
present the user with a better experience.

### Should I set a shorter `Max-Age` parameter on the cookies?#

The `Max-Age` or `Expires` cookie parameters only control whether the browser
sends the value to the server. Since a refresh token represents the long-lived
authentication session of the user on that browser, setting a short `Max-Age`
or `Expires` parameter on the cookies only results in a degraded user
experience.

The only way to ensure that a user has logged out or their session has ended
is to get the user's details with `getUser()`.

### What should I use for the `SameSite` property?#

Make sure you [understand the behavior of the property in different
situations](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-
Cookie/SameSite) as some properties can degrade the user experience.

A good default is to use `Lax` which sends cookies when users are navigating
to your site. Cookies typically require the `Secure` attribute, which only
sends them over HTTPS. However, this can be a problem when developing on
`localhost`.

### Can I use server-side rendering with a CDN or cache?#

Yes, but you need to be careful to include at least the refresh token cookie
value in the cache key. Otherwise you may be accidentally serving pages with
data belonging to different users!

Also be sure you set proper cache control headers. We recommend invalidating
cache keys every hour or less.

### Which authentication flows have PKCE support?#

At present, PKCE is supported on the Magic Link, OAuth, Sign Up, and Password
Recovery routes. These correspond to the `signInWithOtp`, `signInWithOAuth`,
`signUp`, and `resetPasswordForEmail` methods on the Supabase client library.
When using PKCE with Phone and Email OTPs, there is no behavior change with
respect to the implicit flow - an access token will be returned in the body
when a request is successful.

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/content/guides/auth/server-
side/advanced-guide.mdx)

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

