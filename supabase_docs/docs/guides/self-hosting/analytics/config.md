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
  2.   3. Analytics Server
  4.   5. [Configuration](/docs/guides/self-hosting/analytics/config)
  6. 

# Analytics Self-hosting Config

* * *

You can use environment variables to configure your Analytics Server.

## General Settings

General server settings.

##### Parameters

LOGFLARE_SINGLE_TENANT

REQUIRED

boolean

This is will seed a singular user into the database, and will disable browser
authentication. All browser usage will default to this user. Inviting team
users and other team-related functionality is currently not supported for
self-hosted. Logflare self-hosted is currently intended for single-user
experience only.

LOGFLARE_API_KEY

REQUIRED

string

Allows you to pass in an API key that will used for authentication. This is
intended for programmatic usage where an external program sets the API key. It
is advised to use the UI to configure the access tokens instead. If this value
is not provided, the default API key will be automatically generated.

LOGFLARE_SUPABASE_MODE

REQUIRED

boolean

This is a special mode for Logflare which will seed additional resources for
usage with Supabase self-hosted.

PHX_HTTP_PORT

REQUIRED

string

Port which serves HTTP requests

DB_SCHEMA

REQUIRED

string

This ENV variable sets the search path to a custom database schema. This
allows you to customize the schema used on the database.

LOGFLARE_LOG_LEVEL

REQUIRED

string

Allows the setting of the log level at runtime. For production settings, we
advise `warn`.

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/pages/guides/self-
hosting/analytics/config.tsx)

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

