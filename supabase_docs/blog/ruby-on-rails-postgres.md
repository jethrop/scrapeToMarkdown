[Back](/blog)

[Blog](/blog)

# Getting started with Ruby on Rails and Postgres on Supabase

29 Jan 2024

•

5 minute read

[![Thor Schaeff
avatar](/_next/image?url=https%3A%2F%2Fgithub.com%2Fthorwebdev.png&w=96&q=75)Thor
SchaeffDevRel & DX](https://twitter.com/thorwebdev)

![Getting started with Ruby on Rails and Postgres on
Supabase](/_next/image?url=%2Fimages%2Fblog%2Fgetting-
started%2Frails%2Frails.jpg&w=3840&q=100)

Every Supabase project comes with a full
[Postgres](https://www.postgresql.org/) database, a free and open source
database which is considered one of the world's most stable and advanced
databases.

Postgres is an ideal choice for your Ruby on Rails applications as Rails ships
with a built-in Postgres adapter!

In this post we'll start from scratch, creating a new Rails project,
connecting it to our Supabase Postgres database, and interacting with the
database using the Rails Console.

##### Need help migrating?

Supabase is one of the best [free alternatives to Heroku
Postgres](/alternatives/supabase-vs-heroku-postgres). See [this
guide](/docs/guides/resources/migrating-to-supabase/heroku) to learn how to
migrate from Heroku to Supabase.

There's also a [Heroku to Supabase migration
tool](https://migrate.supabase.com/) available to migrate in just a few
clicks.

If you prefer video guide, you can follow along below. And make sure to
subscribe to the [Supabase YouTube
channel](https://www.youtube.com/channel/UCNTVzV1InxHV-
YR0fSajqPQ?view_as=subscriber&sub_confirmation=1)!

## Create a Rails Project#

Make sure your Ruby and Rails versions are up to date, then use `rails new` to
scaffold a new Rails project. Use the `-d=postgresql` flag to set it up for
Postgres.

Go to the [Rails docs](https://guides.rubyonrails.org/getting_started.html)
for more details.

Terminal

`  

_10

rails new blog -d=postgresql

  
`

## Set up the Postgres connection details#

Go to [database.new](https://database.new) and create a new Supabase project.
Save your database password securely.

When your project is up and running, navigate to the [database
settings](https://supabase.com/dashboard/project/_/settings/database) to find
the URI connection string.

Rails ships with a Postgres adapter included, you can simply configure it via
the environment variables. You can find the database URL in your [Supabase
Dashboard](/dashboard/project/_/settings/database).

Terminal

`  

_10

export DATABASE_URL=postgres://postgres.xxxx:[[email protected]](/cdn-
cgi/l/email-protection):5432/postgres

  
`

## Create and run a database migration#

Rails includes Active Record as the ORM as well as database migration tooling
which generates the SQL migration files for you.

Create an example `Article` model and generate the migration files.

Terminal

`  

_10

bin/rails generate scaffold Article title:string body:text

_10

bin/rails db:migrate

  
`

## Use the Model to interact with the database#

You can use the included Rails console to interact with the database. For
example, you can create new entries or list all entries in a Model's table.

Terminal

`  

_10

bin/rails console

  
`

irb

`  

_10

article = Article.new(title: "Hello Rails", body: "I am on Rails!")

_10

article.save # Saves the entry to the database

_10

_10

Article.all

  
`

## Start the app#

Terminal

`  

_10

bin/rails server

  
`

Run the development server. Go to <http://127.0.0.1:3000> in a browser to see
your application running.

## Update the app to show articles#

Currently the app shows a nice development splash screen, let's update this to
show our articles from the database:

config/routes.rb

`  

_10

Rails.application.routes.draw do

_10

# Define your application routes per the DSL in
https://guides.rubyonrails.org/routing.html

_10

_10

# Defines the root path route ("/")

_10

root "articles#index"

_10

end

  
`

## Deploy to Fly.io#

In order to start working with Fly.io, you will need `flyctl`, our CLI app for
managing apps. If you've already installed it, carry on. If not, hop over to
the [installation guide](https://fly.io/docs/hands-on/install-flyctl/). Once
that's installed you'll want to [log in to Fly](https://fly.io/docs/getting-
started/log-in-to-fly/).

### Provision Rails with Fly.io#

To configure and launch the app, you can use `fly launch` and follow the
wizard.

When asked "Do you want to tweak these settings before proceeding?" select `y`
and set Postgres to `none` as we will be providing the Supabase database URL
as a secret.

### Set the connection string as secret#

Use the Fly.io CLI to set the Supabase database connection URI from above as a
sevret which is exposed as an environment variable to the Rails app.

Terminal

`  

_10

fly secrets set DATABASE_URL=$DATABASE_URL

  
`

### Deploy the app#

Deploying your application is done with the following command:

Terminal

`  

_10

fly deploy

  
`

This will take a few seconds as it uploads your application, builds a machine
image, deploys the images, and then monitors to ensure it starts successfully.
Once complete visit your app with the following command:

Terminal

`  

_10

fly apps open

  
`

That's it! You're Rails app is up and running with Supabase Postgres and
Fly.io!

## Conclusion#

Supabase is the ideal platform for powering your Postgres database for your
Ruby on Rails applications! Every Supabase project comes with a full Postgres
database and a good number of [useful
extensions](/docs/guides/database/extensions)!

Try it out now at [database.new](https://database.new)!

## More Supabase#

  * [Migration guides](/docs/guides/resources#migrate-to-supabase)
  * [Options for connecting to your Postgres database](/docs/guides/database/connecting-to-postgres)

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fruby-
on-rails-
postgres&text=Getting%20started%20with%20Ruby%20on%20Rails%20and%20Postgres%20on%20Supabase)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fruby-
on-rails-
postgres&text=Getting%20started%20with%20Ruby%20on%20Rails%20and%20Postgres%20on%20Supabase)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fruby-
on-rails-
postgres&t=Getting%20started%20with%20Ruby%20on%20Rails%20and%20Postgres%20on%20Supabase)

[Last postpgvector 0.6.0: 30x faster with parallel index builds30 January
2024](/blog/pgvector-fast-builds)

[Next postCreate a Figma Clone app with Flutter and Supabase Realtime26
January 2024](/blog/flutter-figma-clone)

[postgres](/blog/tags/postgres)[developers](/blog/tags/developers)[ruby](/blog/tags/ruby)

On this page

  * Create a Rails Project
  * Set up the Postgres connection details
  * Create and run a database migration
  * Use the Model to interact with the database
  * Start the app
  * Update the app to show articles
  * Deploy to Fly.io
    * Provision Rails with Fly.io
    * Set the connection string as secret
    * Deploy the app
  * Conclusion
  * More Supabase

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fruby-
on-rails-
postgres&text=Getting%20started%20with%20Ruby%20on%20Rails%20and%20Postgres%20on%20Supabase)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fruby-
on-rails-
postgres&text=Getting%20started%20with%20Ruby%20on%20Rails%20and%20Postgres%20on%20Supabase)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fruby-
on-rails-
postgres&t=Getting%20started%20with%20Ruby%20on%20Rails%20and%20Postgres%20on%20Supabase)

## Build in a weekend, scale to millions

[Start your project](https://supabase.com/dashboard)[Request a
demo](/contact/sales)

