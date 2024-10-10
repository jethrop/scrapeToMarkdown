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

Self-Hosting

  1. [Self-Hosting](/docs/guides/self-hosting)
  2.   3. Storage Server
  4.   5. [Configuration](/docs/guides/self-hosting/storage/config)
  6. 

# Storage Self-hosting Config

* * *

A sample `.env` file is located in the [storage
repository](https://github.com/supabase/storage-api/blob/master/.env.sample).

Use this file to configure your environment variables for your Storage server.

## General

General Settings

##### Parameters

ANON_KEY

REQUIRED

no type

A long-lived JWT with anonymous Postgres privileges.

SERVICE_KEY

REQUIRED

no type

A long-lived JWT with Postgres privileges to bypass Row Level Security.

TENANT_ID

REQUIRED

no type

The ID of a Storage tenant.

REGION

REQUIRED

no type

Region of your S3 bucket.

GLOBAL_S3_BUCKET

REQUIRED

no type

Name of your S3 bucket.

POSTGREST_URL

REQUIRED

no type

The URL of your PostgREST server.

PGRST_JWT_SECRET

REQUIRED

no type

A JWT Secret for the PostgREST database.

DATABASE_URL

REQUIRED

no type

The URL of your Postgres database.

PGOPTIONS

REQUIRED

no type

Additional configuration parameters for Postgres startup.

FILE_SIZE_LIMIT

REQUIRED

no type

The maximum file size allowed.

STORAGE_BACKEND

REQUIRED

no type

The storage provider.

FILE_STORAGE_BACKEND_PATH

REQUIRED

no type

The location storage when the "STORAGE_BACKEND" is set to "file".

## Multi-tenant

Configuration items for multi-tenant servers.

##### Parameters

IS_MULTITENANT

REQUIRED

no type

Operate across multiple tenants.

MULTITENANT_DATABASE_URL

REQUIRED

no type

The URL of the multitenant Postgres database.

X_FORWARDED_HOST_REGEXP

REQUIRED

no type

TBD.

POSTGREST_URL_SUFFIX

REQUIRED

no type

The suffix for the PostgREST instance.

ADMIN_API_KEYS

REQUIRED

no type

Secure API key for administrative endpoints.

ENCRYPTION_KEY

REQUIRED

no type

An key for encryting/decrypting secrets.

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/pages/guides/self-
hosting/storage/config.tsx)

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

