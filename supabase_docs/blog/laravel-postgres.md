[Back](/blog)

[Blog](/blog)

# Getting started with Laravel and Postgres

22 Jan 2024

•

4 minute read

[![Thor Schaeff
avatar](/_next/image?url=https%3A%2F%2Fgithub.com%2Fthorwebdev.png&w=96&q=75)Thor
SchaeffDevRel & DX](https://twitter.com/thorwebdev)

![Getting started with Laravel and
Postgres](/_next/image?url=%2Fimages%2Fblog%2Fgetting-
started%2Flaravel%2Flaravel.jpg&w=3840&q=100)

Every Supabase project comes with a full
[Postgres](https://www.postgresql.org/) database, a free and open source
database which is considered one of the world's most stable and advanced
databases.

Postgres is an ideal choice for your Laravel PHP applications as Laravel ships
with a Postgres adapter built in!

In this post we'll start from scratch, creating a new Laravel application,
setting up the Laravel Breeze starter kit for user authentication, and
connecting it to our Supabase Postgres database.

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

## Create a Laravel Project#

Make sure your PHP and Composer versions are up to date, then use `composer
create-project` to scaffold a new Laravel project.

See the [Laravel docs](https://laravel.com/docs/10.x/installation#creating-a-
laravel-project) for more details.

Terminal

`  

_10

composer create-project laravel/laravel example-app

  
`

## Install the Authentication template#

Install [Laravel Breeze](https://laravel.com/docs/10.x/starter-kits#laravel-
breeze), a simple implementation of all of Laravel's [authentication
features](https://laravel.com/docs/10.x/authentication).

Terminal

`  

_10

composer require laravel/breeze --dev

_10

php artisan breeze:install

  
`

Note: this template does not use [Supabase Auth](/auth) but rather Laravel's
built in Auth system. This means that [Supabase Auth pricing](/pricing) does
not apply. You'd only be billed for Database resources used in this case.

## Set up the Postgres connection details#

Go to [database.new](https://database.new) and create a new Supabase project.
Save your database password securely.

When your project is up and running, navigate to the [database
settings](/dashboard/project/_/settings/database) to find the URI connection
string.

Laravel ships with a Postgres adapter out of the box, you can simply configure
it via the environment variables. You can find the database URL in your
[Supabase Dashboard](/dashboard/project/_/settings/database).

.env

`  

_10

DB_CONNECTION=pgsql

_10

DATABASE_URL=postgres://postgres.xxxx:[[email protected]](/cdn-cgi/l/email-
protection):5432/postgres

  
`

### Change the default schema#

By default Laravel uses the `public` schema. We recommend changing this as
supabase exposes the `public` schema as a [data API](/docs/guides/api).

You can change the schema of your Laravel application by modifying the
`search_path` variable `config/database.php`:

config/database.php

`  

_14

'pgsql' => [

_14

'driver' => 'pgsql',

_14

'url' => env('DATABASE_URL'),

_14

'host' => env('DB_HOST', '127.0.0.1'),

_14

'port' => env('DB_PORT', '5432'),

_14

'database' => env('DB_DATABASE', 'forge'),

_14

'username' => env('DB_USERNAME', 'forge'),

_14

'password' => env('DB_PASSWORD', ''),

_14

'charset' => 'utf8',

_14

'prefix' => '',

_14

'prefix_indexes' => true,

_14

'search_path' => 'laravel',

_14

'sslmode' => 'prefer',

_14

],

  
`

## Run the database migrations#

Laravel ships with database migration files that set up the required tables
for Laravel Authentication and User Management.

Terminal

`  

_10

php artisan migrate

  
`

## Start the app#

Terminal

`  

_10

php artisan serve

  
`

Run the development server. Go to <http://127.0.0.1:8000> in a browser to see
your application. You can also navigate to <http://127.0.0.1:8000/register>
and <http://127.0.0.1:8000/login> to register and log in users.

## Conclusion#

Supabase is the ideal platform for powering your Postgres database for your
Laravel applications! Every Supabase project comes with a full Postgres
database and a good number of [useful
extension](/docs/guides/database/extensions)!

Try it out now at [database.new](https://database.new)!

## More Supabase#

  * [Migration guides](/docs/guides/resources#migrate-to-supabase)
  * [Options for connecting to your Postgres database](/docs/guides/database/connecting-to-postgres)

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Flaravel-
postgres&text=Getting%20started%20with%20Laravel%20and%20Postgres)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Flaravel-
postgres&text=Getting%20started%20with%20Laravel%20and%20Postgres)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Flaravel-
postgres&t=Getting%20started%20with%20Laravel%20and%20Postgres)

[Last postHow pg_graphql works24 January 2024](/blog/how-pg-graphql-works)

[Next postWhat is SAML? A practical guide to the authentication protocol17
January 2024](/blog/what-is-saml-authentication)

[postgres](/blog/tags/postgres)[developers](/blog/tags/developers)[php](/blog/tags/php)

On this page

  * Create a Laravel Project
  * Install the Authentication template
  * Set up the Postgres connection details
    * Change the default schema
  * Run the database migrations
  * Start the app
  * Conclusion
  * More Supabase

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Flaravel-
postgres&text=Getting%20started%20with%20Laravel%20and%20Postgres)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Flaravel-
postgres&text=Getting%20started%20with%20Laravel%20and%20Postgres)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Flaravel-
postgres&t=Getting%20started%20with%20Laravel%20and%20Postgres)

## Build in a weekend, scale to millions

[Start your project](https://supabase.com/dashboard)[Request a
demo](/contact/sales)

