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

Javascript Reference v1.0

##### Version out of date

There's a newer version of this library! Migrate to the [newest
version](/docs/reference/javascript).

# JavaScript Client Library

@supabase/supabase-js[View on GitHub](https://github.com/supabase/supabase-js)

This reference documents every object and method available in Supabase's
isomorphic JavaScript library, supabase-js. You can use supabase-js to
interact with your Postgres database, listen to database changes, invoke Deno
Edge Functions, build login and user management functionality, and manage
large files.

* * *

## Initializing

Create a new client for use in the browser.

### Parameters

  * supabaseUrlRequiredstring

The unique Supabase URL which is supplied when you create a new project in
your project dashboard.

  * supabaseKeyRequiredstring

The unique Supabase Key which is supplied when you create a new project in
your project dashboard.

  * optionsOptionalSupabaseClientOptions

Details

Create ClientWith Additional ParametersAPI schemasCustom Fetch Implementation

`  

_10

import { createClient } from '@supabase/supabase-js'

_10

_10

// Create a single supabase client for interacting with your database

_10

const supabase = createClient('https://xyzcompany.supabase.co', 'public-anon-
key')

  
`

* * *

## Upgrade guide

supabase-js v2 focuses on "quality-of-life" improvements for developers and
addresses some of the largest pain points in v1. v2 includes type support, a
rebuilt Auth library with async methods, improved errors, and more.

No new features will be added to supabase-js v1 , but we'll continuing merging
security fixes to v1, with maintenance patches for the next 3 months.

## Upgrade the client library#

Install the latest version

`  

_10

npm install @supabase/supabase-js@2

  
`

_Optionally_ if you are using custom configuration with `createClient` then
follow below:

BeforeAfter

src/supabaseClient.ts

`  

_10

const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY, {

_10

schema: 'custom',

_10

persistSession: false,

_10

})

  
`

Read more about the [constructor options](/docs/reference/javascript/release-
notes#explicit-constructor-options).

### Auth methods#

The signIn() method has been deprecated in favor of more explicit method
signatures to help with type hinting. Previously it was difficult for
developers to know what they were missing (e.g., a lot of developers didn't
realize they could use passwordless magic links).

#### Sign in with email and password#

BeforeAfter

`  

_10

const { user, error } = await supabase

_10

.auth

_10

.signIn({ email, password })

  
`

#### Sign in with magic link#

BeforeAfter

`  

_10

const { error } = await supabase

_10

.auth

_10

.signIn({ email })

  
`

#### Sign in with a third-party provider#

BeforeAfter

`  

_10

const { error } = await supabase

_10

.auth

_10

.signIn({ provider })

  
`

#### Sign in with phone#

BeforeAfter

`  

_10

const { error } = await supabase

_10

.auth

_10

.signIn({ phone, password })

  
`

#### Sign in with phone using OTP#

BeforeAfter

`  

_10

const { error } = await supabase

_10

.auth

_10

.api

_10

.sendMobileOTP(phone)

  
`

#### Reset password for email#

BeforeAfter

`  

_10

const { data, error } = await supabase

_10

.auth

_10

.api

_10

.resetPasswordForEmail(email)

  
`

#### Get the user's current session#

Note that `auth.getSession` reads the auth token and the unencoded session
data from the local storage medium. It _doesn't_ send a request back to the
Supabase Auth server unless the local session is expired.

You should **never** trust the unencoded session data if you're writing server
code, since it could be tampered with by the sender. If you need verified,
trustworthy user data, call `auth.getUser` instead, which always makes a
request to the Auth server to fetch trusted data.

BeforeAfter

`  

_10

const session = supabase.auth.session()

  
`

#### Get the logged-in user#

BeforeAfter

`  

_10

const user = supabase.auth.user()

  
`

#### Update user data for a logged-in user#

BeforeAfter

`  

_10

const { user, error } = await supabase

_10

.auth

_10

.update({ attributes })

  
`

#### Use a custom `access_token` JWT with Supabase#

BeforeAfter

`  

_10

const { user, error } = supabase.auth.setAuth(access_token)

  
`

### Cookie methods#

The cookie-related methods like `setAuthCookie` and `getUserByCookie` have
been removed.

For Next.js you can use the [Auth
Helpers](https://supabase.com/docs/guides/auth/auth-helpers/nextjs) to help
you manage cookies. If you can't use the Auth Helpers, you can use [server-
side rendering](https://supabase.com/docs/guides/auth/server-side-rendering).

Some the [PR](https://github.com/supabase/gotrue-js/pull/340) for additional
background information.

### Data methods#

`.insert()` / `.upsert()` / `.update()` / `.delete()` don't return rows by
default: [PR](https://github.com/supabase/postgrest-js/pull/276).

Previously, these methods return inserted/updated/deleted rows by default
(which caused [some
confusion](https://github.com/supabase/supabase/discussions/1548)), and you
can opt to not return it by specifying `returning: 'minimal'`. Now the default
behavior is to not return rows. To return inserted/updated/deleted rows, add a
`.select()` call at the end.

#### Insert and return data#

BeforeAfter

`  

_10

const { data, error } = await supabase

_10

.from('my_table')

_10

.insert({ new_data })

  
`

#### Update and return data#

BeforeAfter

`  

_10

const { data, error } = await supabase

_10

.from('my_table')

_10

.update({ new_data })

_10

.eq('id', id)

  
`

#### Upsert and return data#

BeforeAfter

`  

_10

const { data, error } = await supabase

_10

.from('my_table')

_10

.upsert({ new_data })

  
`

#### Delete and return data#

BeforeAfter

`  

_10

const { data, error } = await supabase

_10

.from('my_table')

_10

.delete()

_10

.eq('id', id)

  
`

### Realtime methods#

#### Subscribe#

BeforeAfter

`  

_10

const userListener = supabase

_10

.from('users')

_10

.on('*', (payload) => handleAllEventsPayload(payload.new))

_10

.subscribe()

  
`

#### Unsubscribe#

BeforeAfter

`  

_10

userListener.unsubscribe()

  
`

* * *

## Fetch data

  * By default, Supabase projects will return a maximum of 1,000 rows. This setting can be changed in Project API Settings. It's recommended that you keep it low to limit the payload size of accidental or malicious requests. You can use `range()` queries to paginate through your data.
  * `select()` can be combined with [Modifiers](/docs/reference/javascript/using-modifiers)
  * `select()` can be combined with [Filters](/docs/reference/javascript/using-filters)
  * If using the Supabase hosted platform `apikey` is technically a reserved keyword, since the API gateway will pluck it out for authentication. [It should be avoided as a column name](https://github.com/supabase/supabase/issues/5465).

Getting your dataSelecting specific columnsQuery foreign tablesQuery the same
foreign table multiple timesFiltering with inner joinsQuerying with count
optionQuerying JSON dataReturn data as CSVAborting requests in-flight

`  

_10

const { data, error } = await supabase

_10

.from('cities')

_10

.select()

  
`

* * *

## Insert data

  * By default, every time you run `insert()`, the client library will make a `select` to return the full record. This is convenient, but it can also cause problems if your Policies are not configured to allow the `select` operation. If you are using Row Level Security and you are encountering problems, try setting the `returning` param to `minimal`.

Create a recordBulk createUpsert

`  

_10

const { data, error } = await supabase

_10

.from('cities')

_10

.insert([

_10

{ name: 'The Shire', country_id: 554 }

_10

])

  
`

* * *

## Update data

  * `update()` should always be combined with [Filters](/docs/reference/javascript/using-filters) to target the item(s) you wish to update.

Updating your dataUpdating JSON data

`  

_10

const { data, error } = await supabase

_10

.from('cities')

_10

.update({ name: 'Middle Earth' })

_10

.match({ name: 'Auckland' })

  
`

* * *

## Upsert data

  * Primary keys should be included in the data payload in order for an update to work correctly.
  * Primary keys must be natural, not surrogate. There are however, [workarounds](https://github.com/PostgREST/postgrest/issues/1118) for surrogate primary keys.
  * If you need to insert new data and update existing data at the same time, use [Postgres triggers](https://github.com/supabase/postgrest-js/issues/173#issuecomment-825124550).

Upsert your dataBulk Upsert your dataUpserting into tables with
constraintsReturn the exact number of rows

`  

_10

const { data, error } = await supabase

_10

.from('messages')

_10

.upsert({ id: 3, message: 'foo', username: 'supabot' })

  
`

* * *

## Delete data

  * `delete()` should always be combined with [filters](/docs/reference/javascript/using-filters) to target the item(s) you wish to delete.
  * If you use `delete()` with filters and you have [RLS](/docs/learn/auth-deep-dive/auth-row-level-security) enabled, only rows visible through `SELECT` policies are deleted. Note that by default no rows are visible, so you need at least one `SELECT`/`ALL` policy that makes the rows visible.

Delete records

`  

_10

const { data, error } = await supabase

_10

.from('cities')

_10

.delete()

_10

.match({ id: 666 })

  
`

* * *

## Call a Postgres function

You can call Postgres functions as _Remote Procedure Calls_ , logic in your
database that you can execute from anywhere. Functions are useful when the
logic rarely changes—like for password resets and updates.

`  

_10

create or replace function hello_world() returns text as $$

_10

select 'Hello world';

_10

$$ language sql;

  
`

Call a Postgres function without argumentsCall a Postgres function with
argumentsBulk processingCall a Postgres function with filtersCall a Postgres
function with a count option

`  

_10

const { data, error } = await supabase

_10

.rpc('hello_world')

  
`

* * *

## Using filters

Filters can be used on `select()`, `update()`, and `delete()` queries.

If a Postgres function returns a table response, you can also apply filters.

### Applying Filters#

You must apply your filters to the end of your query. For example:

`  

_10

const { data, error } = await supabase

_10

.from('cities')

_10

.select('name, country_id')

_10

.eq('name', 'The Shire') // Correct

_10

_10

const { data, error } = await supabase

_10

.from('cities')

_10

.eq('name', 'The Shire') // Incorrect

_10

.select('name, country_id')

  
`

### Chaining#

Filters can be chained together to produce advanced queries. For example:

`  

_10

const { data, error } = await supabase

_10

.from('cities')

_10

.select('name, country_id')

_10

.gte('population', 1000)

_10

.lt('population', 10000)

  
`

### Conditional Chaining#

Filters can be built up one step at a time and then executed. For example:

`  

_13

const filterByName = null

_13

const filterPopLow = 1000

_13

const filterPopHigh = 10000

_13

_13

let query = supabase

_13

.from('cities')

_13

.select('name, country_id')

_13

_13

if (filterByName) { query = query.eq('name', filterByName) }

_13

if (filterPopLow) { query = query.gte('population', filterPopLow) }

_13

if (filterPopHigh) { query = query.lt('population', filterPopHigh) }

_13

_13

const { data, error } = await query

  
`

* * *

## Column is equal to a value

With `select()`With `update()`With `delete()`With `rpc()`

`  

_10

const { data, error } = await supabase

_10

.from('cities')

_10

.select('name, country_id')

_10

.eq('name', 'The shire')

  
`

* * *

## Column is not equal to a value

With `select()`With `update()`With `delete()`With `rpc()`

`  

_10

const { data, error } = await supabase

_10

.from('cities')

_10

.select('name, country_id')

_10

.neq('name', 'The shire')

  
`

* * *

## Column is greater than a value

With `select()`With `update()`With `delete()`With `rpc()`

`  

_10

const { data, error } = await supabase

_10

.from('cities')

_10

.select('name, country_id')

_10

.gt('country_id', 250)

  
`

* * *

## Column is greater than or equal to a value

With `select()`With `update()`With `delete()`With `rpc()`

`  

_10

const { data, error } = await supabase

_10

.from('cities')

_10

.select('name, country_id')

_10

.gte('country_id', 250)

  
`

* * *

## Column is less than a value

With `select()`With `update()`With `delete()`With `rpc()`

`  

_10

const { data, error } = await supabase

_10

.from('cities')

_10

.select('name, country_id')

_10

.lt('country_id', 250)

  
`

* * *

## Column is less than or equal to a value

With `select()`With `update()`With `delete()`With `rpc()`

`  

_10

const { data, error } = await supabase

_10

.from('cities')

_10

.select('name, country_id')

_10

.lte('country_id', 250)

  
`

* * *

## Column matches a pattern

With `select()`With `update()`With `delete()`With `rpc()`

`  

_10

const { data, error } = await supabase

_10

.from('cities')

_10

.select('name, country_id')

_10

.like('name', '%la%')

  
`

* * *

## Column matches a case-insensitive pattern

With `select()`With `update()`With `delete()`With `rpc()`

`  

_10

const { data, error } = await supabase

_10

.from('cities')

_10

.select('name, country_id')

_10

.ilike('name', '%la%')

  
`

* * *

## Column is a value

With `select()`With `update()`With `delete()`With `rpc()`

`  

_10

const { data, error } = await supabase

_10

.from('cities')

_10

.select('name, country_id')

_10

.is('name', null)

  
`

* * *

## Column is in an array

With `select()`With `update()`With `delete()`With `rpc()`

`  

_10

const { data, error } = await supabase

_10

.from('cities')

_10

.select('name, country_id')

_10

.in('name', ['Rio de Janeiro', 'San Francisco'])

  
`

* * *

## Column contains every element in a value

  * `.contains()` can work on array columns or range columns. It is very useful for finding rows where a tag array contains all the values in the filter array.

`  

_10

.contains('arraycol',["a","b"]) // You can use a javascript array for an array
column

_10

.contains('arraycol','{"a","b"}') // You can use a string with Postgres array
{} for array column.

_10

.contains('rangecol','(1,2]') // Use Postgres range syntax for range column.

_10

.contains('rangecol',`(${arr}]`) // You can insert an array into a string.

  
`

With `select()`With `update()`With `delete()`With `rpc()`

`  

_10

const { data, error } = await supabase

_10

.from('countries')

_10

.select('name, id, main_exports')

_10

.contains('main_exports', ['oil'])

  
`

* * *

## Contained by value

  * `.containedBy()` can work on array columns or range columns.

`  

_10

.containedBy('arraycol',["a","b"]) // You can use a javascript array for an
array column

_10

.containedBy('arraycol','{"a","b"}') // You can use a string with Postgres
array {} for array column.

_10

.containedBy('rangecol','(1,2]') // Use Postgres range syntax for range
column.

_10

.containedBy('rangecol',`(${arr}]`) // You can insert an array into a string.

  
`

With `select()`With `update()`With `delete()`With `rpc()`

`  

_10

const { data, error } = await supabase

_10

.from('countries')

_10

.select('name, id, main_exports')

_10

.containedBy('main_exports', ['cars', 'food', 'machine'])

  
`

* * *

## Greater than a range

With `select()`With `update()`With `delete()`With `rpc()`

`  

_10

const { data, error } = await supabase

_10

.from('countries')

_10

.select('name, id, population_range_millions')

_10

.rangeGt('population_range_millions', '[150, 250]')

  
`

* * *

## Greater than or equal to a range

With `select()`With `update()`With `delete()`With `rpc()`

`  

_10

const { data, error } = await supabase

_10

.from('countries')

_10

.select('name, id, population_range_millions')

_10

.rangeGte('population_range_millions', '[150, 250]')

  
`

* * *

## Less than or equal to a range

With `select()`With `update()`With `delete()`With `rpc()`

`  

_10

const { data, error } = await supabase

_10

.from('countries')

_10

.select('name, id, population_range_millions')

_10

.rangeLt('population_range_millions', '[150, 250]')

  
`

* * *

## Mutually exclusive to a range

With `select()`With `update()`With `delete()`With `rpc()`

`  

_10

const { data, error } = await supabase

_10

.from('countries')

_10

.select('name, id, population_range_millions')

_10

.rangeAdjacent('population_range_millions', '[70, 185]')

  
`

* * *

## With a common element

  * `.overlaps()` can work on array columns or range columns.

`  

_10

.overlaps('arraycol',["a","b"]) // You can use a javascript array for an array
column

_10

.overlaps('arraycol','{"a","b"}') // You can use a string with Postgres array
{} for array column.

_10

.overlaps('rangecol','(1,2]') // Use Postgres range syntax for range column.

_10

.overlaps('rangecol',`(${arr}]`) // You can insert an array into a string.

  
`

With `select()`With `update()`With `delete()`With `rpc()`

`  

_10

const { data, error } = await supabase

_10

.from('countries')

_10

.select('name, id, main_exports')

_10

.overlaps('main_exports', ['computers', 'minerals'])

  
`

* * *

## Match a string

Text searchBasic normalizationFull normalizationWebsearch

`  

_10

const { data, error } = await supabase

_10

.from('quotes')

_10

.select('catchphrase')

_10

.textSearch('catchphrase', `'fat' & 'cat'`, {

_10

config: 'english'

_10

})

  
`

* * *

## Match an associated value

With `select()`With `update()`With `delete()`With `rpc()`

`  

_10

const { data, error } = await supabase

_10

.from('cities')

_10

.select('name, country_id')

_10

.match({name: 'Beijing', country_id: 156})

  
`

* * *

## Don't match the filter

  * `.not()` expects you to use the raw [PostgREST syntax](https://postgrest.org/en/stable/api.html#horizontal-filtering-rows) for the filter names and values.

`  

_10

.not('name','eq','Paris')

_10

.not('arraycol','cs','{"a","b"}') // Use Postgres array {} for array column
and 'cs' for contains.

_10

.not('rangecol','cs','(1,2]') // Use Postgres range syntax for range column.

_10

.not('id','in','(6,7)') // Use Postgres list () for in filter.

_10

.not('id','in',`(${arr})`) // You can insert a javascript array.

  
`

With `select()`With `update()`With `delete()`With `rpc()`

`  

_10

const { data, error } = await supabase

_10

.from('cities')

_10

.select('name, country_id')

_10

.not('name', 'eq', 'Paris')

  
`

* * *

## Match at least one filter

  * `.or()` expects you to use the raw [PostgREST syntax](https://postgrest.org/en/stable/api.html#horizontal-filtering-rows) for the filter names and values.

`  

_10

.or('id.in.(6,7), arraycol.cs.{"a","b"}') // Use Postgres list () for in
filter. Array {} for array column and 'cs' for contains.

_10

.or(`id.in.(${arrList}),arraycol.cs.{${arr}}`) // You can insert a javascipt
array for list or array on array column.

_10

.or(`id.in.(${arrList}),rangecol.cs.[${arrRange})`) // You can insert a
javascipt array for list or range on a range column.

  
`

With `select()`Use `or` with `and`Use `or` on foreign tables

`  

_10

const { data, error } = await supabase

_10

.from('cities')

_10

.select('name, country_id')

_10

.or('id.eq.20,id.eq.30')

  
`

* * *

## Match the filter

  * `.filter()` expects you to use the raw [PostgREST syntax](https://postgrest.org/en/stable/api.html#horizontal-filtering-rows) for the filter names and values, so it should only be used as an escape hatch in case other filters don't work.

`  

_10

.filter('arraycol','cs','{"a","b"}') // Use Postgres array {} for array column
and 'cs' for contains.

_10

.filter('rangecol','cs','(1,2]') // Use Postgres range syntax for range
column.

_10

.filter('id','in','(6,7)') // Use Postgres list () for in filter.

_10

.filter('id','in',`(${arr})`) // You can insert a javascript array.

  
`

With `select()`With `update()`With `delete()`With `rpc()`Filter embedded
resources

`  

_10

const { data, error } = await supabase

_10

.from('cities')

_10

.select('name, country_id')

_10

.filter('name', 'in', '("Paris","Tokyo")')

  
`

* * *

## Using modifiers

Modifiers can be used on `select()` queries.

If a Postgres function returns a table response, you can also apply modifiers
to the `rpc()` function.

* * *

## Order the results

With `select()`With embedded resourcesOrdering multiple columns

`  

_10

const { data, error } = await supabase

_10

.from('cities')

_10

.select('name, country_id')

_10

.order('id', { ascending: false })

  
`

* * *

## Limit the number of rows returned

With `select()`With embedded resources

`  

_10

const { data, error } = await supabase

_10

.from('cities')

_10

.select('name, country_id')

_10

.limit(1)

  
`

* * *

## Limit the query to a range

With `select()`

`  

_10

const { data, error } = await supabase

_10

.from('cities')

_10

.select('name, country_id')

_10

.range(0,3)

  
`

* * *

## Retrieve one row of data

With `select()`

`  

_10

const { data, error } = await supabase

_10

.from('cities')

_10

.select('name, country_id')

_10

.limit(1)

_10

.single()

  
`

* * *

## Retrieve zero or one row of data

With `select()`

`  

_10

const { data, error } = await supabase

_10

.from('cities')

_10

.select('name, country_id')

_10

.eq('name', 'Singapore')

_10

.maybeSingle()

  
`

* * *

## Create a new user

  * By default, the user will need to verify their email address before logging in. If you would like to change this, you can disable "Email Confirmations" by going to Authentication -> Settings on [supabase.com/dashboard](https://supabase.com/dashboard)
  * If "Email Confirmations" is turned on, a `user` is returned but `session` will be null
  * If "Email Confirmations" is turned off, both a `user` and a `session` will be returned
  * When the user confirms their email address, they will be redirected to localhost:3000 by default. To change this, you can go to Authentication -> Settings on [supabase.com/dashboard](https://supabase.com/dashboard)
  * If signUp() is called for an existing confirmed user:
    * If "Enable email confirmations" is enabled on the "Authentication" -> "Settings" page, an obfuscated / fake user object will be returned.
    * If "Enable email confirmations" is disabled, an error with a message "User already registered" will be returned.
  * To check if a user already exists, refer to getUser().

Sign up.Sign up with additional user meta data.Sign up with third-party
providers.Sign up with Phone.

`  

_10

const { user, session, error } = await supabase.auth.signUp({

_10

email: '[[email protected]](/cdn-cgi/l/email-protection)',

_10

password: 'example-password',

_10

})

  
`

* * *

## Listen to auth events

Listen to auth changesListen to sign inListen to sign outListen to token
refreshListen to user updatesListen to user deletedListen to password recovery
events

`  

_10

supabase.auth.onAuthStateChange((event, session) => {

_10

console.log(event, session)

_10

})

  
`

* * *

## Sign in a user

  * A user can sign up either via email or OAuth.
  * If you provide `email` without a `password`, the user will be sent a magic link.
  * The magic link's destination URL is determined by the SITE_URL config variable. To change this, you can go to Authentication -> Settings on [supabase.com/dashboard](https://supabase.com/dashboard)
  * Specifying a `provider` will open the browser to the relevant login page.

Sign in with email and passwordSign in with magic link.Sign in using third-
party providers.Sign in with phone and passwordSign in using a third-party
provider with redirectSign in with scopesSign in using a refresh token (e.g.
in React Native).

`  

_10

const { user, session, error } = await supabase.auth.signIn({

_10

email: '[[email protected]](/cdn-cgi/l/email-protection)',

_10

password: 'example-password',

_10

})

  
`

* * *

## Sign out a user

Sign out

`  

_10

const { error } = await supabase.auth.signOut()

  
`

* * *

## Send a password reset request

Sends a password reset request to an email address.

  * When the user clicks the reset link in the email they are redirected back to your application. You can configure the URL that the user is redirected to via the `redirectTo` param. See [redirect URLs and wildcards](/docs/guides/auth/overview#redirect-urls-and-wildcards) to add additional redirect URLs to your project.
  * After the user has been redirected successfully, prompt them for a new password and call `updateUser()`:

`  

_10

const { data, error } = await supabase.auth.update({

_10

password: new_password,

_10

})

  
`

Reset passwordReset password (React)

`  

_10

const { data, error } = await supabase.auth.api.resetPasswordForEmail(

_10

email,

_10

{ redirectTo: 'https://example.com/update-password' }

_10

)

  
`

* * *

## Update a user

User email: By Default, email updates sends a confirmation link to both the
user's current and new email. To only send a confirmation link to the user's
new email, disable **Secure email change** in your project's [email auth
provider settings](https://supabase.com/dashboard/project/_/auth/providers).

User metadata: It's generally better to store user data in a table within your
public schema (i.e., `public.users`). Use the `update()` method if you have
data which rarely changes or is specific only to the logged in user.

Update the email for an authenticated userUpdate the password for an
authenticated userUpdate the user's metadata

`  

_10

const { user, error } = await supabase.auth.update({email: '[[email
protected]](/cdn-cgi/l/email-protection)'})

  
`

Notes

* * *

## Update the access token

Basic example.With Express.

`  

_11

function apiFunction(req, res) {

_11

// Assuming the access token was sent as a header "X-Supabase-Auth"

_11

const { access_token } = req.get('X-Supabase-Auth')

_11

_11

// You can now use it within a Supabase Client

_11

const supabase = createClient("https://xyzcompany.supabase.co", "public-anon-
key")

_11

const { user, error } = supabase.auth.setAuth(access_token)

_11

_11

// This client will now send requests as this user

_11

const { data } = await supabase.from('your_table').select()

_11

}

  
`

Notes

* * *

## Retrieve a user

This method gets the user object from memory.

Get the logged in user

`  

_10

const user = supabase.auth.user()

  
`

* * *

## Retrieve a session

Get the session data

`  

_10

const session = supabase.auth.session()

  
`

* * *

## Retrieve a user

  * Fetches the user object from the database instead of local storage.
  * Note that user() fetches the user object from local storage which might not be the most updated.
  * Requires the user's access_token.

Fetch the user object using the access_token jwt.

`  

_10

const { user, error } = await supabase.auth.api.getUser(

_10

'ACCESS_TOKEN_JWT',

_10

)

  
`

* * *

## Invokes a Supabase Edge Function.

Invokes a function

Invokes a Supabase Edge Function.

  * Requires an Authorization header.
  * Invoke params generally match the [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) spec.

### Parameters

  * functionNameRequiredstring

The name of the Function to invoke.

  * optionsRequiredFunctionInvokeOptions

Options for invoking the Function.

Details

### Return Type

Promise<Union: expand to see options>

Basic invocation.Specifying response type.Passing custom headers.

`  

_10

const { data, error } = await supabase.functions.invoke('hello', {

_10

body: JSON.stringify({ foo: 'bar' })

_10

})

  
`

* * *

## Subscribe to channel

  * Realtime is disabled by default for new Projects for better database performance and security. You can turn it on by [managing replication](/docs/guides/database/api#managing-realtime).
  * If you want to receive the "previous" data for updates and deletes, you will need to set `REPLICA IDENTITY` to `FULL`, like this: `ALTER TABLE your_table REPLICA IDENTITY FULL;`

Listen to all database changesListen to a specific tableListen to
insertsListen to updatesListen to deletesListen to multiple eventsListen to
row level changes

`  

_10

const mySubscription = supabase

_10

.from('*')

_10

.on('*', payload => {

_10

console.log('Change received!', payload)

_10

})

_10

.subscribe()

  
`

* * *

## Remove a subscription

  * Removing subscriptions is a great way to maintain the performance of your project's database. Supabase will automatically handle cleanup 30 seconds after a user is disconnected, but unused subscriptions may cause degradation as more users are simultaneously subscribed.

Remove a subscription

`  

_10

supabase.removeSubscription(mySubscription)

  
`

* * *

## Remove all subscriptions

  * Removing subscriptions is a great way to maintain the performance of your project's database. Supabase will automatically handle cleanup 30 seconds after a user is disconnected, but unused subscriptions may cause degradation as more users are simultaneously subscribed.

Removes all subscriptions

`  

_10

supabase.removeAllSubscriptions()

  
`

* * *

## Retrieve subscriptions

Get all subscriptions

`  

_10

const subscriptions = supabase.getSubscriptions()

  
`

* * *

## Create a bucket

  * Policy permissions required:
    * `buckets` permissions: `insert`
    * `objects` permissions: none

Create bucket

`  

_10

const { data, error } = await supabase

_10

.storage

_10

.createBucket('avatars', { public: false })

  
`

* * *

## Retrieve a bucket

  * Policy permissions required:
    * `buckets` permissions: `select`
    * `objects` permissions: none

Get bucket

`  

_10

const { data, error } = await supabase

_10

.storage

_10

.getBucket('avatars')

  
`

* * *

## List all buckets

  * Policy permissions required:
    * `buckets` permissions: `select`
    * `objects` permissions: none

List buckets

`  

_10

const { data, error } = await supabase

_10

.storage

_10

.listBuckets()

  
`

* * *

## Update a bucket

  * Policy permissions required:
    * `buckets` permissions: `update`
    * `objects` permissions: none

Update bucket

`  

_10

const { data, error } = await supabase

_10

.storage

_10

.updateBucket('avatars', { public: false })

  
`

* * *

## Delete a bucket

  * Policy permissions required:
    * `buckets` permissions: `select` and `delete`
    * `objects` permissions: none

Delete bucket

`  

_10

const { data, error } = await supabase

_10

.storage

_10

.deleteBucket('avatars')

  
`

* * *

## Empty a bucket

  * Policy permissions required:
    * `buckets` permissions: `select`
    * `objects` permissions: `select` and `delete`

Empty bucket

`  

_10

const { data, error } = await supabase

_10

.storage

_10

.emptyBucket('avatars')

  
`

* * *

## Upload a file

  * Policy permissions required:
    * `buckets` permissions: none
    * `objects` permissions: `insert`
  * For React Native, using either `Blob`, `File` or `FormData` does not work as intended. Upload file using `ArrayBuffer` from base64 file data instead, see example below.

Upload fileUpload file using `ArrayBuffer` from base64 file data

`  

_10

const avatarFile = event.target.files[0]

_10

const { data, error } = await supabase

_10

.storage

_10

.from('avatars')

_10

.upload('public/avatar1.png', avatarFile, {

_10

cacheControl: '3600',

_10

upsert: false

_10

})

  
`

* * *

## Download a file

  * Policy permissions required:
    * `buckets` permissions: none
    * `objects` permissions: `select`

Download file

`  

_10

const { data, error } = await supabase

_10

.storage

_10

.from('avatars')

_10

.download('folder/avatar1.png')

  
`

* * *

## List all files in a bucket

  * Policy permissions required:
    * `buckets` permissions: none
    * `objects` permissions: `select`

List files in a bucketSearch files in a bucket

`  

_10

const { data, error } = await supabase

_10

.storage

_10

.from('avatars')

_10

.list('folder', {

_10

limit: 100,

_10

offset: 0,

_10

sortBy: { column: 'name', order: 'asc' },

_10

})

  
`

* * *

## Replace an existing file

  * Policy permissions required:
    * `buckets` permissions: none
    * `objects` permissions: `update` and `select`
  * For React Native, using either `Blob`, `File` or `FormData` does not work as intended. Update file using `ArrayBuffer` from base64 file data instead, see example below.

Update fileUpdate file using `ArrayBuffer` from base64 file data

`  

_10

const avatarFile = event.target.files[0]

_10

const { data, error } = await supabase

_10

.storage

_10

.from('avatars')

_10

.update('public/avatar1.png', avatarFile, {

_10

cacheControl: '3600',

_10

upsert: false

_10

})

  
`

* * *

## Move an existing file

  * Policy permissions required:
    * `buckets` permissions: none
    * `objects` permissions: `update` and `select`

Move file

`  

_10

const { data, error } = await supabase

_10

.storage

_10

.from('avatars')

_10

.move('public/avatar1.png', 'private/avatar2.png')

  
`

* * *

## Copy an existing file

  * Policy permissions required:
    * `buckets` permissions: none
    * `objects` permissions: `insert` and `select`

Copy file

`  

_10

const { data, error } = await supabase

_10

.storage

_10

.from('avatars')

_10

.copy('public/avatar1.png', 'private/avatar2.png')

  
`

* * *

## Delete files in a bucket

  * Policy permissions required:
    * `buckets` permissions: none
    * `objects` permissions: `delete` and `select`

Delete file

`  

_10

const { data, error } = await supabase

_10

.storage

_10

.from('avatars')

_10

.remove(['folder/avatar1.png'])

  
`

* * *

## Create a signed URL

  * Policy permissions required:
    * `buckets` permissions: none
    * `objects` permissions: `select`

Create Signed URL

`  

_10

const { signedURL, error } = await supabase

_10

.storage

_10

.from('avatars')

_10

.createSignedUrl('folder/avatar1.png', 60)

  
`

* * *

## Create signed URLs

  * Policy permissions required:
    * `buckets` permissions: none
    * `objects` permissions: `select`

Create Signed URLs

`  

_10

const { data, error } = await supabase

_10

.storage

_10

.from('avatars')

_10

.createSignedUrls(['folder/avatar1.png', 'folder/avatar2.png'], 60)

  
`

* * *

## Retrieve public URL

  * The bucket needs to be set to public, either via [updateBucket()](/docs/reference/javascript/storage-updatebucket) or by going to Storage on [supabase.com/dashboard](https://supabase.com/dashboard), clicking the overflow menu on a bucket and choosing "Make public"
  * Policy permissions required:
    * `buckets` permissions: none
    * `objects` permissions: none

Returns the URL for an asset in a public bucket

`  

_10

const { publicURL, error } = supabase

_10

.storage

_10

.from('public-bucket')

_10

.getPublicUrl('folder/avatar1.png')

  
`

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

