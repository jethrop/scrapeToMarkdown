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

Platform

  1. [Platform](/docs/guides/platform)
  2.   3. More
  4.   5. [Migrating to Supabase](/docs/guides/platform/migrating-to-supabase)
  6.   7. [Firebase Firestore](/docs/guides/platform/migrating-to-supabase/firestore-data)
  8. 

# Migrated from Firebase Firestore to Supabase

## Migrate your Firebase Firestore database to a Supabase Postgres database.

* * *

Supabase provides several [tools](https://github.com/supabase-
community/firebase-to-supabase/tree/main/firestore) to convert data from a
Firebase Firestore database to a Supabase PostgreSQL database. The process
copies the entire contents of a single Firestore `collection` to a single
PostgreSQL `table`.

The Firestore `collection` is "flattened" and converted to a table with basic
columns of one of the following types: `text`, `numeric`, `boolean`, or
`jsonb`. If your structure is more complex, you can write a program to split
the newly-created `json` file into multiple, related tables before you import
your `json` file(s) to Supabase.

## Set up the migration tool #

  1. Clone the [firebase-to-supabase](https://github.com/supabase-community/firebase-to-supabase) repository:

`  

_10

git clone https://github.com/supabase-community/firebase-to-supabase.git

  
`

  2. In the `/firestore` directory, create a file named `supabase-service.json` with the following contents:

`  

_10

{

_10

"host": "database.server.com",

_10

"password": "secretpassword",

_10

"user": "postgres",

_10

"database": "postgres",

_10

"port": 5432

_10

}

  
`

  3. Go to the [Database settings](https://supabase.com/dashboard/project/_/settings/database) for your project in the Supabase Dashboard.

  4. Under `Connection parameters`, enable `Use connection pooling` and set the mode to `Session`. Replace the `Host` and `User` fields with the values shown.

  5. Enter the password you used when you created your Supabase project in the `password` entry in the `supabase-service.json` file.

## Generate a Firebase private key #

  1. Log in to your [Firebase Console](https://console.firebase.google.com/project) and open your project.
  2. Click the gear icon next to **Project Overview** in the sidebar and select **Project Settings**.
  3. Click **Service Accounts** and select **Firebase Admin SDK**.
  4. Click **Generate new private key**.
  5. Rename the downloaded file to `firebase-service.json`.

## Command line options#

### List all Firestore collections#

`node collections.js`

### Dump Firestore collection to JSON file#

`node firestore2json.js <collectionName> [<batchSize>] [<limit>]`

  * `batchSize` (optional) defaults to 1000
  * output filename is `<collectionName>.json`
  * `limit` (optional) defaults to 0 (no limit)

#### Customize the JSON file with hooks#

You can customize the way your JSON file is written using a custom hook. A
common use for this is to "flatten" the JSON file, or to split nested data
into separate, related database tables. For example, you could take a
Firestore document that looks like this:

Firestore

`  

_10

[{ "user": "mark", "score": 100, "items": ["hammer", "nail", "glue"] }]

  
`

And split it into two files (one table for users and one table for items):

Users

`  

_10

[{ "user": "mark", "score": 100 }]

  
`

Items

`  

_10

[

_10

{ "user": "mark", "item": "hammer" },

_10

{ "user": "mark", "item": "nail" },

_10

{ "user": "mark", "item": "glue" }

_10

]

  
`

### Import JSON file to Supabase (PostgreSQL) #

`node json2supabase.js <path_to_json_file> [<primary_key_strategy>]
[<primary_key_name>]`

  * `<path_to_json_file>` The full path of the file you created in the previous step (`Dump Firestore collection to JSON file `), such as `./my_collection.json`
  * `[<primary_key_strategy>]` (optional) Is one of:
    * `none` (default) No primary key is added to the table.
    * `smallserial` Creates a key using `(id SMALLSERIAL PRIMARY KEY)` (autoincrementing 2-byte integer).
    * `serial` Creates a key using `(id SERIAL PRIMARY KEY)` (autoincrementing 4-byte integer).
    * `bigserial` Creates a key using `(id BIGSERIAL PRIMARY KEY)` (autoincrementing 8-byte integer).
    * `uuid` Creates a key using `(id UUID PRIMARY KEY DEFAULT gen_random_uuid())` (randomly generated UUID).
    * `firestore_id` Creates a key using `(id TEXT PRIMARY KEY)` (uses existing `firestore_id` random text as key).
  * `[<primary_key_name>]` (optional) Name of primary key. Defaults to "id".

## Custom hooks#

Hooks are used to customize the process of exporting a collection of Firestore
documents to JSON. They can be used for:

  * Customizing or modifying keys
  * Calculating data
  * Flattening nested documents into related SQL tables

### Write a custom hook#

#### Create a .js file for your collection#

If your Firestore collection is called `users`, create a file called
`users.js` in the current folder.

#### Construct your .js file#

The basic format of a hook file looks like this:

`  

_10

module.exports = (collectionName, doc, recordCounters, writeRecord) => {

_10

// modify the doc here

_10

return doc

_10

}

  
`

##### Parameters

  * `collectionName`: The name of the collection you are processing.
  * `doc`: The current document (JSON object) being processed.
  * `recordCounters`: An internal object that keeps track of how many records have been processed in each collection.
  * `writeRecord`: This function automatically handles the process of writing data to other JSON files (useful for "flatting" your document into separate JSON files to be written to separate database tables). `writeRecord` takes the following parameters:
    * `name`: Name of the JSON file to write to.
    * `doc`: The document to write to the file.
    * `recordCounters`: The same `recordCounters` object that was passed to this hook (just passes it on).

### Examples#

#### Add a new (unique) numeric key to a collection#

`  

_10

module.exports = (collectionName, doc, recordCounters, writeRecord) => {

_10

doc.unique_key = recordCounter[collectionName] + 1

_10

return doc

_10

}

  
`

#### Add a timestamp of when this record was dumped from Firestore#

`  

_10

module.exports = (collectionName, doc, recordCounters, writeRecord) => {

_10

doc.dump_time = new Date().toISOString()

_10

return doc

_10

}

  
`

#### Flatten JSON into separate files#

Flatten the `users` collection into separate files:

`  

_14

[

_14

{

_14

"uid": "abc123",

_14

"name": "mark",

_14

"score": 100,

_14

"weapons": ["toothpick", "needle", "rock"]

_14

},

_14

{

_14

"uid": "xyz789",

_14

"name": "chuck",

_14

"score": 9999999,

_14

"weapons": ["hand", "foot", "head"]

_14

}

_14

]

  
`

The `users.js` hook file:

`  

_11

module.exports = (collectionName, doc, recordCounters, writeRecord) => {

_11

for (let i = 0; i < doc.weapons.length; i++) {

_11

const weapon = {

_11

uid: doc.uid,

_11

weapon: doc.weapons[i],

_11

}

_11

writeRecord('weapons', weapon, recordCounters)

_11

}

_11

delete doc.weapons // moved to separate file

_11

return doc

_11

}

  
`

The result is two separate JSON files:

users.json

`  

_10

[

_10

{ "uid": "abc123", "name": "mark", "score": 100 },

_10

{ "uid": "xyz789", "name": "chuck", "score": 9999999 }

_10

]

  
`

weapons.json

`  

_10

[

_10

{ "uid": "abc123", "weapon": "toothpick" },

_10

{ "uid": "abc123", "weapon": "needle" },

_10

{ "uid": "abc123", "weapon": "rock" },

_10

{ "uid": "xyz789", "weapon": "hand" },

_10

{ "uid": "xyz789", "weapon": "foot" },

_10

{ "uid": "xyz789", "weapon": "head" }

_10

]

  
`

## Resources#

  * [Supabase vs Firebase](https://supabase.com/alternatives/supabase-vs-firebase)
  * [Firestore Storage Migration](/docs/guides/migrations/firebase-storage)
  * [Firebase Auth Migration](/docs/guides/migrations/firebase-auth)

## Enterprise#

[Contact us](https://forms.supabase.com/enterprise) if you need more help
migrating your project.

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/content/guides/platform/migrating-
to-supabase/firestore-data.mdx)

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

