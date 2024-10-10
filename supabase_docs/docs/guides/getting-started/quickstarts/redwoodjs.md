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

Getting Started

  1. [Start with Supabase](/docs/guides/getting-started)
  2.   3. Framework Quickstarts
  4.   5. [RedwoodJS](/docs/guides/getting-started/quickstarts/redwoodjs)
  6. 

# Use Supabase with RedwoodJS

## Learn how to create a Supabase project, add some sample data to your
database using Prisma migration and seeds, and query the data from a RedwoodJS
app.

* * *

1

### Setup your new Supabase Project

[Create a new project](https://supabase.com/dashboard) in the Supabase
Dashboard.

Be sure to make note of the Database Password you used as you will need this
later to connect to your database.

![New project for redwoodjs](/docs/img/guides/getting-
started/quickstarts/redwoodjs/new-project.png)

2

### Gather Database Connection Strings

Go to the [database settings
page](https://supabase.com/dashboard/project/_/settings/database). In this
quickstart, we are going to connect via the connection pooler. If your network
supports IPv6, you can connect to the database directly without using the
connection pooler.

We will use the pooler both in `Transaction` and `Session` mode. `Transaction`
mode is used for application queries and `Session` mode is used for running
migrations with Prisma.

To do this, set the connection mode to `Transaction` in the [database settings
page](https://supabase.com/dashboard/project/_/settings/database) and copy the
connection string and append `?pgbouncer=true&&connection_limit=1`.
`pgbouncer=true` disables Prisma from generating prepared statements. This is
required since our connection pooler does not support prepared statements in
transaction mode yet. The `connection_limit=1` parameter is only required if
you are using Prisma from a serverless environment. This is the Transaction
mode connection string.

To get the Session mode connection pooler string, change the port of the
connection string from the dashboard to 5432.

You will need the Transaction mode connection string and the Session mode
connection string to setup environment variables in Step 5.

You can copy and paste these connection strings from the Supabase Dashboard
when needed in later steps.

![pooled connection for redwoodjs](/docs/img/guides/getting-
started/quickstarts/redwoodjs/pooled-connection-strings.png)

3

### Create a RedwoodJS app

Create a RedwoodJS app with TypeScript.

The [`yarn` package manager](https://yarnpkg.com) is required to create a
RedwoodJS app. You will use it to run RedwoodJS commands later.

While TypeScript is recommended, If you want a JavaScript app, omit the `--ts`
flag.

Terminal

`  

_10

yarn create redwood-app my-app --ts

  
`

4

### Open your RedwoodJS app in VS Code

You'll develop your app, manage database migrations, and run your app in VS
Code.

Terminal

`  

_10

cd my-app

_10

code .

  
`

5

### Configure Environment Variables

In your `.env` file, add the following environment variables for your database
connection:

  * The `DATABASE_URL` should use the Transaction mode connection string you copied in Step 1.

  * The `DIRECT_URL` should use the Session mode connection string you copied in Step 1.

.env

`  

_10

# Transaction mode connection string used for migrations

_10

DATABASE_URL="postgres://postgres.[project-ref]:[db-
password]@xxx.pooler.supabase.com:6543/postgres?pgbouncer=true&connection_limit=1"

_10

_10

# Session mode connection string — used by Prisma Client

_10

DIRECT_URL="postgres://postgres.[project-ref]:[db-
password]@xxx.pooler.supabase.com:5432/postgres"

  
`

6

### Update your Prisma Schema

By default, RedwoodJS ships with a SQLite database, but we want to use
PostgreSQL.

Update your Prisma schema file `api/db/schema.prisma` to use your Supabase
PostgreSQL database connection environment variables you setup in Step 5.

api/prisma/schema.prisma

`  

_10

datasource db {

_10

provider = "postgresql"

_10

url = env("DATABASE_URL")

_10

directUrl = env("DIRECT_URL")

_10

}

  
`

7

### Create the Country model and apply a schema migration

Create the Country model in `api/db/schema.prisma` and then run `yarn rw
prisma migrate dev` from your terminal to apply the migration.

api/db/schema.prisma

`  

_10

model Country {

_10

id Int @id @default(autoincrement())

_10

name String @unique

_10

}

  
`

8

### Update seed script

Let's seed the database with a few countries.

Update the file `scripts/seeds.ts` to contain the following code:

scripts/seed.ts

`  

_20

import type { Prisma } from '@prisma/client'

_20

import { db } from 'api/src/lib/db'

_20

_20

export default async () => {

_20

try {

_20

const data: Prisma.CountryCreateArgs['data'][] = [

_20

{ name: 'United States' },

_20

{ name: 'Canada' },

_20

{ name: 'Mexico' },

_20

]

_20

_20

console.log('Seeding countries ...')

_20

_20

const countries = await db.country.createMany({ data })

_20

_20

console.log('Done.', countries)

_20

} catch (error) {

_20

console.error(error)

_20

}

_20

}

  
`

9

### Seed your database

Run the seed database command to populate the `Country` table with the
countries you just created.

The reset database command `yarn rw prisma db reset` will recreate the tables
and will also run the seed script.

Terminal

`  

_10

yarn rw prisma db seed

  
`

10

### Scaffold the Country UI

Now, we'll use RedwoodJS generators to scaffold a CRUD UI for the `Country`
model.

Terminal

`  

_10

yarn rw g scaffold country

  
`

11

### Start the app

Start the app via `yarn rw dev`. A browser will open to the RedwoodJS Splash
page.

![RedwoodJS Splash Page](/docs/img/redwoodjs-qs-splash.png)

12

### View Countries UI

Click on `/countries` to visit <http://localhost:8910/countries> where should
see the list of countries.

You may now edit, delete, and add new countries using the scaffolded UI.

![RedwoodJS Splash Page](/docs/img/redwoodjs-qs-countries-ui.png)

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/content/guides/getting-
started/quickstarts/redwoodjs.mdx)

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

