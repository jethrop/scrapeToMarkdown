[Back](/blog)

[Blog](/blog)

# Supabase Bootstrap: the fastest way to launch a new project

15 Apr 2024

•

4 minute read

[![Qiao Han
avatar](/_next/image?url=https%3A%2F%2Fgithub.com%2Fsweatybridge.png&w=96&q=75)Qiao
HanEngineering](https://github.com/sweatybridge)

[![Thor Schaeff
avatar](/_next/image?url=https%3A%2F%2Fgithub.com%2Fthorwebdev.png&w=96&q=75)Thor
SchaeffDevRel & DX](https://twitter.com/thorwebdev)

![Supabase Bootstrap: the fastest way to launch a new
project](/_next/image?url=%2Fimages%2Fblog%2Fga-
week%2Fbootstrap%2Fthumb.png&w=3840&q=100)

Supabase `bootstrap` is the fastest to spin up a new hosted Supabase project
from existing starter templates:

`  

_10

npx supabase bootstrap

  
`

This brings a “shadcn”-like experience to Supabase, creating a project locally
and launching a remote database ready for deployment.

## Getting started#

From any local directory, run `supabase bootstrap` and you will be prompted to
choose a starter template. And the best thing is, you don't even need to
install the CLI to get started! As long as you have `npm` or `bun` installed,
you're ready to go!

  * CLI: `supabase bootstrap`
  * NPM: `npx supabase@latest bootstrap`
  * Bun: `bunx` `supabase@latest bootstrap`

## How templates work#

The list of starter templates is published on GitHub as
[samples.json](https://github.com/supabase-community/supabase-
samples/blob/main/samples.json). Whenever we (and in the future the community)
add a new starter, it will automatically become available to all Supabase
users.

The template repository typically includes the full frontend code, following
the file structure below:

  * A `supabase` directory with `config.toml` and `migrations` files (if any).
  * A `.env.example` file that defines a list of environment variables for CLI to populate project credentials. We currently support the same list of credentials as our [Vercel integration](https://vercel.com/integrations/supabase). If a `.env` file doesn't exist, the CLI will create it for you.

### Local development#

After selecting a starter, the Supabase CLI downloads all files from the
template repository to your chosen local directory.

##### GitHub rate limits

You may run into GitHub rate limit when downloading too frequently from
template repository. This can be avoided by setting `GITHUB_TOKEN` environment
variable locally to your GitHub personal access token.

This model is very similar to the popular [shadcn](https://ui.shadcn.com/)
workflow. After files are creating in your local repo, you can modify them and
check them into source control.

### Deploying to production#

During the `supabase bootstrap` process, a new project will be created on the
Supabase platform and linked to your local environment. This command will run
you through the account creation flow if you don't already have one.

##### Some patience required

Linking to your new hosted project may take a short while as it needs to spin
up a new database in the cloud.

Once the linking is completed, you will be prompted to push any template
migration files to your new hosted project. These migration files will setup
your remote database with the necessary schemas to support the starter
application.

After pushing the migrations, your project credentials will be exported to a
`.env` file for you to connect from any frontend or backend code. The default
environment variables include:

  * `POSTGRES_URL`
  * `SUPABASE_URL`
  * `SUPABASE_ANON_KEY`
  * `SUPABASE_SERVICE_ROLE_KEY`

Other custom variables from `.env.example` file defined by your chosen
template will also be merged to your local `.env` file.

##### Store credentials securely

It is important to store these credentials securely as anyone can connect to
your remote database using the `POSTGRES_URL`.

## Start developing#

Finally, the CLI will suggest a `start` command to launch your application
locally. Starting the local app will use credentials defined in `.env` file to
connect to your new hosted project.

## Template library#

And that's it, with a single command, you can get a new project up and running
end to end.

Supabase Bootstrap makes it even easier to get started with Supabase, mobile
app tools, and web development frameworks like Next.js, Expo React Native,
Flutter, Swift iOS.

We have many many more templates coming soon, and we'll be opening it up to
community contributions. Stay tuned!

## Get started#

Visit the [Supabase CLI docs](/docs/guides/cli/getting-started) to get started
with `supabase bootstrap`.

[![GA logo](/_next/image?url=%2Fimages%2Flaunchweek%2Fga%2Fga-
black.svg&w=64&q=75)![GA
logo](/_next/image?url=%2Fimages%2Flaunchweek%2Fga%2Fga-
white.svg&w=64&q=75)Week](/ga-week)

15-19 April

[Day 1 -Supabase is officially launching into General Availability](/ga)[Day 2
-Supabase Functions now supports AI models](/blog/ai-inference-now-available-
in-supabase-edge-functions)[Day 3 -Supabase Auth now supports Anonymous sign-
ins](/blog/anonymous-sign-ins)[Day 4 -Supabase Storage: now supports the S3
protocol](/blog/s3-compatible-storage)[Day 5 -Supabase Security Advisor &
Performance Advisor](/blog/security-performance-advisor)

Build Stage

[01 -PostgreSQL Index Advisor](https://github.com/supabase/index_advisor)[02
-Branching now Publicly Available](/blog/branching-publicly-available)[03
-Oriole joins Supabase](/blog/supabase-acquires-oriole)[04 -Supabase on AWS
Marketplace](/blog/supabase-aws-marketplace)[05 -Supabase
Bootstrap](/blog/supabase-bootstrap)[06 -Supabase Swift](/blog/supabase-
swift)[07 -Top 10 Launches from Supabase GA Week](/blog/ga-week-summary)[Open
Source Hackathon 2024](/blog/supabase-oss-hackathon)[Community Meetups](/ga-
week#meetups)

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fsupabase-
bootstrap&text=Supabase%20Bootstrap%3A%20the%20fastest%20way%20to%20launch%20a%20new%20project)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fsupabase-
bootstrap&text=Supabase%20Bootstrap%3A%20the%20fastest%20way%20to%20launch%20a%20new%20project)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fsupabase-
bootstrap&t=Supabase%20Bootstrap%3A%20the%20fastest%20way%20to%20launch%20a%20new%20project)

[Last postSupabase on the AWS Marketplace15 April 2024](/blog/supabase-aws-
marketplace)

[Next postSupabase Swift15 April 2024](/blog/supabase-swift)

[launch-week](/blog/tags/launch-week)[CLI](/blog/tags/CLI)

On this page

  * Getting started
  * How templates work
    * Local development
    * Deploying to production
  * Start developing
  * Template library
  * Get started

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fsupabase-
bootstrap&text=Supabase%20Bootstrap%3A%20the%20fastest%20way%20to%20launch%20a%20new%20project)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fsupabase-
bootstrap&text=Supabase%20Bootstrap%3A%20the%20fastest%20way%20to%20launch%20a%20new%20project)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fsupabase-
bootstrap&t=Supabase%20Bootstrap%3A%20the%20fastest%20way%20to%20launch%20a%20new%20project)

## Build in a weekend, scale to millions

[Start your project](https://supabase.com/dashboard)[Request a
demo](/contact/sales)

