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
  2.   3. CLI
  4.   5. [Getting started](/docs/guides/local-development/cli/getting-started)
  6. 

# Supabase CLI

## Develop locally, deploy to the Supabase Platform, and set up CI/CD
workflows

* * *

The Supabase CLI enables you to run the entire Supabase stack locally, on your
machine or in a CI environment. With just two commands, you can set up and
start a new local project:

  1. `supabase init` to create a new local project
  2. `supabase start` to launch the Supabase services

## Installing the Supabase CLI#

macOSWindowsLinuxnpm / Bun

Install the CLI with [Homebrew](https://brew.sh):

`  

_10

brew install supabase/tap/supabase

  
`

## Updating the Supabase CLI#

When a new [version](https://github.com/supabase/cli/releases) is released,
you can update the CLI using the same methods.

macOSWindowsLinuxnpm / Bun

`  

_10

brew upgrade supabase

  
`

If you have any Supabase containers running locally, stop them and delete
their data volumes before proceeding with the upgrade. This ensures that
Supabase managed services can apply new migrations on a clean state of the
local database.

##### Backup and stop running containers

Remember to save any local schema and data changes before stopping because the
`--no-backup` flag will delete them.

`  

_10

supabase db diff my_schema

_10

supabase db dump --local --data-only > supabase/seed.sql

_10

supabase stop --no-backup

  
`

## Running Supabase locally#

The Supabase CLI uses Docker containers to manage the local development stack.
Follow the official guide to install and configure [Docker
Desktop](https://docs.docker.com/desktop):

macOSWindows

Alternately, you can use a different container tool that offers Docker
compatible APIs.

  * [Rancher Desktop](https://rancherdesktop.io/) (macOS, Windows, Linux)
  * [Podman](https://podman.io/) (macOS, Windows, Linux)
  * [OrbStack](https://orbstack.dev/) (macOS)
  * [colima](https://github.com/abiosoft/colima) (macOS)

Inside the folder where you want to create your project, run:

`  

_10

supabase init

  
`

This will create a new `supabase` folder. It's safe to commit this folder to
your version control system.

Now, to start the Supabase stack, run:

`  

_10

supabase start

  
`

This takes time on your first run because the CLI needs to download the Docker
images to your local machine. The CLI includes the entire Supabase toolset,
and a few additional images that are useful for local development (like a
local SMTP server and a database diff tool).

## Access your project's services#

Once all of the Supabase services are running, you'll see output containing
your local Supabase credentials. It should look like this, with urls and keys
that you'll use in your local project:

`  

_10

_10

Started supabase local development setup.

_10

_10

API URL: http://localhost:54321

_10

DB URL: postgresql://postgres:postgres@localhost:54322/postgres

_10

Studio URL: http://localhost:54323

_10

Inbucket URL: http://localhost:54324

_10

anon key: eyJh......

_10

service_role key: eyJh......

  
`

StudioPostgresAPI GatewayAnalytics

`  

_10

# Default URL:

_10

http://localhost:54323

  
`

The local development environment includes Supabase Studio, a graphical
interface for working with your database.

![Local Studio](/docs/img/guides/cli/local-studio.png)

## Stopping local services#

When you are finished working on your Supabase project, you can stop the stack
(without resetting your local database):

`  

_10

supabase stop

  
`

## Learn more#

  * [CLI configuration](/docs/guides/local-development/cli/config)
  * [CLI reference](/docs/reference/cli)

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/content/guides/local-
development/cli/getting-started.mdx)

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

