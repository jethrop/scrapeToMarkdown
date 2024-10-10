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
  6.   7. [Firebase Storage](/docs/guides/platform/migrating-to-supabase/firebase-storage)
  8. 

# Migrated from Firebase Storage to Supabase

## Migrate Firebase Storage files to Supabase Storage.

* * *

Supabase provides several [tools](https://github.com/supabase-
community/firebase-to-supabase/tree/main/storage) to convert storage files
from Firebase Storage to Supabase Storage. Conversion is a two-step process:

  1. Files are downloaded from a Firebase storage bucket to a local filesystem.
  2. Files are uploaded from the local filesystem to a Supabase storage bucket.

## Set up the migration tool #

  1. Clone the [firebase-to-supabase](https://github.com/supabase-community/firebase-to-supabase) repository:

`  

_10

git clone https://github.com/supabase-community/firebase-to-supabase.git

  
`

  2. In the `/storage` directory, rename [supabase-keys-sample.js](https://github.com/supabase-community/firebase-to-supabase/blob/main/storage/supabase-keys-sample.js) to `supabase-keys.js`.

  3. Go to your Supabase project's [API settings](https://supabase.com/dashboard/project/_/settings/api) in the Dashboard.

  4. Copy the **Project URL** and update the `SUPABASE_URL` value in `supabase-keys.js`.

  5. Under **Project API keys** , copy the **service_role** key and update the `SUPABASE_KEY` value in `supabase-keys.js`.

## Generate a Firebase private key #

  1. Log in to your [Firebase Console](https://console.firebase.google.com/project) and open your project.
  2. Click the gear icon next to **Project Overview** in the sidebar and select **Project Settings**.
  3. Click **Service Accounts** and select **Firebase Admin SDK**.
  4. Click **Generate new private key**.
  5. Rename the downloaded file to `firebase-service.json`.

## Command line options#

### Download Firestore Storage bucket to a local filesystem folder #

`node download.js <prefix> [<folder>] [<batchSize>] [<limit>] [<token>]`

  * `<prefix>`: The prefix of the files to download. To process the root bucket, use an empty prefix: "".
  * `<folder>`: (optional) Name of subfolder for downloaded files. The selected folder is created as a subfolder of the current folder (e.g., `./downloads/`). The default is `downloads`.
  * `<batchSize>`: (optional) The default is 100.
  * `<limit>`: (optional) Stop after processing this many files. For no limit, use `0`.
  * `<token>`: (optional) Begin processing at this pageToken.

To process in batches using multiple command-line executions, you must use the
same parameters with a new `<token>` on subsequent calls. Use the token
displayed on the last call to continue the process at a given point.

### Upload files to Supabase Storage bucket #

`node upload.js <prefix> <folder> <bucket>`

  * `<prefix>`: The prefix of the files to download. To process all files, use an empty prefix: "".
  * `<folder>`: Name of subfolder of files to upload. The selected folder is read as a subfolder of the current folder (e.g., `./downloads/`). The default is `downloads`.
  * `<bucket>`: Name of the bucket to upload to.

If the bucket doesn't exist, it's created as a `non-public` bucket. You must
set permissions on this new bucket in the [Supabase
Dashboard](https://supabase.com/dashboard/project/_/storage/buckets) before
users can download any files.

## Resources#

  * [Supabase vs Firebase](https://supabase.com/alternatives/supabase-vs-firebase)
  * [Firestore Data Migration](/docs/guides/migrations/firestore-data)
  * [Firebase Auth Migration](/docs/guides/migrations/firebase-auth)

## Enterprise#

[Contact us](https://forms.supabase.com/enterprise) if you need more help
migrating your project.

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/content/guides/platform/migrating-
to-supabase/firebase-storage.mdx)

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

