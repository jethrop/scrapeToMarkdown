[Back](/blog)

[Blog](/blog)

# Official Supabase extension for VS Code and GitHub Copilot

12 Aug 2024

•

3 minute read

[![Anas Araid avatar](/_next/image?url=https%3A%2F%2Fgithub.com%2Fanas-
araid.png&w=96&q=75)Anas AraidGuest Author](https://github.com/anas-araid)

[![Thor Schaeff
avatar](/_next/image?url=https%3A%2F%2Fgithub.com%2Fthorwebdev.png&w=96&q=75)Thor
SchaeffDevRel & DX](https://twitter.com/thorwebdev)

![Official Supabase extension for VS Code and GitHub
Copilot](/_next/image?url=%2Fimages%2Fblog%2Flw12%2Fday-1%2Fgithub_copilot_extension-
thumb.png&w=3840&q=100)

Today we're launching a new [GitHub Copilot extension for VS
Code](https://marketplace.visualstudio.com/items?itemName=Supabase.vscode-
supabase-extension) to make your development with Supabase and VS Code even
more delightful, starting with a Copilot-guided experience for [database
migrations](/docs/guides/cli/local-development#database-migrations).

The foundation for this extension was created by [Anas
Araid](https://github.com/anas-araid) during a previous [Launch Week
Hackathon](https://twitter.com/anas_araid/status/1736641409094988033).
Impressed with their work, we partnered with them to add a ["Chat
Participant"](https://code.visualstudio.com/api/extension-guides/chat), an
exciting [new feature recently
launched](https://code.visualstudio.com/blogs/2024/06/24/extensions-are-all-
you-need) by the GitHub and VS Code teams at Microsoft.

## Features#

The VS Code extension is quite feature rich:

### GitHub Copilot Chat Participant#

The extension provides a [Chat
Participant](https://code.visualstudio.com/api/extension-guides/chat) for
GitHub Copilot to help with your Supabase questions. Simply type `@supabase`
in your Copilot Chat and the extension will include your database schema as
context to Copilot.

### Copilot-guided database migrations#

The extension provides a guided experience to create and apply [database
migrations](/docs/guides/cli/local-development#database-migrations). Simply
type `@supabase /migration <describe what you want to do>` in your Copilot
Chat and the extension will generate a new SQL migration for you.

### Inspect tables & views#

Inspect your tables and views, including their columns, types, and data,
directly from the editor:

### List database migrations#

See the migration history of your database:

### Inspect database functions#

Inspect your database functions and their SQL definitions:

### List Storage buckets#

List the Storage buckets in your Supabase project.

## What's Next?#

We're excited to continue adding more features that will make your development
experience with Supabase even more delightful - and for this we need your
help! If you have any feedback, feature requests, or bug reports, please [open
an issue on GitHub](https://github.com/supabase-community/supabase-vscode-
extension/issues).

The extension requires you to have the Supabase CLI installed and have your
project running locally. In a future release, we will integrate the [Supabase
Managamenet API](/docs/reference/api/introduction) into the extension to make
connecting to your hosted Supabase projects as seamless as possible.

## Contributing to Supabase#

The entire Supabase stack is [fully open source](/open-source), including
[this extension](https://github.com/supabase-community/supabase-vscode-
extension). In fact, this extension was originally created by [Anas
Araid](https://github.com/anas-araid) during a [previous Launch Week
Hackathon](https://twitter.com/anas_araid/status/1736641409094988033).

Your contributions, feedback, and engagement in the Supabase community are
invaluable, and play a significant role in shaping our future. Thank you for
your support!

## Resources#

  * [Install the extension](https://marketplace.visualstudio.com/items?itemName=Supabase.vscode-supabase-extension)
  * [Read the source code](https://github.com/supabase-community/supabase-vscode-extension)
  * [Submit a Feature Request](https://github.com/supabase-community/supabase-vscode-extension/issues)
  * [Get started with Supabase](https://database.new)

[Launch Week12](/launch-week)

12-16 August

[Day 1 -postgres.new: In-browser Postgres with an AI
interface](/blog/postgres-new)[Day 2 -Realtime Broadcast and Presence
Authorization](/blog/supabase-realtime-broadcast-and-presence-
authorization)[Day 3 -Supabase Auth: Bring-your-own Auth0, Cognito, or
Firebase](/blog/third-party-auth-mfa-phone-send-hooks)[Day 4 -Introducing Log
Drains](/blog/log-drains)[Day 5 -Postgres Foreign Data Wrappers with
Wasm](/blog/postgres-foreign-data-wrappers-with-wasm)

Build Stage

[01 -GitHub Copilot](/blog/github-copilot-extension-for-vs-code)[02
-pg_replicate](https://news.ycombinator.com/item?id=41209994)[03 -Snaplet is
now open source](/blog/snaplet-is-now-open-source)[04 -Supabase
Book](/blog/supabase-book-by-david-lorenz)[05
-PostgREST](/blog/postgrest-12-2)[06 -vec2pg](/blog/vec2pg)[07
-pg_graphql](/blog/pg-graphql-1-5-7)[08 -Platform Access
Control](/blog/platform-access-control)[09 -python-support](/blog/python-
support)[10 -Launch Week Summary](/blog/launch-week-12-top-10)[Community
Meetups](/launch-week#meetups)

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fgithub-
copilot-extension-for-vs-
code&text=Official%20Supabase%20extension%20for%20VS%20Code%20and%20GitHub%20Copilot)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fgithub-
copilot-extension-for-vs-
code&text=Official%20Supabase%20extension%20for%20VS%20Code%20and%20GitHub%20Copilot)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fgithub-
copilot-extension-for-vs-
code&t=Official%20Supabase%20extension%20for%20VS%20Code%20and%20GitHub%20Copilot)

[Last postSupabase Realtime: Broadcast and Presence Authorization13 August
2024](/blog/supabase-realtime-broadcast-and-presence-authorization)

[Next postpostgres.new: In-browser Postgres with an AI interface12 August
2024](/blog/postgres-new)

[launch-week](/blog/tags/launch-week)

On this page

  * Features
    * GitHub Copilot Chat Participant
    * Copilot-guided database migrations
    * Inspect tables & views
    * List database migrations
    * Inspect database functions
    * List Storage buckets
  * What's Next?
  * Contributing to Supabase
  * Resources

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fgithub-
copilot-extension-for-vs-
code&text=Official%20Supabase%20extension%20for%20VS%20Code%20and%20GitHub%20Copilot)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fgithub-
copilot-extension-for-vs-
code&text=Official%20Supabase%20extension%20for%20VS%20Code%20and%20GitHub%20Copilot)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fgithub-
copilot-extension-for-vs-
code&t=Official%20Supabase%20extension%20for%20VS%20Code%20and%20GitHub%20Copilot)

## Build in a weekend, scale to millions

[Start your project](https://supabase.com/dashboard)[Request a
demo](/contact/sales)

