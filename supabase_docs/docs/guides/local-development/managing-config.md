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

Local Development

  1. [Local Dev / CLI](/docs/guides/local-development)
  2.   3. Local development
  4.   5. [Managing config and secrets](/docs/guides/local-development/managing-config)
  6. 

# Managing config and secrets

* * *

The Supabase CLI uses a `config.toml` file to manage local configuration. This
file is located in the `supabase` directory of your project.

## Config reference#

The `config.toml` file is automatically created when you run `supabase init`.

There are a wide variety of options available, which can be found in the [CLI
Config Reference](/docs/guides/cli/config).

For example, to enable the "Apple" OAuth provider for local development, you
can append the following information to `config.toml`:

`  

_10

[auth.external.apple]

_10

enabled = false

_10

client_id = ""

_10

secret = ""

_10

redirect_uri = "" # Overrides the default auth redirectUrl.

  
`

## Using secrets inside config.toml#

You can reference environment variables within the `config.toml` file using
the `env()` function. This will detect any values stored in an `.env` file at
the root of your project directory. This is particularly useful for storing
sensitive information like API keys, and any other values that you don't want
to check into version control.

`  

_10

.

_10

├── .env

_10

├── .env.example

_10

└── supabase

_10

└── config.toml

  
`

Do NOT commit your `.env` into git. Be sure to configure your `.gitignore` to
exclude this file.

For example, if your `.env` contained the following values:

`  

_10

GITHUB_CLIENT_ID=""

_10

GITHUB_SECRET=""

  
`

Then you would reference them inside of our `config.toml` like this:

`  

_10

[auth.external.github]

_10

enabled = true

_10

client_id = "env(GITHUB_CLIENT_ID)"

_10

secret = "env(GITHUB_SECRET)"

_10

redirect_uri = "" # Overrides the default auth redirectUrl.

  
`

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/content/guides/local-
development/managing-config.mdx)

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

