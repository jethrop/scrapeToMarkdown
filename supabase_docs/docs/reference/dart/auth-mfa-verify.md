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

Dart Reference v2.0

# Flutter Client Library

supabase_flutter[View on GitHub](https://github.com/supabase/supabase-flutter)

This reference documents every object and method available in Supabase's
Flutter library, [supabase-
flutter](https://pub.dev/packages/supabase_flutter). You can use supabase-
flutter to interact with your Postgres database, listen to database changes,
invoke Deno Edge Functions, build login and user management functionality, and
manage large files.

We also provide a [supabase](https://pub.dev/packages/supabase) package for
non-Flutter projects.

* * *

## Installing

### Install from pub.dev#

You can install Supabase package from
[pub.dev](https://pub.dev/packages/supabase_flutter)

FlutterOther Dart Project

Terminal

`  

_10

flutter pub add supabase_flutter

  
`

* * *

## Initializing

You can initialize Supabase with the static `initialize()` method of the
`Supabase` class.

The Supabase client is your entrypoint to the rest of the Supabase
functionality and is the easiest way to interact with everything we offer
within the Supabase ecosystem.

### Parameters

  * urlRequiredstring

The unique Supabase URL which is supplied when you create a new project in
your project dashboard.

  * anonKeyRequiredstring

The unique Supabase Key which is supplied when you create a new project in
your project dashboard.

  * headersOptionalMap<String, String>

Custom header to be passed to the Supabase client.

  * httpClientOptionalClient

Custom http client to be used by the Supabase client.

  * authOptionsOptionalFlutterAuthClientOptions

Options to change the Auth behaviors.

Details

  * postgrestOptionsOptionalPostgrestClientOptions

Options to change the Postgrest behaviors.

Details

  * realtimeClientOptionsOptionalRealtimeClientOptions

Options to change the Realtime behaviors.

Details

  * storageOptionsOptionalStorageClientOptions

Options to change the Storage behaviors.

Details

For FlutterFor other Dart projects

`  

_11

Future<void> main() async {

_11

await Supabase.initialize(

_11

url: 'https://xyzcompany.supabase.co',

_11

anonKey: 'public-anon-key',

_11

);

_11

_11

runApp(MyApp());

_11

}

_11

_11

// Get a reference your Supabase client

_11

final supabase = Supabase.instance.client;

  
`

* * *

## Upgrade guide

Although `supabase_flutter` v2 brings a few breaking changes, for the most
part the public API should be the same with a few minor exceptions. We have
brought numerous updates behind the scenes to make the SDK work more
intuitively for Flutter and Dart developers.

## Upgrade the client library#

Make sure you are using v2 of the client library in your `pubspec.yaml` file.

`  

_10

supabase_flutter: ^2.0.0

  
`

_Optionally_ passing custom configuration to `Supabase.initialize()` is now
organized into separate objects:

BeforeAfter

main.dart

`  

_10

await Supabase.initialize(

_10

url: supabaseUrl,

_10

anonKey: supabaseKey,

_10

authFlowType: AuthFlowType.pkce,

_10

storageRetryAttempts: 10,

_10

realtimeClientOptions: const RealtimeClientOptions(

_10

logLevel: RealtimeLogLevel.info,

_10

),

_10

);

  
`

### Auth updates#

#### Renaming Provider to OAuthProvider#

`Provider` enum is renamed to `OAuthProvider`. Previously the `Provider`
symbol often collided with classes in the
[provider](https://pub.dev/packages/provider) package and developers needed to
add import prefixes to avoid collisions. With the new update, developers can
use Supabase and Provider in the same codebase without any import prefixes.

BeforeAfter

`  

_10

await supabase.auth.signInWithOAuth(

_10

Provider.google,

_10

);

  
`

#### Sign in with Apple method deprecated#

We have removed the
[sign_in_with_apple](https://pub.dev/packages/sign_in_with_apple) dependency
in v2. This is because not every developer needs to sign in with Apple, and we
want to reduce the number of dependencies in the library.

With v2, you can import
[sign_in_with_apple](https://pub.dev/packages/sign_in_with_apple) as a
separate dependency if you need to sign in with Apple. We have also added
`auth.generateRawNonce()` method to easily generate a secure nonce.

BeforeAfter

`  

_10

await supabase.auth.signInWithApple();

  
`

#### Initialization does not await for session refresh#

In v1, `Supabase.initialize()` would await for the session to be refreshed
before returning. This caused delays in the app's launch time, especially when
the app is opened in a poor network environment.

In v2, `Supabase.initialize()` returns immediately after obtaining the session
from the local storage, which makes the app launch faster. Because of this,
there is no guarantee that the session is valid when the app starts.

If you need to make sure the session is valid, you can access the `isExpired`
getter to check if the session is valid. If the session is expired, you can
listen to the `onAuthStateChange` event and wait for a new `tokenRefreshed`
event to be fired.

BeforeAfter

`  

_10

// Session is valid, no check required

_10

final session = supabase.auth.currentSession;

  
`

#### Removing Flutter Webview dependency for OAuth sign in#

In v1, on iOS you could pass a `BuildContext` to the `signInWithOAuth()`
method to launch the OAuth flow in a Flutter Webview.

In v2, we have dropped the
[webview_flutter](https://pub.dev/packages/webview_flutter) dependency in v2
to allow you to have full control over the UI of the OAuth flow. We now have
[native support for Google and Apple sign in](/docs/reference/dart/auth-
signinwithidtoken), so opening an external browser is no longer needed on iOS.

Because of this update, we no longer need the `context` parameter, so we have
removed the `context` parameter from the `signInWithOAuth()` method.

BeforeAfter

`  

_10

// Opens a webview on iOS.

_10

await supabase.auth.signInWithOAuth(

_10

Provider.github,

_10

authScreenLaunchMode: LaunchMode.inAppWebView,

_10

context: context,

_10

);

  
`

#### PKCE is the default auth flow type#

[PKCE flow](https://supabase.com/blog/supabase-auth-sso-pkce#introducing-
pkce), which is a more secure method for obtaining sessions from deep links,
is now the default auth flow for any authentication involving deep links.

BeforeAfter

`  

_10

await Supabase.initialize(

_10

url: 'SUPABASE_URL',

_10

anonKey: 'SUPABASE_ANON_KEY',

_10

authFlowType: AuthFlowType.implicit, // set to implicit by default

_10

);

  
`

#### Auth callback host name parameter removed#

`Supabase.initialize()` no longer has the `authCallbackUrlHostname` parameter.
The `supabase_flutter` SDK will automatically detect auth callback URLs and
handle them internally.

BeforeAfter

`  

_10

await Supabase.initialize(

_10

url: 'SUPABASE_URL',

_10

anonKey: 'SUPABASE_ANON_KEY',

_10

authCallbackUrlHostname: 'auth-callback',

_10

);

  
`

#### SupabaseAuth class removed#

The `SupabaseAuth` had an `initialSession` member, which was used to obtain
the initial session upon app start. This is now removed, and `currentSession`
should be used to access the session at any time.

BeforeAfter

`  

_10

// Use `initialSession` to obtain the initial session when the app starts.

_10

final initialSession = await SupabaseAuth.initialSession;

  
`

### Data methods#

#### Insert and return data#

We made the query builder immutable, which means you can reuse the same query
object to chain multiple filters and get the expected outcome.

BeforeAfter

`  

_10

// If you declare a query and chain filters on it

_10

final myQuery = supabase.from('my_table').select();

_10

_10

final foo = await myQuery.eq('some_col', 'foo');

_10

_10

// The `eq` filter above is applied in addition to the following filter

_10

final bar = await myQuery.eq('another_col', 'bar');

  
`

#### Renaming is and in filter#

Because `is` and `in` are [reserved
keywords](https://dart.dev/languages/keywords) in Dart, v1 used `is_` and
`in_` as query filter names. Users found the underscore confusing, so the
query filters are now renamed to `isFilter` and `inFilter`.

BeforeAfter

`  

_10

final data = await supabase

_10

.from('users')

_10

.select()

_10

.is_('status', null);

_10

_10

final data = await supabase

_10

.from('users')

_10

.select()

_10

.in_('status', ['ONLINE', 'OFFLINE']);

  
`

#### Deprecate FetchOption in favor of `count()` and `head()` methods#

`FetchOption()` on `.select()` is now deprecated, and new `.count()` and
`head()` methods are added to the query builder.

`count()` on `.select()` performs the select while also getting the count
value, and `.count()` directly on `.from()` performs a head request resulting
in only fetching the count value.

BeforeAfter

`  

_22

// Request with count option

_22

final res = await supabase.from('cities').select(

_22

'name',

_22

const FetchOptions(

_22

count: CountOption.exact,

_22

),

_22

);

_22

_22

final data = res.data;

_22

final count = res.count;

_22

_22

// Request with count and head option

_22

// obtains the count value without fetching the data.

_22

final res = await supabase.from('cities').select(

_22

'name',

_22

const FetchOptions(

_22

count: CountOption.exact,

_22

head: true,

_22

),

_22

);

_22

_22

final count = res.count;

  
`

#### PostgREST error codes#

The `PostgrestException` instance thrown by the API methods has a `code`
property. In v1, the `code` property contained the http status code.

In v2, the `code` property contains the [PostgREST error
code](https://postgrest.org/en/stable/references/errors.html), which is more
useful for debugging.

BeforeAfter

`  

_10

try {

_10

await supabase.from('countries').select();

_10

} on PostgrestException catch (error) {

_10

error.code; // Contains http status code

_10

}

  
`

### Realtime methods#

Realtime methods contains the biggest breaking changes. Most of these changes
are to make the interface more type safe.

We have removed the `.on()` method and replaced it with
`.onPostgresChanges()`, `.onBroadcast()`, and three different presence
methods.

#### Postgres Changes#

Use the new `.onPostgresChanges()` method to listen to realtime changes in the
database.

In v1, filters were not strongly typed because they took a `String` type. In
v2, `filter` takes an object. Its properties are strictly typed to catch type
errors.

The payload of the callback is now typed as well. In `v1`, the payload was
returned as `dynamic`. It is now returned as a `PostgresChangePayload` object.
The object contains the `oldRecord` and `newRecord` properties for accessing
the data before and after the change.

BeforeAfter

`  

_13

supabase.channel('my_channel').on(

_13

RealtimeListenTypes.postgresChanges,

_13

ChannelFilter(

_13

event: '*',

_13

schema: 'public',

_13

table: 'messages',

_13

filter: 'room_id=eq.200',

_13

),

_13

(dynamic payload, [ref]) {

_13

final Map<String, dynamic> newRecord = payload['new'];

_13

final Map<String, dynamic> oldRecord = payload['old'];

_13

},

_13

).subscribe();

  
`

#### Broadcast#

Broadcast now uses the dedicated `.onBroadcast()` method, rather than the
generic `.on()` method. Because the method is specific to broadcast, it takes
fewer properties.

BeforeAfter

`  

_10

supabase.channel('my_channel').on(

_10

RealtimeListenTypes.broadcast,

_10

ChannelFilter(

_10

event: 'position',

_10

),

_10

(dynamic payload, [ref]) {

_10

print(payload);

_10

},

_10

).subscribe();

  
`

#### Presence#

Realtime Presence gets three different methods for listening to three
different presence events: `sync`, `join`, and `leave`. This allows the
callback to be strictly typed.

BeforeAfter

`  

_27

final channel = supabase.channel('room1');

_27

_27

channel.on(

_27

RealtimeListenTypes.presence,

_27

ChannelFilter(event: 'sync'),

_27

(payload, [ref]) {

_27

print('Synced presence state: ${channel.presenceState()}');

_27

},

_27

).on(

_27

RealtimeListenTypes.presence,

_27

ChannelFilter(event: 'join'),

_27

(payload, [ref]) {

_27

print('Newly joined presences $payload');

_27

},

_27

).on(

_27

RealtimeListenTypes.presence,

_27

ChannelFilter(event: 'leave'),

_27

(payload, [ref]) {

_27

print('Newly left presences: $payload');

_27

},

_27

).subscribe(

_27

(status, [error]) async {

_27

if (status == 'SUBSCRIBED') {

_27

await channel.track({'online_at': DateTime.now().toIso8601String()});

_27

}

_27

},

_27

);

  
`

* * *

## Fetch data

Perform a SELECT query on the table or view.

  * By default, Supabase projects will return a maximum of 1,000 rows. This setting can be changed in Project API Settings. It's recommended that you keep it low to limit the payload size of accidental or malicious requests. You can use `range()` queries to paginate through your data.
  * `select()` can be combined with [Filters](/docs/reference/dart/using-filters)
  * `select()` can be combined with [Modifiers](/docs/reference/dart/using-modifiers)
  * `apikey` is a reserved keyword if you're using the [Supabase Platform](/docs/guides/platform) and [should be avoided as a column name](https://github.com/supabase/supabase/issues/5465).

### Parameters

  * columnsOptionalString

The columns to retrieve, separated by commas. Columns can be renamed when
returned with `customName:columnName`

Getting your dataSelecting specific columnsQuery referenced tablesQuery
referenced tables through a join tableQuery the same referenced table multiple
timesFiltering through referenced tablesQuerying with count optionQuerying
JSON dataQuerying referenced table with inner joinSwitching schemas per query

`  

_10

final data = await supabase

_10

.from('countries')

_10

.select();

  
`

Data source

Response

* * *

## Insert data

Perform an INSERT into the table or view.

### Parameters

  * valuesRequiredMap<String, dynamic> or List<Map<String, dynamic>>

The values to insert. Pass an object to insert a single row or an array to
insert multiple rows.

Create a recordFetch inserted recordBulk create

`  

_10

await supabase

_10

.from('cities')

_10

.insert({'name': 'The Shire', 'country_id': 554});

  
`

Data source

* * *

## Update data

Perform an UPDATE on the table or view.

  * `update()` should always be combined with [Filters](/docs/reference/dart/using-filters) to target the item(s) you wish to update.

### Parameters

  * valuesRequiredMap<String, dynamic>

The values to update with.

Update your dataUpdate a record and return itUpdate JSON data

`  

_10

await supabase

_10

.from('countries')

_10

.update({ 'name': 'Australia' })

_10

.eq('id', 1);

  
`

Data source

* * *

## Upsert data

Perform an UPSERT on the table or view. Depending on the column(s) passed to
`onConflict`, `.upsert()` allows you to perform the equivalent of `.insert()`
if a row with the corresponding `onConflict` columns doesn't exist, or if it
does exist, perform an alternative action depending on `ignoreDuplicates`.

  * Primary keys must be included in `values` to use upsert.

### Parameters

  * valuesRequiredMap<String, dynamic> or List<Map<String, dynamic>>

The values to upsert with. Pass a Map to upsert a single row or an List to
upsert multiple rows.

  * onConflictOptionalString

Comma-separated UNIQUE column(s) to specify how duplicate rows are determined.
Two rows are duplicates if all the `onConflict` columns are equal.

  * ignoreDuplicatesOptionalbool

If `true`, duplicate rows are ignored. If `false`, duplicate rows are merged
with existing rows.

  * defaultToNullOptionalbool

Make missing fields default to `null`. Otherwise, use the default value for
the column. This only applies when inserting new rows, not when merging with
existing rows where ignoreDuplicates is set to false. This also only applies
when doing bulk upserts.

Upsert your dataBulk Upsert your dataUpserting into tables with constraints

`  

_10

final data = await supabase

_10

.from('countries')

_10

.upsert({ 'id': 1, 'name': 'Albania' })

_10

.select();

  
`

Data source

Response

* * *

## Delete data

Perform a DELETE on the table or view.

  * `delete()` should always be combined with [Filters](/docs/reference/dart/using-filters) to target the item(s) you wish to delete.
  * If you use `delete()` with filters and you have RLS enabled, only rows visible through `SELECT` policies are deleted. Note that by default no rows are visible, so you need at least one `SELECT`/`ALL` policy that makes the rows visible.

Delete recordsDelete multiple recordsFetch deleted records

`  

_10

await supabase

_10

.from('countries')

_10

.delete()

_10

.eq('id', 1);

  
`

Data source

* * *

## Call a Postgres function

Perform a function call.

You can call Postgres functions as Remote Procedure Calls, logic in your
database that you can execute from anywhere. Functions are useful when the
logic rarely changes—like for password resets and updates.

### Parameters

  * fnRequiredString

The function name to call.

  * paramsOptionalMap<String, dynamic>

The arguments to pass to the function call.

Call a Postgres function without argumentsCall a Postgres function with
argumentsBulk processingCall a Postgres function with filters

`  

_10

final data = await supabase

_10

.rpc('hello_world');

  
`

Data source

Response

* * *

## Using filters

Filters allow you to only return rows that match certain conditions.

Filters can be used on `select()`, `update()`, `upsert()`, and `delete()`
queries.

If a Database function returns a table response, you can also apply filters.

Applying FiltersChaining FiltersConditional ChainingFilter by values within a
JSON columnFilter Referenced Tables

`  

_10

final data = await supabase

_10

.from('cities')

_10

.select('name, country_id')

_10

.eq('name', 'The Shire'); // Correct

_10

_10

final data = await supabase

_10

.from('cities')

_10

.eq('name', 'The Shire') // Incorrect

_10

.select('name, country_id');

  
`

Notes

* * *

## Column is equal to a value

Match only rows where `column` is equal to `value`.

### Parameters

  * columnRequiredString

The column to filter on.

  * valueRequiredObject

The value to filter with.

With `select()`

`  

_10

final data = await supabase

_10

.from('countries')

_10

.select()

_10

.eq('name', 'Albania');

  
`

Data source

Response

* * *

## Column is not equal to a value

Finds all rows whose value on the stated `column` doesn't match the specified
`value`.

### Parameters

  * columnRequiredString

The column to filter on.

  * valueRequiredObject

The value to filter with.

With `select()`

`  

_10

final data = await supabase

_10

.from('countries')

_10

.select('name, country_id')

_10

.neq('name', 'Albania');

  
`

Data source

Response

* * *

## Column is greater than a value

Finds all rows whose value on the stated `column` is greater than the
specified `value`.

### Parameters

  * columnRequiredString

The column to filter on.

  * valueRequiredObject

The value to filter with.

With `select()`

`  

_10

final data = await supabase

_10

.from('countries')

_10

.select()

_10

.gt('id', 2);

  
`

Data source

Response

* * *

## Column is greater than or equal to a value

Finds all rows whose value on the stated `column` is greater than or equal to
the specified `value`.

### Parameters

  * columnRequiredString

The column to filter on.

  * valueRequiredObject

The value to filter with.

With `select()`

`  

_10

final data = await supabase

_10

.from('countries')

_10

.select()

_10

.gte('id', 2);

  
`

Data source

Response

* * *

## Column is less than a value

Finds all rows whose value on the stated `column` is less than the specified
`value`.

### Parameters

  * columnRequiredString

The column to filter on.

  * valueRequiredObject

The value to filter with.

With `select()`

`  

_10

final data = await supabase

_10

.from('countries')

_10

.select()

_10

.lt('id', 2);

  
`

Data source

Response

* * *

## Column is less than or equal to a value

Finds all rows whose value on the stated `column` is less than or equal to the
specified `value`.

### Parameters

  * columnRequiredString

The column to filter on.

  * valueRequiredObject

The value to filter with.

With `select()`

`  

_10

final data = await supabase

_10

.from('countries')

_10

.select()

_10

.lte('id', 2);

  
`

Data source

Response

* * *

## Column matches a pattern

Finds all rows whose value in the stated `column` matches the supplied
`pattern` (case sensitive).

### Parameters

  * columnRequiredString

The column to filter on.

  * patternRequiredString

The pattern to match with.

With `select()`

`  

_10

final data = await supabase

_10

.from('countries')

_10

.select()

_10

.like('name', '%Alba%');

  
`

Data source

Response

* * *

## Column matches a case-insensitive pattern

Finds all rows whose value in the stated `column` matches the supplied
`pattern` (case insensitive).

### Parameters

  * columnRequiredString

The column to filter on.

  * patternRequiredString

The pattern to match with.

With `select()`

`  

_10

final data = await supabase

_10

.from('countries')

_10

.select()

_10

.ilike('name', '%alba%');

  
`

Data source

Response

* * *

## Column is a value

A check for exact equality (null, true, false), finds all rows whose value on
the stated `column` exactly match the specified `value`.

### Parameters

  * columnRequiredString

The column to filter on.

  * valueRequiredObject?

The value to filter with.

Checking for nullness, true or false

`  

_10

final data = await supabase

_10

.from('countries')

_10

.select()

_10

.isFilter('name', null);

  
`

Data source

Response

Notes

* * *

## Column is in an array

Finds all rows whose value on the stated `column` is found on the specified
`values`.

### Parameters

  * columnRequiredString

The column to filter on.

  * valuesRequiredList

The List to filter with.

With `select()`

`  

_10

final data = await supabase

_10

.from('countries')

_10

.select()

_10

.inFilter('name', ['Albania', 'Algeria']);

  
`

Data source

Response

Notes

* * *

## Column contains every element in a value

Only relevant for jsonb, array, and range columns. Match only rows where
`column` contains every element appearing in `value`.

### Parameters

  * columnRequiredString

The jsonb, array, or range column to filter on.

  * valueRequiredObject

The jsonb, array, or range value to filter with.

On array columnsOn range columnsOn `jsonb` columns

`  

_10

final data = await supabase

_10

.from('issues')

_10

.select()

_10

.contains('tags', ['is:open', 'priority:low']);

  
`

Data source

Response

Notes

* * *

## Contained by value

Only relevant for jsonb, array, and range columns. Match only rows where every
element appearing in `column` is contained by `value`.

### Parameters

  * columnRequiredString

The jsonb, array, or range column to filter on.

  * valueRequiredObject

The jsonb, array, or range value to filter with.

On array columnsOn range columnsOn `jsonb` columns

`  

_10

final data = await supabase

_10

.from('classes')

_10

.select('name')

_10

.containedBy('days', ['monday', 'tuesday', 'wednesday', 'friday']);

  
`

Data source

Response

* * *

## Greater than a range

Only relevant for range columns. Match only rows where every element in
`column` is greater than any element in `range`.

### Parameters

  * columnRequiredString

The range column to filter on.

  * rangeRequiredString

The range to filter with.

With `select()`

`  

_10

final data = await supabase

_10

.from('reservations')

_10

.select()

_10

.rangeGt('during', '[2000-01-02 08:00, 2000-01-02 09:00)');

  
`

Data source

Response

Notes

* * *

## Greater than or equal to a range

Only relevant for range columns. Match only rows where every element in
`column` is either contained in `range` or greater than any element in
`range`.

### Parameters

  * columnRequiredString

The range column to filter on.

  * rangeRequiredString

The range to filter with.

With `select()`

`  

_10

final data = await supabase

_10

.from('reservations')

_10

.select()

_10

.rangeGte('during', '[2000-01-02 08:30, 2000-01-02 09:30)');

  
`

Data source

Response

Notes

* * *

## Less than a range

Only relevant for range columns. Match only rows where every element in
`column` is less than any element in `range`.

### Parameters

  * columnRequiredString

The range column to filter on.

  * rangeRequiredString

The range to filter with.

With `select()`

`  

_10

final data = await supabase

_10

.from('reservations')

_10

.select()

_10

.rangeLt('during', '[2000-01-01 15:00, 2000-01-01 16:00)');

  
`

Data source

Response

Notes

* * *

## Less than or equal to a range

Only relevant for range columns. Match only rows where every element in
`column` is either contained in `range` or less than any element in `range`.

### Parameters

  * columnRequiredString

The range column to filter on.

  * rangeRequiredString

The range to filter with.

With `select()`

`  

_10

final data = await supabase

_10

.from('reservations')

_10

.select()

_10

.rangeLte('during', '[2000-01-01 15:00, 2000-01-01 16:00)');

  
`

Data source

Response

Notes

* * *

## Mutually exclusive to a range

Only relevant for range columns. Match only rows where `column` is mutually
exclusive to `range` and there can be no element between the two ranges.

### Parameters

  * columnRequiredString

The range column to filter on.

  * rangeRequiredString

The range to filter with.

With `select()`

`  

_10

final data = await supabase

_10

.from('reservations')

_10

.select()

_10

.rangeAdjacent('during', '[2000-01-01 12:00, 2000-01-01 13:00)');

  
`

Data source

Response

Notes

* * *

## With a common element

Only relevant for array and range columns. Match only rows where `column` and
`value` have an element in common.

### Parameters

  * columnRequiredString

The array or range column to filter on.

  * valueRequiredObject

The array or range value to filter with.

On array columnsOn range columns

`  

_10

final data = await supabase

_10

.from('issues')

_10

.select('title')

_10

.overlaps('tags', ['is:closed', 'severity:high']);

  
`

Data source

Response

* * *

## Match a string

Finds all rows whose tsvector value on the stated `column` matches
to_tsquery(query).

### Parameters

  * columnRequiredString

The text or tsvector column to filter on.

  * queryRequiredString

The query text to match with.

  * configOptionalString

The text search configuration to use.

  * typeOptionalTextSearchType

Change how the `query` text is interpreted.

Text searchBasic normalizationFull normalizationWebsearch

`  

_10

final data = await supabase

_10

.from('quotes')

_10

.select('catchphrase')

_10

.textSearch('content', "'eggs' & 'ham'",

_10

config: 'english'

_10

);

  
`

Data source

Response

* * *

## Match an associated value

Finds all rows whose columns match the specified `query` object.

### Parameters

  * queryRequiredMap<String, dynamic>

The object to filter with, with column names as keys mapped to their filter
values

With `select()`

`  

_10

final data = await supabase

_10

.from('countries')

_10

.select()

_10

.match({ 'id': 2, 'name': 'Albania' });

  
`

Data source

Response

* * *

## Don't match the filter

Finds all rows which doesn't satisfy the filter.

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

.not('id','in','(6,7)') // Use Postgres list () and 'in' instead of
`inFilter`.

_10

.not('id','in','(${mylist.join(',')})') // You can insert a Dart list array.

  
`

### Parameters

  * columnRequiredString

The column to filter on.

  * operatorRequiredString

The operator to be negated to filter with, following PostgREST syntax.

  * valueOptionalObject

The value to filter with, following PostgREST syntax.

With `select()`With `update()`With `delete()`With `rpc()`

`  

_10

final data = await supabase

_10

.from('countries')

_10

.select()

_10

.not('name', 'is', null)

  
`

Data source

Response

* * *

## Match at least one filter

Finds all rows satisfying at least one of the filters.

  * `.or()` expects you to use the raw [PostgREST syntax](https://postgrest.org/en/stable/api.html#horizontal-filtering-rows) for the filter names and values.

`  

_10

.or('id.in.(6,7),arraycol.cs.{"a","b"}') // Use Postgres list () and 'in'
instead of `inFilter`. Array {} and 'cs' for contains.

_10

.or('id.in.(${mylist.join(',')}),arraycol.cs.{${mylistArray.join(',')}}') //
You can insert a Dart list for list or array column.

_10

.or('id.in.(${mylist.join(',')}),rangecol.cs.(${mylistRange.join(',')}]') //
You can insert a Dart list for list or range column.

  
`

### Parameters

  * filtersRequiredString

The filters to use, following PostgREST syntax

  * referencedTableOptionalString

Set this to filter on referenced tables instead of the parent table

With `select()`Use `or` with `and`Use `or` on referenced tables

`  

_10

final data = await supabase

_10

.from('countries')

_10

.select('name')

_10

.or('id.eq.2,name.eq.Algeria');

  
`

Data source

Response

* * *

## Match the filter

Match only rows which satisfy the filter. This is an escape hatch - you should
use the specific filter methods wherever possible.

`.filter()` expects you to use the raw [PostgREST
syntax](https://postgrest.org/en/stable/api.html#horizontal-filtering-rows)
for the filter names and values, so it should only be used as an escape hatch
in case other filters don't work.

`  

_10

.filter('arraycol','cs','{"a","b"}') // Use Postgres array {} and 'cs' for
contains.

_10

.filter('rangecol','cs','(1,2]') // Use Postgres range syntax for range
column.

_10

.filter('id','in','(6,7)') // Use Postgres list () and 'in' for in_ filter.

_10

.filter('id','cs','{${mylist.join(',')}}') // You can insert a Dart array
list.

  
`

### Parameters

  * columnRequiredString

The column to filter on.

  * operatorRequiredString

The operator to filter with, following PostgREST syntax.

  * valueRequiredObject

The value to filter with, following PostgREST syntax.

With `select()`With `update()`With `delete()`With `rpc()`On a referenced table

`  

_10

final data = await supabase

_10

.from('countries')

_10

.select()

_10

.filter('name', 'in', '("Algeria","Japan")')

  
`

Data source

Response

* * *

## Using modifiers

Filters work on the row level. That is, they allow you to return rows that
only match certain conditions without changing the shape of the rows.
Modifiers are everything that don't fit that definition—allowing you to change
the format of the response (e.g., returning a CSV string).

Modifiers must be specified after filters. Some modifiers only apply for
queries that return rows (e.g., `select()` or `rpc()` on a function that
returns a table response).

* * *

## Return data after inserting

With `upsert()`

`  

_10

final data = await supabase

_10

.from('countries')

_10

.upsert({ 'id': 1, 'name': 'Algeria' })

_10

.select();

  
`

Data source

Response

* * *

## Order the results

Orders the result with the specified column.

### Parameters

  * columnRequiredString

The column to order by.

  * ascendingOptionalbool

Whether to order in ascending order. Default is `false`.

  * nullsFirstOptionalbool

Whether to order nulls first. Default is `false`.

  * referencedTableOptionalString

Specify the referenced table when ordering by a column in an embedded
resource.

With `select()`On a referenced table

`  

_10

final data = await supabase

_10

.from('countries')

_10

.select('id, name')

_10

.order('id', ascending: false);

  
`

Data source

Response

* * *

## Limit the number of rows returned

Limits the result with the specified count.

### Parameters

  * countRequiredint

The maximum number of rows to return.

  * referencedTableOptionalint

Set this to limit rows of referenced tables instead of the parent table.

With `select()`On a referenced table

`  

_10

final data = await supabase

_10

.from('cities')

_10

.select('name')

_10

.limit(1);

  
`

Data source

Response

* * *

## Limit the query to a range

Limits the result to rows within the specified range, inclusive.

### Parameters

  * fromRequiredint

The starting index from which to limit the result.

  * toRequiredint

The last index to which to limit the result.

  * referencedTableOptionalString

Set this to limit rows of referenced tables instead of the parent table.

With `select()`

`  

_10

final data = await supabase

_10

.from('countries')

_10

.select('name')

_10

.range(0, 1);

  
`

Data source

Response

* * *

## Retrieve one row of data

Retrieves only one row from the result. Result must be one row (e.g. using
limit), otherwise this will result in an error.

With `select()`

`  

_10

final data = await supabase

_10

.from('countries')

_10

.select('name')

_10

.limit(1)

_10

.single();

  
`

Data source

Response

* * *

## Retrieve zero or one row of data

With `select()`

`  

_10

final data = await supabase

_10

.from('countries')

_10

.select()

_10

.eq('name', 'Singapore')

_10

.maybeSingle();

  
`

Data source

Response

* * *

## Retrieve as a CSV

Return data as CSV

`  

_10

final data = await supabase

_10

.from('countries')

_10

.select()

_10

.csv();

  
`

Data source

Response

Notes

* * *

## Using explain

For debugging slow queries, you can get the [Postgres `EXPLAIN` execution
plan](https://www.postgresql.org/docs/current/sql-explain.html) of a query
using the `explain()` method. This works on any query, even for `rpc()` or
writes.

Explain is not enabled by default as it can reveal sensitive information about
your database. It's best to only enable this for testing environments but if
you wish to enable it for production you can provide additional protection by
using a `pre-request` function.

Follow the [Performance Debugging Guide](/docs/guides/database/debugging-
performance) to enable the functionality on your project.

### Parameters

  * analyzeOptionalbool

If `true`, the query will be executed and the actual run time will be
returned.

  * verboseOptionalbool

If `true`, the query identifier will be returned and `data` will include the
output columns of the query.

  * settingsOptionalbool

If `true`, include information on configuration parameters that affect query
planning.

  * buffersOptionalbool

If `true`, include information on buffer usage.

  * walOptionalbool

If `true`, include information on WAL record generation.

Get the execution planGet the execution plan with analyze and verbose

`  

_10

final data = await supabase

_10

.from('countries')

_10

.select()

_10

.explain();

  
`

Data source

Response

Notes

* * *

## Create a new user

Creates a new user.

  * By default, the user needs to verify their email address before logging in. To turn this off, disable **Confirm email** in [your project](https://supabase.com/dashboard/project/_/auth/providers).
  * **Confirm email** determines if users need to confirm their email address after signing up.
    * If **Confirm email** is enabled, a `user` is returned but `session` is null.
    * If **Confirm email** is disabled, both a `user` and a `session` are returned.
  * When the user confirms their email address, they are redirected to the [`SITE_URL`](https://supabase.com/docs/guides/auth/redirect-urls) by default. You can modify your `SITE_URL` or add additional redirect URLs in [your project](https://supabase.com/dashboard/project/_/auth/url-configuration).
  * If signUp() is called for an existing confirmed user:
    * When both **Confirm email** and **Confirm phone** (even when phone provider is disabled) are enabled in [your project](/dashboard/project/_/auth/providers), an obfuscated/fake user object is returned.
    * When either **Confirm email** or **Confirm phone** (even when phone provider is disabled) is disabled, the error message, `User already registered` is returned.

### Parameters

  * emailOptionalString

User's email address to be used for email authentication.

  * phoneOptionalString

User's phone number to be used for phone authentication.

  * passwordRequiredString

Password to be used for authentication.

  * emailRedirectToOptionalString

The URL to redirect the user to after they confirm their email address.

  * dataOptionalMap<String, dynamic>

The user's metadata to be stored in the user's object.

  * captchaTokenOptionalString

The captcha token to be used for captcha verification.

  * channelOptionalOtpChannel

Messaging channel to use (e.g. whatsapp or sms). Defaults to `OtpChannel.sms`.

Sign up with an email and passwordSign up with a phone number and password
(SMS)Sign up with additional metadataSign up with redirect URL

`  

_10

final AuthResponse res = await supabase.auth.signUp(

_10

email: '[[email protected]](/cdn-cgi/l/email-protection)',

_10

password: 'example-password',

_10

);

_10

final Session? session = res.session;

_10

final User? user = res.user;

  
`

Response

* * *

## Listen to auth events

Receive a notification every time an auth event happens.

  * Types of auth events: `AuthChangeEvent.passwordRecovery`, `AuthChangeEvent.signedIn`, `AuthChangeEvent.signedOut`, `AuthChangeEvent.tokenRefreshed`, `AuthChangeEvent.userUpdated`and `AuthChangeEvent.userDeleted`

Listen to auth changesListen to a specific eventUnsubscribe from auth
subscription

`  

_25

final authSubscription = supabase.auth.onAuthStateChange.listen((data) {

_25

final AuthChangeEvent event = data.event;

_25

final Session? session = data.session;

_25

_25

print('event: $event, session: $session');

_25

_25

switch (event) {

_25

case AuthChangeEvent.initialSession:

_25

// handle initial session

_25

case AuthChangeEvent.signedIn:

_25

// handle signed in

_25

case AuthChangeEvent.signedOut:

_25

// handle signed out

_25

case AuthChangeEvent.passwordRecovery:

_25

// handle password recovery

_25

case AuthChangeEvent.tokenRefreshed:

_25

// handle token refreshed

_25

case AuthChangeEvent.userUpdated:

_25

// handle user updated

_25

case AuthChangeEvent.userDeleted:

_25

// handle user deleted

_25

case AuthChangeEvent.mfaChallengeVerified:

_25

// handle mfa challenge verified

_25

}

_25

});

  
`

* * *

## Create an anonymous user

Creates an anonymous user.

  * Returns an anonymous user
  * It is recommended to set up captcha for anonymous sign-ins to prevent abuse. You can pass in the captcha token in the `options` param.

### Parameters

  * dataOptionalMap<String, dynamic>

The user's metadata to be stored in the user's object.

  * captchaTokenOptionalString

The captcha token to be used for captcha verification.

Create an anonymous userCreate an anonymous user with custom user metadata

`  

_10

await supabase.auth.signInAnonymously();

  
`

Response

* * *

## Sign in a user

Log in an existing user using email or phone number with password.

  * Requires either an email and password or a phone number and password.

### Parameters

  * emailOptionalString

User's email address to be used for email authentication.

  * phoneOptionalString

User's phone number to be used for phone authentication.

  * passwordRequiredString

Password to be used for authentication.

  * captchaTokenOptionalString

The captcha token to be used for captcha verification.

Sign in with email and passwordSign in with phone and password

`  

_10

final AuthResponse res = await supabase.auth.signInWithPassword(

_10

email: '[[email protected]](/cdn-cgi/l/email-protection)',

_10

password: 'example-password',

_10

);

_10

final Session? session = res.session;

_10

final User? user = res.user;

  
`

Response

* * *

## Sign in with ID Token

Allows you to perform native Google and Apple sign in by combining it with
[google_sign_in](https://pub.dev/packages/google_sign_in) or
[sign_in_with_apple](https://pub.dev/packages/sign_in_with_apple) packages.

### Parameters

  * providerRequiredOAuthProvider

The provider to perform the sign in with. Currently, `OAuthProvider.google`
and `OAuthProvider.apple` are supported.

  * idTokenRequiredString

The identity token obtained from the third-party provider.

  * accessTokenOptionalString

Access token obtained from the third-party provider. Required for Google sign
in.

  * nonceOptionalString

Raw nonce value used to perform the third-party sign in. Required for Apple
sign-in.

  * captchaTokenOptionalString

The captcha token to be used for captcha verification.

Native Google sign inNative Apple Sign in

`  

_28

import 'package:google_sign_in/google_sign_in.dart';

_28

import 'package:supabase_flutter/supabase_flutter.dart';

_28

_28

const webClientId = '<web client ID that you registered on Google Cloud, for
example my-web.apps.googleusercontent.com>';

_28

_28

const iosClientId = '<iOS client ID that you registered on Google Cloud, for
example my-ios.apps.googleusercontent.com';

_28

_28

final GoogleSignIn googleSignIn = GoogleSignIn(

_28

clientId: iosClientId,

_28

serverClientId: webClientId,

_28

);

_28

final googleUser = await googleSignIn.signIn();

_28

final googleAuth = await googleUser!.authentication;

_28

final accessToken = googleAuth.accessToken;

_28

final idToken = googleAuth.idToken;

_28

_28

if (accessToken == null) {

_28

throw 'No Access Token found.';

_28

}

_28

if (idToken == null) {

_28

throw 'No ID Token found.';

_28

}

_28

_28

final response = await supabase.auth.signInWithIdToken(

_28

provider: OAuthProvider.google,

_28

idToken: idToken,

_28

accessToken: accessToken,

_28

);

  
`

Response

Notes

* * *

## Sign in a user through OTP

  * Requires either an email or phone number.
  * This method is used for passwordless sign-ins where an OTP is sent to the user's email or phone number.
  * If you're using an email, you can configure whether you want the user to receive a magiclink or an OTP.
  * If you're using phone, you can configure whether you want the user to receive an OTP.
  * The magic link's destination URL is determined by the [`SITE_URL`](https://supabase.com/docs/guides/auth/redirect-urls). You can modify the `SITE_URL` or add additional redirect urls in [your project](https://supabase.com/dashboard/project/_/auth/url-configuration).

### Parameters

  * emailOptionalString

Email address to send the magic link or OTP to.

  * phoneOptionalString

Phone number to send the OTP to.

  * emailRedirectToOptionalString

The URL to redirect the user to after they click on the magic link.

  * shouldCreateUserOptionalbool

If set to false, this method will not create a new user. Defaults to true.

  * dataOptionalMap<String, dynamic>

The user's metadata to be stored in the user's object.

  * captchaTokenOptionalString

The captcha token to be used for captcha verification.

  * channelOptionalOtpChannel

Messaging channel to use (e.g. whatsapp or sms). Defaults to `OtpChannel.sms`.

Sign in with email.Sign in with SMS OTP.Sign in with WhatsApp OTP

`  

_10

await supabase.auth.signInWithOtp(

_10

email: '[[email protected]](/cdn-cgi/l/email-protection)',

_10

emailRedirectTo: kIsWeb ? null : 'io.supabase.flutter://signin-callback/',

_10

);

  
`

Response

Notes

* * *

## Sign in a user through OAuth

Signs the user in using third-party OAuth providers.

  * This method is used for signing in using a third-party provider.
  * Supabase supports many different [third-party providers](https://supabase.com/docs/guides/auth#providers).

### Parameters

  * providerRequiredOAuthProvider

The OAuth provider to use for signing in.

  * redirectToOptionalString

The URL to redirect the user to after they sign in with the third-party
provider.

  * scopesOptionalString

A list of scopes to request from the third-party provider.

  * authScreenLaunchModeOptionalLaunchMode

The launch mode for the auth screen. Defaults to `LaunchMode.platformDefault`.

  * queryParamsOptionalMap<String, String>

Additional query parameters to be passed to the OAuth flow.

Sign in using a third-party providerWith `redirectTo`With scopes

`  

_10

await supabase.auth.signInWithOAuth(

_10

OAuthProvider.github,

_10

redirectTo: kIsWeb ? null : 'my.scheme://my-host', // Optionally set the
redirect link to bring back the user via deeplink.

_10

authScreenLaunchMode:

_10

kIsWeb ? LaunchMode.platformDefault : LaunchMode.externalApplication, //
Launch the auth screen in a new webview on mobile.

_10

);

  
`

* * *

## Sign in a user through SSO

  * Before you can call this method you need to [establish a connection](/docs/guides/auth/sso/auth-sso-saml#managing-saml-20-connections) to an identity provider. Use the [CLI commands](/docs/reference/cli/supabase-sso) to do this.
  * If you've associated an email domain to the identity provider, you can use the `domain` property to start a sign-in flow.
  * In case you need to use a different way to start the authentication flow with an identity provider, you can use the `providerId` property. For example:
    * Mapping specific user email addresses with an identity provider.
    * Using different hints to identify the correct identity provider, like a company-specific page, IP address or other tracking information.

### Parameters

  * providerIdOptionalString

The ID of the SSO provider to use for signing in.

  * domainOptionalString

The email domain to use for signing in.

  * redirectToOptionalString

The URL to redirect the user to after they sign in with the third-party
provider.

  * captchaTokenOptionalString

The captcha token to be used for captcha verification.

  * launchModeOptionalLaunchMode

The launch mode for the auth screen. Defaults to `LaunchMode.platformDefault`.

Sign in with email domainSign in with provider UUID

`  

_10

await supabase.auth.signInWithSSO(

_10

domain: 'company.com',

_10

);

  
`

* * *

## Sign out a user

Signs out the current user, if there is a logged in user.

  * In order to use the `signOut()` method, the user needs to be signed in first.

### Parameters

  * scopeOptionalSignOutScope

Whether to sign out from all devices or just the current device. Defaults to
`SignOutScope.local`.

Sign out

`  

_10

await supabase.auth.signOut();

  
`

* * *

## Verify and log in through OTP

  * The `verifyOtp` method takes in different verification types. If a phone number is used, the type can either be `sms` or `phone_change`. If an email address is used, the type can be one of the following: `signup`, `magiclink`, `recovery`, `invite` or `email_change`.
  * The verification type used should be determined based on the corresponding auth method called before `verifyOtp` to sign up or sign in a user.

### Parameters

  * tokenRequiredString

The token that user was sent to their email or mobile phone

  * typeRequiredOtpType

Type of the OTP to verify

  * emailOptionalString

Email address that the OTP was sent to

  * phoneOptionalString

Phone number that the OTP was sent to

  * redirectToOptionalString

URI to redirect the user to after the OTP is verified

  * captchaTokenOptionalString

The captcha token to be used for captcha verification

  * tokenHashOptionalString

Token used in an email link

Verify Signup One-Time Password (OTP)Verify SMS One-Time Password (OTP)

`  

_10

final AuthResponse res = await supabase.auth.verifyOTP(

_10

type: OtpType.signup,

_10

token: token,

_10

phone: '+13334445555',

_10

);

_10

final Session? session = res.session;

_10

final User? user = res.user;

  
`

Response

* * *

## Retrieve a session

Returns the session data, if there is an active session.

Get the session data

`  

_10

final Session? session = supabase.auth.currentSession;

  
`

Response

* * *

## Retrieve a new session

  * This method will refresh and return a new session whether the current one is expired or not.

Refresh session using the current session

`  

_10

final AuthResponse res = await supabase.auth.refreshSession();

_10

final session = res.session;

  
`

Response

* * *

## Retrieve a user

Returns the user data, if there is a logged in user.

Get the logged in user

`  

_10

final User? user = supabase.auth.currentUser;

  
`

Response

* * *

## Update a user

Updates user data for a logged in user.

  * In order to use the `updateUser()` method, the user needs to be signed in first.
  * By default, email updates sends a confirmation link to both the user's current and new email. To only send a confirmation link to the user's new email, disable **Secure email change** in your project's [email auth provider settings](https://supabase.com/dashboard/project/_/auth/providers).

### Parameters

  * attributesRequiredUserAttributes

Attributes to update for the user.

Details

  * emailRedirectToOptionalString

The URI to redirect the user to after the email is updated.

Update the email for an authenticated userUpdate the password for an
authenticated userUpdate the user's metadataUpdate the user's password with a
nonce

`  

_10

final UserResponse res = await supabase.auth.updateUser(

_10

UserAttributes(

_10

email: '[[email protected]](/cdn-cgi/l/email-protection)',

_10

),

_10

);

_10

final User? updatedUser = res.user;

  
`

Response

Notes

* * *

## Retrieve identities linked to a user

Gets all the identities linked to a user.

  * The user needs to be signed in to call `getUserIdentities()`.

Returns a list of identities linked to the user

`  

_10

final identities = await supabase.auth.getUserIdentities();

  
`

Response

* * *

## Link an identity to a user

Links an oauth identity to an existing user. This method supports the PKCE
flow.

  * The **Enable Manual Linking** option must be enabled from your [project's authentication settings](/dashboard/project/_/settings/auth).
  * The user needs to be signed in to call `linkIdentity()`.
  * If the candidate identity is already linked to the existing user or another user, `linkIdentity()` will fail.

### Parameters

  * providerRequiredOAuthProvider

The provider to link the identity to.

  * redirectToOptionalString

The URL to redirect the user to after they sign in with the third-party
provider.

  * scopesOptionalString

A list of scopes to request from the third-party provider.

  * authScreenLaunchModeOptionalLaunchMode

The launch mode for the auth screen. Defaults to `LaunchMode.platformDefault`.

  * queryParamsOptionalMap<String, String>

Additional query parameters to be passed to the OAuth flow.

Link an identity to a user

`  

_10

await supabase.auth.linkIdentity(OAuthProvider.google);

  
`

* * *

## Unlink an identity from a user

Unlinks an identity from a user by deleting it. The user will no longer be
able to sign in with that identity once it's unlinked.

  * The **Enable Manual Linking** option must be enabled from your [project's authentication settings](/dashboard/project/_/settings/auth).
  * The user needs to be signed in to call `unlinkIdentity()`.
  * The user must have at least 2 identities in order to unlink an identity.
  * The identity to be unlinked must belong to the user.

### Parameters

  * identityRequiredUserIdentity

The user identity to unlink.

Unlink an identity

`  

_10

// retrieve all identites linked to a user

_10

final identities = await supabase.auth.getUserIdentities();

_10

_10

// find the google identity

_10

final googleIdentity = identities.firstWhere(

_10

(element) => element.provider == 'google',

_10

);

_10

_10

// unlink the google identity

_10

await supabase.auth.unlinkIdentity(googleIdentity);

  
`

* * *

## Send a password reauthentication nonce

  * This method is used together with `updateUser()` when a user's password needs to be updated.
  * This method sends a nonce to the user's email. If the user doesn't have a confirmed email address, the method sends the nonce to the user's confirmed phone number instead.

Send reauthentication nonce

`  

_10

await supabase.auth.reauthenticate();

  
`

Notes

* * *

## Resend an OTP

  * Resends a signup confirmation, email change, or phone change email to the user.
  * Passwordless sign-ins can be resent by calling the `signInWithOtp()` method again.
  * Password recovery emails can be resent by calling the `resetPasswordForEmail()` method again.
  * This method only resend an email or phone OTP to the user if an initial signup, email change, or phone change request was made.

Resend an email signup confirmation

`  

_10

final ResendResponse res = await supabase.auth.resend(

_10

type: OtpType.signup,

_10

email: '[[email protected]](/cdn-cgi/l/email-protection)',

_10

);

  
`

Notes

* * *

## Set the session data

  * `setSession()` takes in a refresh token and uses it to get a new session.
  * The refresh token can only be used once to obtain a new session.
  * [Refresh token rotation](/docs/guides/cli/config#auth.enable_refresh_token_rotation) is enabled by default on all projects to guard against replay attacks.
  * You can configure the [`REFRESH_TOKEN_REUSE_INTERVAL`](/docs/guides/cli/config#auth.refresh_token_reuse_interval) which provides a short window in which the same refresh token can be used multiple times in the event of concurrency or offline issues.

### Parameters

  * refreshTokenRequiredString

Refresh token to use to get a new session.

Refresh the session

`  

_10

final refreshToken = supabase.currentSession?.refreshToken ?? '';

_10

final AuthResponse response = await supabase.auth.setSession(refreshToken);

_10

_10

final session = res.session;

  
`

Response

Notes

* * *

## Auth MFA

This section contains methods commonly used for Multi-Factor Authentication
(MFA) and are invoked behind the `supabase.auth.mfa` namespace.

Currently, we only support time-based one-time password (TOTP) as the 2nd
factor. We don't support recovery codes but we allow users to enroll more than
1 TOTP factor, with an upper limit of 10.

Having a 2nd TOTP factor for recovery means the user doesn't have to store
their recovery codes. It also reduces the attack surface since the recovery
factor is usually time-limited and not a single static code.

Learn more about implementing MFA on your application on our guide
[here](https://supabase.com/docs/guides/auth/auth-mfa#overview).

* * *

## Enroll a factor

Starts the enrollment process for a new Multi-Factor Authentication (MFA)
factor. This method creates a new `unverified` factor. To verify a factor,
present the QR code or secret to the user and ask them to add it to their
authenticator app. The user has to enter the code from their authenticator app
to verify it.

  * Currently, `totp` is the only supported `factorType`. The returned `id` should be used to create a challenge.
  * To create a challenge, see [`mfa.challenge()`](/docs/reference/dart/auth-mfa-challenge).
  * To verify a challenge, see [`mfa.verify()`](/docs/reference/dart/auth-mfa-verify).
  * To create and verify a challenge in a single step, see [`mfa.challengeAndVerify()`](/docs/reference/dart/auth-mfa-challengeandverify).

### Parameters

  * factorTypeOptionalString

Type of factor being enrolled.

  * issuerOptionalString

Domain which the user is enrolled with.

  * friendlyNameOptionalString

Human readable name assigned to the factor.

Enroll a time-based, one-time password (TOTP) factor

`  

_10

final res = await supabase.auth.mfa.enroll(factorType: FactorType.totp);

_10

_10

final qrCodeUrl = res.totp.qrCode;

  
`

Response

* * *

## Create a challenge

Prepares a challenge used to verify that a user has access to a MFA factor.

  * An [enrolled factor](/docs/reference/dart/auth-mfa-enroll) is required before creating a challenge.
  * To verify a challenge, see [`mfa.verify()`](/docs/reference/dart/auth-mfa-verify).

### Parameters

  * factorIdRequiredString

System assigned identifier for authenticator device as returned by enroll

Create a challenge for a factor

`  

_10

final res = await supabase.auth.mfa.challenge(

_10

factorId: '34e770dd-9ff9-416c-87fa-43b31d7ef225',

_10

);

  
`

Response

* * *

## Verify a challenge

Verifies a code against a challenge. The verification code is provided by the
user by entering a code seen in their authenticator app.

  * To verify a challenge, please [create a challenge](/docs/reference/dart/auth-mfa-challenge) first.

### Parameters

  * factorIdRequiredString

System assigned identifier for authenticator device as returned by enroll

  * challengeIdRequiredString

The ID of the challenge to verify

  * codeRequiredString

The verification code on the user's authenticator app

Verify a challenge for a factor

`  

_10

final res = await supabase.auth.mfa.verify(

_10

factorId: '34e770dd-9ff9-416c-87fa-43b31d7ef225',

_10

challengeId: '4034ae6f-a8ce-4fb5-8ee5-69a5863a7c15',

_10

code: '123456',

_10

);

  
`

Response

* * *

## Create and verify a challenge

Helper method which creates a challenge and immediately uses the given code to
verify against it thereafter. The verification code is provided by the user by
entering a code seen in their authenticator app.

  * An [enrolled factor](/docs/reference/dart/auth-mfa-enroll) is required before invoking `challengeAndVerify()`.
  * Executes [`mfa.challenge()`](/docs/reference/dart/auth-mfa-challenge) and [`mfa.verify()`](/docs/reference/dart/auth-mfa-verify) in a single step.

### Parameters

  * factorIdRequiredString

System assigned identifier for authenticator device as returned by enroll

  * codeRequiredString

The verification code on the user's authenticator app

Create and verify a challenge for a factor

`  

_10

final res = await supabase.auth.mfa.challengeAndVerify(

_10

factorId: '34e770dd-9ff9-416c-87fa-43b31d7ef225',

_10

code: '123456',

_10

);

  
`

Response

* * *

## Unenroll a factor

Unenroll removes a MFA factor. A user has to have an `aal2` authenticator
level in order to unenroll a `verified` factor.

### Parameters

  * factorIdRequiredString

System assigned identifier for authenticator device as returned by enroll

Unenroll a factor

`  

_10

final res = await supabase.auth.mfa.unenroll(

_10

'34e770dd-9ff9-416c-87fa-43b31d7ef225',

_10

);

  
`

Response

* * *

## Get Authenticator Assurance Level

Returns the Authenticator Assurance Level (AAL) for the active session.

  * Authenticator Assurance Level (AAL) is the measure of the strength of an authentication mechanism.
  * In Supabase, having an AAL of `aal1` means the user has signed in with their first factor, such as email, password, or OAuth sign-in. An AAL of `aal2` means the user has also signed in with their second factor, such as a time-based, one-time-password (TOTP).
  * If the user has a verified factor, the `nextLevel` field returns `aal2`. Otherwise, it returns `aal1`.

Get the AAL details of a session

`  

_10

final res = supabase.auth.mfa.getAuthenticatorAssuranceLevel();

_10

final currentLevel = res.currentLevel;

_10

final nextLevel = res.nextLevel;

_10

final currentAuthenticationMethods = res.currentAuthenticationMethods;

  
`

Response

* * *

## Auth Admin

  * Any method under the `supabase.auth.admin` namespace requires a `service_role` key.
  * These methods are considered admin methods and should be called on a trusted server. Never expose your `service_role` key in the Flutter app.

Create server-side auth client

`  

_10

final supabase = SupabaseClient(supabaseUrl, serviceRoleKey);

  
`

* * *

## Retrieve a user

Get user by id.

  * Fetches the user object from the database based on the user's id.
  * The `getUserById()` method requires the user's id which maps to the `auth.users.id` column.

### Parameters

  * uidRequiredString

User ID of the user to fetch.

Fetch the user object using the access_token jwt

`  

_10

final res = await supabase.auth.admin.getUserById(userId);

_10

final user = res.user;

  
`

Response

* * *

## List all users

Get a list of users.

  * Defaults to return 50 users per page.

### Parameters

  * pageOptionalint

What page of users to return.

  * pageOptionalint

How many users to be returned per page. Defaults to 50.

Get a page of usersPaginated list of users

`  

_10

// Returns the first 50 users.

_10

final List<User> users = await supabase.auth.admin.listUsers();

  
`

Response

* * *

## Create a user

Creates a new user.

  * To confirm the user's email address or phone number, set `email_confirm` or `phone_confirm` to true. Both arguments default to false.
  * `createUser()` will not send a confirmation email to the user. You can use [`inviteUserByEmail()`](/docs/reference/dart/auth-admin-inviteuserbyemail) if you want to send them an email invite instead.
  * If you are sure that the created user's email or phone number is legitimate and verified, you can set the `email_confirm` or `phone_confirm` param to `true`.

### Parameters

  * attributesRequiredAdminUserAttributes

Attributes to create the user with.

Details

With custom user metadataAuto-confirm the user's emailAuto-confirm the user's
phone number

`  

_10

final res = await supabase.auth.admin.createUser(AdminUserAttributes(

_10

email: '[[email protected]](/cdn-cgi/l/email-protection)',

_10

password: 'password',

_10

userMetadata: {'name': 'Yoda'},

_10

));

  
`

Response

* * *

## Delete a user

Delete a user.

  * The `deleteUser()` method requires the user's ID, which maps to the `auth.users.id` column.

### Parameters

  * idRequiredString

ID of the user to be deleted.

Removes a user

`  

_10

await supabase.auth.admin

_10

.deleteUser('715ed5db-f090-4b8c-a067-640ecee36aa0');

  
`

* * *

## Send an email invite link

Sends an invite link to the user's email address.

### Parameters

  * emailRequiredString

Email address of the user to invite.

  * redirectToOptionalString

URI to redirect the user to after they open the invite link.

  * dataOptionalMap<String, dynamic>

A custom data object to store the user's metadata. This maps to the
`auth.users.user_metadata` column.

Invite a user

`  

_10

final UserResponse res = await supabase.auth.admin

_10

.inviteUserByEmail('[[email protected]](/cdn-cgi/l/email-protection)');

_10

final User? user = res.user;

  
`

Response

* * *

## Generate an email link

Generates email links and OTPs to be sent via a custom email provider.

  * The following types can be passed into `generateLink()`: `signup`, `magiclink`, `invite`, `recovery`, `emailChangeCurrent`, `emailChangeNew`, `phoneChange`.
  * `generateLink()` only generates the email link for `email_change_email` if the "Secure email change" setting is enabled under the "Email" provider in your Supabase project.
  * `generateLink()` handles the creation of the user for `signup`, `invite` and `magiclink`.

### Parameters

  * typeRequiredGenerateLinkType

The type of invite link to generate.

  * emailRequiredString

Email address of the user to invite.

  * passwordOptionalString

Password for the user. Required for `signup` type.

  * redirectToOptionalString

URI to redirect the user to after they open the invite link.

  * dataOptionalMap<String, dynamic>

A custom data object to store the user's metadata. This maps to the
`auth.users.user_metadata` column.

Generate a signup link

`  

_10

final res = await supabase.auth.admin.generateLink(

_10

type: GenerateLinkType.signup,

_10

email: '[[email protected]](/cdn-cgi/l/email-protection)',

_10

password: 'secret',

_10

);

_10

final actionLink = res.properties.actionLink;

  
`

Response

* * *

## Update a user

### Parameters

  * uidRequiredGenerateLinkType

User ID of the user to update.

  * attributesRequiredAdminUserAttributes

Attributes to update for the user.

Details

Updates a user's email

`  

_10

await supabase.auth.admin.updateUserById(

_10

'6aa5d0d4-2a9f-4483-b6c8-0cf4c6c98ac4',

_10

attributes: AdminUserAttributes(

_10

email: '[[email protected]](/cdn-cgi/l/email-protection)',

_10

),

_10

);

  
`

* * *

## Invokes a Supabase Edge Function.

Invokes a Supabase Function. See the [guide](/docs/guides/functions) for
details on writing Functions.

  * Requires an Authorization header.
  * Invoke params generally match the [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) spec.

### Parameters

  * functionNameRequiredString

The name of the function to invoke.

  * headersOptionalMap<String, String>

Custom headers to send with the request.

  * bodyOptionalMap<String, String>

The body of the request.

  * methodOptionalHttpMethod

HTTP method of the request. Defaults to POST.

Basic invocation.Specifying response type.Parsing custom headers.

`  

_10

final res = await supabase.functions.invoke('hello', body: {'foo': 'baa'});

_10

final data = res.data;

  
`

* * *

## Listen to database changes

Returns real-time data from your table as a `Stream`.

  * Realtime is disabled by default for new tables. You can turn it on by [managing replication](/docs/guides/realtime/postgres-changes#replication-setup).
  * `stream()` will emit the initial data as well as any further change on the database as `Stream<List<Map<String, dynamic>>>` by combining Postgrest and Realtime.
  * Takes a list of primary key column names that will be used to update and delete the proper records within the SDK.
  * The following filters are available
    * `.eq('column', value)` listens to rows where the column equals the value
    * `.neq('column', value)` listens to rows where the column does not equal the value
    * `.gt('column', value)` listens to rows where the column is greater than the value
    * `.gte('column', value)` listens to rows where the column is greater than or equal to the value
    * `.lt('column', value)` listens to rows where the column is less than the value
    * `.lte('column', value)` listens to rows where the column is less than or equal to the value
    * `.inFilter('column', [val1, val2, val3])` listens to rows where the column is one of the values

Listen to a tableWith filter, order and limitWith an IN filterUsing `stream()`
with `StreamBuilder`

`  

_10

supabase.from('countries')

_10

.stream(primaryKey: ['id'])

_10

.listen((List<Map<String, dynamic>> data) {

_10

// Do something awesome with the data

_10

});

  
`

* * *

## Subscribe to channel

Subscribe to realtime changes in your database.

  * Realtime is disabled by default for new tables. You can turn it on by [managing replication](/docs/guides/realtime/postgres-changes#replication-setup).
  * If you want to receive the "previous" data for updates and deletes, you will need to set `REPLICA IDENTITY` to `FULL`, like this: `ALTER TABLE your_table REPLICA IDENTITY FULL;`

Listen to database changesListen to insertsListen to updatesListen to
deletesListen to multiple eventsListen to row level changesListen to broadcast
messagesListen to presence events

`  

_10

supabase

_10

.channel('public:countries')

_10

.onPostgresChanges(

_10

event: PostgresChangeEvent.all,

_10

schema: 'public',

_10

table: 'countries',

_10

callback: (payload) {

_10

print('Change received: ${payload.toString()}');

_10

})

_10

.subscribe();

  
`

* * *

## Unsubscribe from a channel

Unsubscribes and removes Realtime channel from Realtime client.

  * Removing a channel is a great way to maintain the performance of your project's Realtime service as well as your database if you're listening to Postgres changes. Supabase will automatically handle cleanup 30 seconds after a client is disconnected, but unused channels may cause degradation as more clients are simultaneously subscribed.

Remove a channel

`  

_10

final status = await supabase.removeChannel(channel);

  
`

* * *

## Unsubscribe from all channels

Unsubscribes and removes all Realtime channels from Realtime client.

  * Removing channels is a great way to maintain the performance of your project's Realtime service as well as your database if you're listening to Postgres changes. Supabase will automatically handle cleanup 30 seconds after a client is disconnected, but unused channels may cause degradation as more clients are simultaneously subscribed.

Remove all channels

`  

_10

final statuses = await supabase.removeAllChannels();

  
`

* * *

## Retrieve all channels

Returns all Realtime channels.

Get all channels

`  

_10

final channels = supabase.getChannels();

  
`

* * *

## Create a bucket

Creates a new Storage bucket

  * Policy permissions required:
    * `buckets` permissions: `insert`
    * `objects` permissions: none
  * Refer to the [Storage guide](https://supabase.com/docs/guides/storage/security/access-control) on how access control works

### Parameters

  * idRequiredString

A unique identifier for the bucket you are creating.

  * bucketOptionsOptionalBucketOptions

A parameter to optionally make the bucket public.

Details

Create bucket

`  

_10

final String bucketId = await supabase

_10

.storage

_10

.createBucket('avatars');

  
`

Response

* * *

## Retrieve a bucket

Retrieves the details of an existing Storage bucket.

  * Policy permissions required:
    * `buckets` permissions: `select`
    * `objects` permissions: none
  * Refer to the [Storage guide](https://supabase.com/docs/guides/storage/security/access-control) on how access control works

### Parameters

  * idRequiredString

The unique identifier of the bucket you would like to retrieve.

Get bucket

`  

_10

final Bucket bucket = await supabase

_10

.storage

_10

.getBucket('avatars');

  
`

Response

* * *

## List all buckets

Retrieves the details of all Storage buckets within an existing product.

  * Policy permissions required:
    * `buckets` permissions: `select`
    * `objects` permissions: none
  * Refer to the [Storage guide](https://supabase.com/docs/guides/storage/security/access-control) on how access control works

List buckets

`  

_10

final List<Bucket> buckets = await supabase

_10

.storage

_10

.listBuckets();

  
`

Response

* * *

## Update a bucket

Updates a new Storage bucket

  * Policy permissions required:
    * `buckets` permissions: `update`
    * `objects` permissions: none
  * Refer to the [Storage guide](https://supabase.com/docs/guides/storage/security/access-control) on how access control works

### Parameters

  * idRequiredString

A unique identifier for the bucket you are updating.

  * bucketOptionsRequiredBucketOptions

A parameter to optionally make the bucket public.

Details

Update bucket

`  

_10

final String res = await supabase

_10

.storage

_10

.updateBucket('avatars', const BucketOptions(public: false));

  
`

Response

* * *

## Delete a bucket

Deletes an existing bucket. A bucket can't be deleted with existing objects
inside it. You must first `empty()` the bucket.

  * Policy permissions required:
    * `buckets` permissions: `select` and `delete`
    * `objects` permissions: none
  * Refer to the [Storage guide](https://supabase.com/docs/guides/storage/security/access-control) on how access control works

### Parameters

  * idRequiredString

A unique identifier for the bucket you are deleting.

Delete bucket

`  

_10

final String res = await supabase

_10

.storage

_10

.deleteBucket('avatars');

  
`

Response

* * *

## Empty a bucket

Removes all objects inside a single bucket.

  * Policy permissions required:
    * `buckets` permissions: `select`
    * `objects` permissions: `select` and `delete`
  * Refer to the [Storage guide](https://supabase.com/docs/guides/storage/security/access-control) on how access control works

### Parameters

  * idRequiredString

A unique identifier for the bucket you are emptying.

Empty bucket

`  

_10

final String res = await supabase

_10

.storage

_10

.emptyBucket('avatars');

  
`

Response

* * *

## Upload a file

Uploads a file to an existing bucket.

  * Policy permissions required:
    * `buckets` permissions: none
    * `objects` permissions: `insert`
  * Refer to the [Storage guide](https://supabase.com/docs/guides/storage/security/access-control) on how access control works

### Parameters

  * pathRequiredString

The relative file path. Should be of the format folder/subfolder/filename.png.
The bucket must already exist before attempting to update.

  * fileRequiredFile or Uint8List

File object to be stored in the bucket.

  * fileOptionsOptionalFileOptions

Details

  * retryAttemptsOptionalint

Sets the retryAttempts parameter set across the storage client. Defaults to
10.

  * retryControllerOptionalStorageRetryController

Pass a RetryController instance and call `cancel()` to cancel the retry
attempts.

Upload fileUpload file on web

`  

_10

final avatarFile = File('path/to/file');

_10

final String fullPath = await supabase.storage.from('avatars').upload(

_10

'public/avatar1.png',

_10

avatarFile,

_10

fileOptions: const FileOptions(cacheControl: '3600', upsert: false),

_10

);

  
`

Response

* * *

## Download a file

Downloads a file.

  * Policy permissions required:
    * `buckets` permissions: none
    * `objects` permissions: `select`
  * Refer to the [Storage guide](https://supabase.com/docs/guides/storage/security/access-control) on how access control works

### Parameters

  * pathRequiredString

The full path and file name of the file to be downloaded. For example
folder/image.png.

  * transformOptionalTransformOptions

Transform the asset before serving it to the client.

Details

Download fileWith transform

`  

_10

final Uint8List file = await supabase

_10

.storage

_10

.from('avatars')

_10

.download('avatar1.png');

  
`

Response

* * *

## List all files in a bucket

Lists all the files within a bucket.

  * Policy permissions required:
    * `buckets` permissions: none
    * `objects` permissions: `select`
  * Refer to the [Storage guide](https://supabase.com/docs/guides/storage/security/access-control) on how access control works

### Parameters

  * pathRequiredString

The folder path.

  * searchOptionsOptionalSearchOptions

Options for the search operations such as limit and offset.

Details

List files in a bucket

`  

_10

final List<FileObject> objects = await supabase

_10

.storage

_10

.from('avatars')

_10

.list();

  
`

Response

* * *

## Replace an existing file

Replaces an existing file at the specified path with a new one.

  * Policy permissions required:
    * `buckets` permissions: none
    * `objects` permissions: `update` and `select`
  * Refer to the [Storage guide](https://supabase.com/docs/guides/storage/security/access-control) on how access control works

### Parameters

  * pathRequiredString

The relative file path. Should be of the format folder/subfolder/filename.png.
The bucket must already exist before attempting to update.

  * fileRequiredFile or Uint8List

File object to be stored in the bucket.

  * fileOptionsOptionalFileOptions

Details

  * retryAttemptsOptionalint

Sets the retryAttempts parameter set across the storage client. Defaults to
10.

  * retryControllerOptionalStorageRetryController

Pass a RetryController instance and call `cancel()` to cancel the retry
attempts.

Update fileUpdate file on web

`  

_10

final avatarFile = File('path/to/local/file');

_10

final String path = await supabase.storage.from('avatars').update(

_10

'public/avatar1.png',

_10

avatarFile,

_10

fileOptions: const FileOptions(cacheControl: '3600', upsert: false),

_10

);

  
`

Response

* * *

## Move an existing file

Moves an existing file, optionally renaming it at the same time.

  * Policy permissions required:
    * `buckets` permissions: none
    * `objects` permissions: `update` and `select`
  * Refer to the [Storage guide](https://supabase.com/docs/guides/storage/security/access-control) on how access control works

### Parameters

  * fromPathRequiredString

The original file path, including the current file name. For example
folder/image.png.

  * toPathRequiredString

The new file path, including the new file name. For example folder/image-
new.png.

Move file

`  

_10

final String result = await supabase

_10

.storage

_10

.from('avatars')

_10

.move('public/avatar1.png', 'private/avatar2.png');

  
`

Response

* * *

## Delete files in a bucket

Deletes files within the same bucket

  * Policy permissions required:
    * `buckets` permissions: none
    * `objects` permissions: `delete` and `select`
  * Refer to the [Storage guide](https://supabase.com/docs/guides/storage/security/access-control) on how access control works

### Parameters

  * pathsRequiredList<String>

A list of files to delete, including the path and file name. For example
['folder/image.png'].

Delete file

`  

_10

final List<FileObject> objects = await supabase

_10

.storage

_10

.from('avatars')

_10

.remove(['avatar1.png']);

  
`

Response

* * *

## Create a signed URL

Create signed url to download file without requiring permissions. This URL can
be valid for a set number of seconds.

  * Policy permissions required:
    * `buckets` permissions: none
    * `objects` permissions: `select`
  * Refer to the [Storage guide](https://supabase.com/docs/guides/storage/security/access-control) on how access control works

### Parameters

  * pathRequiredString

The file path, including the file name. For example folder/image.png.

  * expiresInRequiredint

The number of seconds until the signed URL expires. For example, 60 for a URL
which is valid for one minute.

  * transformOptionalTransformOptions

Transform the asset before serving it to the client.

Details

Create Signed URLWith transform

`  

_10

final String signedUrl = await supabase

_10

.storage

_10

.from('avatars')

_10

.createSignedUrl('avatar1.png', 60);

  
`

* * *

## Retrieve public URL

Retrieve URLs for assets in public buckets

  * The bucket needs to be set to public, either via [updateBucket()](/docs/reference/dart/storage-updatebucket) or by going to Storage on [supabase.com/dashboard](https://supabase.com/dashboard), clicking the overflow menu on a bucket and choosing "Make public"
  * Policy permissions required:
    * `buckets` permissions: none
    * `objects` permissions: none
  * Refer to the [Storage guide](https://supabase.com/docs/guides/storage/security/access-control) on how access control works

### Parameters

  * pathRequiredString

The path and name of the file to generate the public URL for. For example
folder/image.png.

  * transformOptionalTransformOptions

Transform the asset before serving it to the client.

Details

Returns the URL for an asset in a public bucketWith transform

`  

_10

final String publicUrl = supabase

_10

.storage

_10

.from('public-bucket')

_10

.getPublicUrl('avatar1.png');

  
`

Response

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

