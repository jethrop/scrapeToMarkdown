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

Database

  1. [Database](/docs/guides/database/overview)
  2.   3. Fundamentals
  4.   5. [Importing data](/docs/guides/database/import-data)
  6. 

# Import data into Supabase

* * *

You can import data into Supabase in multiple ways. The best method depends on
your data size and app requirements.

If you're working with small datasets in development, you can experiment
quickly using CSV import in the Supabase dashboard. If you're working with a
large dataset in production, you should plan your data import to minimize app
latency and ensure data integrity.

## How to import data into Supabase#

You have multiple options for importing your data into Supabase:

  1. CSV import via the Supabase dashboard
  2. Bulk import using `pgloader`
  3. Using the Postgres `COPY` command
  4. Using the Supabase API

If you're importing a large dataset or importing data into production, plan
ahead and prepare your database.

### Option 1: CSV import via Supabase dashboard#

Supabase dashboard provides a user-friendly way to import data. However, for
very large datasets, this method may not be the most efficient choice, given
the size limit is 100MB. It's generally better suited for smaller datasets and
quick data imports. Consider using alternative methods like pgloader for
large-scale data imports.

  1. Navigate to the relevant table in the [Table Editor.](/dashboard/project/_/editor)
  2. Click on “Insert” then choose "Import Data from CSV" and follow the on-screen instructions to upload your CSV file.

### Option 2: Bulk import using pgloader#

[pgloader](https://pgloader.io/) is a powerful tool for efficiently importing
data into a PostgreSQL database that supports a wide range of source database
engines, including MySQL and MS SQL.

You can use it in conjunction with Supabase by following these steps:

  1. Install pgloader on your local machine or a server. For more info, you can refer to the [official pgloader installation page](https://pgloader.readthedocs.io/en/latest/install.html).

`  

_10

$ apt-get install pgloader

  
`

  2. Create a configuration file that specifies the source data and the target Supabase database (e.g., config.load). Here's an example configuration file:

`  

_10

LOAD DATABASE

_10

FROM sourcedb://USER:PASSWORD@HOST/SOURCE_DB

_10

INTO postgres://postgres.xxxx:[[email protected]](/cdn-cgi/l/email-
protection):6543/postgres

_10

ALTER SCHEMA 'public' OWNER TO 'postgres';

_10

set wal_buffers = '64MB', max_wal_senders = 0, statement_timeout = 0, work_mem
to '2GB';

  
`

Customize the source and Supabase database URL and options to fit your
specific use case:

     * `wal_buffers`: This parameter is set to '64MB' to allocate 64 megabytes of memory for write-ahead logging buffers. A larger value can help improve write performance by caching more data in memory before writing it to disk. This can be useful during data import operations to speed up the writing of transaction logs.
     * `max_wal_senders`: It is set to 0, to disable replication connections. This is done during the data import process to prevent replication-related conflicts and issues.
     * `statement_timeout`: The value is set to 0, which means it's disabled, allowing SQL statements to run without a time limit.
     * `work_mem`: It is set to '2GB', allocating 2 GB of memory for query operations. This enhances the performance of complex queries by allowing larger in-memory datasets.
  3. Run pgloader with the configuration file.

`  

_10

pgloader config.load

  
`

For databases using the Postgres engine, we recommend using the
[pg_dump](https://www.postgresql.org/docs/current/app-pgdump.html) and
[psql](https://www.postgresql.org/docs/current/app-psql.html) command line
tools.

### Option 3: Using Postgres copy command#

Read more about [Bulk data loading.](/docs/guides/database/tables#bulk-data-
loading)

### Option 4: Using the Supabase API#

The Supabase API allows you to programmatically import data into your tables.
You can use various client libraries to interact with the API and perform data
import operations. This approach is useful when you need to automate data
imports, and it gives you fine-grained control over the process. Refer to our
[API guide](/docs/guides/api) for more details.

When importing data via the Supabase API, it's advisable to refrain from bulk
imports. This helps ensure a smooth data transfer process and prevents any
potential disruptions.

Read more about [Rate Limiting, Resource Allocation, & Abuse
Prevention.](/docs/guides/platform/going-into-prod#rate-limiting-resource-
allocation--abuse-prevention)

## Preparing to import data#

Large data imports can affect your database performance. Failed imports can
also cause data corruption. Importing data is a safe and common operation, but
you should plan ahead if you're importing a lot of data, or if you're working
in a production environment.

### 1\. Back up your data#

Backups help you restore your data if something goes wrong. Databases on Pro,
Team and Enterprise Plans are automatically backed up on schedule, but you can
also take your own backup. See [Database
Backups](/docs/guides/platform/backups) for more information.

### 2\. Increase statement timeouts#

By default, Supabase enforces query statement timeouts to ensure fair resource
allocation and prevent long-running queries from affecting the overall system.
When importing large datasets, you may encounter timeouts. To address this:

  * **Increase the Statement Timeout** : You can adjust the statement timeout for your session or connection to accommodate longer-running queries. Be cautious when doing this, as excessively long queries can negatively impact system performance. Read more about [Statement Timeouts](/docs/guides/database/postgres/configuration).

### 3\. Estimate your required disk size#

Large datasets consume disk space. Ensure your Supabase project has sufficient
disk capacity to accommodate the imported data. If you know how big your
database is going to be, you can manually increase the size in your [projects
database settings](/dashboard/project/_/settings/database).

Read more about [disk management](/docs/guides/platform/database-size#disk-
management).

### 4\. Disable triggers#

When importing large datasets, it's often beneficial to disable triggers
temporarily. Triggers can significantly slow down the import process,
especially if they involve complex logic or referential integrity checks.
After the import, you can re-enable the triggers.

To disable triggers, use the following SQL commands:

`  

_10

-- Disable triggers on a specific table

_10

ALTER TABLE table_name DISABLE TRIGGER ALL;

_10

_10

-- To re-enable triggers

_10

ALTER TABLE table_name ENABLE TRIGGER ALL;

  
`

### 5\. Rebuild indices after data import is complete#

Indexing is crucial for query performance, but building indices while
importing a large dataset can be time-consuming. Consider building or
rebuilding indices after the data import is complete. This approach can
significantly speed up the import process and reduce the overall time
required.

To build an index after the data import:

`  

_10

-- Create an index on a table

_10

create index index_name on table_name (column_name);

  
`

Read more about [Managing Indexes in
PostgreSQL](/docs/guides/database/postgres/indexes).

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/content/guides/database/import-
data.mdx)

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

