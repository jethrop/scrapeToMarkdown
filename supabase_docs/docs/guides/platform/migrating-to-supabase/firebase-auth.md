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
  6.   7. [Firebase Auth](/docs/guides/platform/migrating-to-supabase/firebase-auth)
  8. 

# Migrate from Firebase Auth to Supabase

## Migrate Firebase auth users to Supabase Auth.

* * *

Supabase provides several [tools](https://github.com/supabase-
community/firebase-to-supabase/tree/main/auth) to help migrate auth users from
a Firebase project to a Supabase project. There are two parts to the migration
process:

  * `firestoreusers2json` ([TypeScript](https://github.com/supabase-community/firebase-to-supabase/blob/main/auth/firestoreusers2json.ts), [JavaScript](https://github.com/supabase-community/firebase-to-supabase/blob/main/auth/firestoreusers2json.js)) exports users from an existing Firebase project to a `.json` file on your local system.
  * `import_users` ([TypeScript](https://github.com/supabase-community/firebase-to-supabase/blob/main/auth/import_users.ts), [JavaScript](https://github.com/supabase-community/firebase-to-supabase/blob/main/auth/import_users.js)) imports users from a saved `.json` file into your Supabase project (inserting those users into the `auth.users` table of your `Postgres` database instance).

## Set up the migration tool #

  1. Clone the [firebase-to-supabase](https://github.com/supabase-community/firebase-to-supabase) repository:

`  

_10

git clone https://github.com/supabase-community/firebase-to-supabase.git

  
`

  2. In the `/auth` directory, create a file named `supabase-service.json` with the following contents:

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

## Save your Firebase password hash parameters #

  1. Log in to your [Firebase Console](https://console.firebase.google.com/project) and open your project.
  2. Select **Authentication** (Build section) in the sidebar.
  3. Select **Users** in the top menu.
  4. At the top right of the users list, open the menu (3 dots) and click **Password hash parameters**.
  5. Copy and save the parameters for `base64_signer_key`, `base64_salt_separator`, `rounds`, and `mem_cost`.

Sample

`  

_10

hash_config {

_10

algorithm: SCRYPT,

_10

base64_signer_key:
XXXX/XXX+XXXXXXXXXXXXXXXXX+XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX==,

_10

base64_salt_separator: Aa==,

_10

rounds: 8,

_10

mem_cost: 14,

_10

}

  
`

## Command line options#

### Dump Firestore users to a JSON file #

`node firestoreusers2json.js [<filename.json>] [<batch_size>]`

  * `filename.json`: (optional) output filename (defaults to `./users.json`)
  * `batchSize`: (optional) number of users to fetch in each batch (defaults to 100)

### Import JSON users file to Supabase Auth (Postgres: auth.users) #

`node import_users.js <path_to_json_file> [<batch_size>]`

  * `path_to_json_file`: full local path and filename of .json input file (of users)
  * `batch_size`: (optional) number of users to process in a batch (defaults to 100)

## Notes#

For more advanced migrations, including the use of a middleware server
component for verifying a user's existing Firebase password and updating that
password in your Supabase project the first time a user logs in, see the
[firebase-to-supabase repo](https://github.com/supabase-community/firebase-to-
supabase/tree/main/auth).

## Resources#

  * [Supabase vs Firebase](https://supabase.com/alternatives/supabase-vs-firebase)
  * [Firestore Data Migration](/docs/guides/migrations/firestore-data)
  * [Firestore Storage Migration](/docs/guides/migrations/firebase-storage)

## Enterprise#

[Contact us](https://forms.supabase.com/enterprise) if you need more help
migrating your project.

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/content/guides/platform/migrating-
to-supabase/firebase-auth.mdx)

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

