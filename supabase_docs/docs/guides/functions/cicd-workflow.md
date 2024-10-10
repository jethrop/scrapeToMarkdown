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

Edge Functions

  1. [Edge Functions](/docs/guides/functions)
  2.   3. Guides
  4.   5. [Deploying with CI / CD pipelines](/docs/guides/functions/cicd-workflow)
  6. 

# Deploying with CI / CD pipelines

## Use GitHub Actions, Bitbucket, and GitLab CI to deploy your Edge Functions.

* * *

You can use popular CI / CD tools like GitHub Actions, Bitbucket, and GitLab
CI to automate Edge Function deployments.

## GitHub Actions#

You can use the official [`setup-cli` GitHub
Action](https://github.com/marketplace/actions/supabase-cli-action) to run
Supabase CLI commands in your GitHub Actions.

The following GitHub Action deploys all Edge Functions any time code is merged
into the `main` branch:

`  

_24

name: Deploy Function

_24

_24

on:

_24

push:

_24

branches:

_24

- main

_24

workflow_dispatch:

_24

_24

jobs:

_24

deploy:

_24

runs-on: ubuntu-latest

_24

_24

env:

_24

SUPABASE_ACCESS_TOKEN: ${{ secrets.SUPABASE_ACCESS_TOKEN }}

_24

PROJECT_ID: your-project-id

_24

_24

steps:

_24

- uses: actions/checkout@v3

_24

_24

- uses: supabase/setup-cli@v1

_24

with:

_24

version: latest

_24

_24

- run: supabase functions deploy --project-ref $PROJECT_ID

  
`

## GitLab CI#

Here is the sample pipeline configuration to deploy via GitLab CI.

`  

_29

image: node:20

_29

_29

# List of stages for jobs, and their order of execution

_29

stages:

_29

- setup

_29

- deploy

_29

_29

# This job runs in the setup stage, which runs first.

_29

setup-npm:

_29

stage: setup

_29

script:

_29

- npm i supabase

_29

cache:

_29

paths:

_29

- node_modules/

_29

artifacts:

_29

paths:

_29

- node_modules/

_29

_29

# This job runs in the deploy stage, which only starts when the job in the
build stage completes successfully.

_29

deploy-function:

_29

stage: deploy

_29

script:

_29

- npx supabase init

_29

- npx supabase functions deploy --debug

_29

services:

_29

- docker:dind

_29

variables:

_29

DOCKER_HOST: tcp://docker:2375

  
`

## Bitbucket Pipelines#

Here is the sample pipeline configuration to deploy via Bitbucket.

`  

_18

image: node:20

_18

_18

pipelines:

_18

default:

_18

- step:

_18

name: Setup

_18

caches:

_18

- node

_18

script:

_18

- npm i supabase

_18

- parallel:

_18

- step:

_18

name: Functions Deploy

_18

script:

_18

- npx supabase init

_18

- npx supabase functions deploy --debug

_18

services:

_18

- docker

  
`

## Declarative configuration#

Individual function configuration like [JWT
verification](/docs/guides/cli/config#functions.function_name.verify_jwt) and
[import map
location](/docs/guides/cli/config#functions.function_name.import_map) can be
set via the `config.toml` file.

`  

_10

[functions.hello-world]

_10

verify_jwt = false

  
`

## Resources#

  * See the [example on GitHub](https://github.com/supabase/supabase/blob/master/examples/edge-functions/.github/workflows/deploy.yaml).

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/content/guides/functions/cicd-
workflow.mdx)

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

