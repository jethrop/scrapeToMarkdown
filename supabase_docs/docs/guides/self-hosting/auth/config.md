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

Self-Hosting

  1. [Self-Hosting](/docs/guides/self-hosting)
  2.   3. Auth Server
  4.   5. [Configuration](/docs/guides/self-hosting/auth/config)
  6. 

# Auth Self-hosting Config

* * *

A `config.toml` file is generated after running `supabase init`. This file is
located in the `supabase` folder under `supabase/config.toml`.

## General

General settings.

##### Parameters

project_id

REQUIRED

no type

A string used to distinguish different Supabase projects on the same host.
Defaults to the working directory name when running `supabase init`.

auth.external.github

REQUIRED

no type

Describes whether the Github provider is enabled or not.

auth.site_url

REQUIRED

no type

The base URL of your website. Used as an allow-list for redirects and for
constructing URLs used in emails.

auth.additional_redirect_urls

REQUIRED

no type

A list of _exact_ URLs that auth providers are permitted to redirect to post
authentication.

auth.jwt_expiry

REQUIRED

no type

How long tokens are valid for, in seconds. Defaults to 3600 (1 hour), maximum
604,800 seconds (one week).

auth.enable_signup

REQUIRED

no type

Allow/disallow new user signups to your project.

auth.email.enable_signup

REQUIRED

no type

Allow/disallow new user signups via email to your project.

auth.email.double_confirm_changes

REQUIRED

no type

If enabled, a user will be required to confirm any email change on both the
old, and new email addresses. If disabled, only the new email is required to
confirm.

auth.email.enable_confirmations

REQUIRED

no type

If enabled, users need to confirm their email address before signing in.

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/pages/guides/self-
hosting/auth/config.tsx)

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

