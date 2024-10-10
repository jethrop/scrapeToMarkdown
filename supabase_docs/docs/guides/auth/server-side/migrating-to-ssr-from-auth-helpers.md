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
  6.   7. [Migrating from Auth Helpers](/docs/guides/auth/server-side/migrating-to-ssr-from-auth-helpers)
  8. 

# Migrating to the SSR package from Auth Helpers

* * *

The new `ssr` package takes the core concepts of the Auth Helpers and makes
them available to any server language or framework. This page will guide you
through migrating from the Auth Helpers package to `ssr`.

### Replacing Supabase packages#

Next.jsSvelteKitRemix

`  

_10

npm uninstall @supabase/auth-helpers-nextjs

  
`

`  

_10

npm install @supabase/ssr

  
`

### Creating a client#

The new `ssr` package exports two functions for creating a Supabase client.
The `createBrowserClient` function is used in the client, and the
`createServerClient` function is used in the server.

Check out the [Creating a client](/docs/guides/auth/server-side/creating-a-
client) page for examples of creating a client in your framework.

## Next steps#

  * Implement [Authentication using Email and Password](/docs/guides/auth/server-side/email-based-auth-with-pkce-flow-for-ssr)
  * Implement [Authentication using OAuth](/docs/guides/auth/server-side/oauth-with-pkce-flow-for-ssr)
  * [Learn more about SSR](/docs/guides/auth/server-side-rendering)

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/content/guides/auth/server-
side/migrating-to-ssr-from-auth-helpers.mdx)

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

