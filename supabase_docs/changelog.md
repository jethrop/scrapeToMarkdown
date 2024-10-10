# Changelog

New updates and product improvements

### [Moving to Org-based billing
](https://github.com/orgs/supabase/discussions/17061)

Aug 31, 2023

We’re fixing the billing system at Supabase - moving from “project-based” to
“organization-based”. We should have started with this model, but I wasn’t
wise enough to know that when we started. We need to make these changes to
roll out Preview Environments / Branching. It also includes:

  * [long-requested](https://github.com/orgs/supabase/discussions/6681) project transfers between organizations
  * An extra 1GB egress on the Free Tier
  * Consolidated invoices
  * Self-serve Team plan
  * Updates for branching
  * No more “upfront” charges for Database Compute Addons

[See all changes in the blog post](https://supabase.com/blog/organization-
based-billing)

## Free plan#

First, and most importantly - there is only one change that affects the free
plan, and that is a good one for you: you now an extra 1GB of egress.

Usage Item| Old plan (per project)| New plan (org based)  
---|---|---  
Egress| 4GB - (2GB Database + 2GB Storage)| 5GB across Database + Storage  
Database Space| 500MB| 500MB  
Storage Space| 1GB| 1GB  
Monthly Active Users| 50K| 50K  
Edge Function Invocations| 500K| 500K  
Edge Function Count| 10| 10  
Realtime Message Count| 2 million| 2 million  
Realtime Peak Connections| 200| 200  
| 2 free projects| 2 free orgs (1 free database per org)  
  
On top of an extra 1GB of egress for free, now that egress is unified across
your org it means that if you aren’t using Supabase Storage, you get even more
Database Egress (5GB instead of 2GB previously)

If you are currently running 2 free projects however, _**this does require
some work from you**_. Because we are now working on an Org-level, instead of
Projects, you will need to:

  1. Create a new “Free org”
  2. Transfer one of your free projects into the newly-created org

This should be done before the end of October, but don’t worry - we’ll give
you frequent comms and clear instructions once the change has been rolled out
(4th Sept).

## Other changes#

We’ve made a lot of improvements to the billing system. Read the full
announcement on our [blog](https://supabase.com/blog/organization-based-
billing) or dive into the related
[docs](https://supabase.com/docs/guides/platform/org-based-billing) for more
details.

## Help, my bill increased!#

This is a major change, and we've tried to design it in a way that's cheaper
for everyone. If your bill has increased as a result of this change, that's
not our intention. Please submit a Support ticket [on the
dashboard](https://supabase.com/dashboard/support/new?category=billing&subject=Organization%20based%20billing)
and we'll figure out a solution.

## Please keep this discussion on topic#

We welcome any questions/feedback about this change, but please keep this
discussion focused only on this change! It's important for those who want to
learn more or are confused. If you have something off-topic, please open a new
discussion or join an existing discussion

### [Security Patch Notice
](https://github.com/orgs/supabase/discussions/9314)

Oct 4, 2022

## Security Patch Notice#

To better secure your Supabase server instances, we will be removing
**superuser** access from the dashboard SQL Editor over the next 30 days.
Existing projects with tables, functions, or other Postgres entities created
via the dashboard SQL Editor require a **one time** migration to be run. This
migration should take less than 10 seconds to run but since it modifies your
existing schema, we will be rolling out this change over a buffer period to
minimise breakages.

### Opt-in Period: 5 Oct - 5 Nov#

During the opt-in period, a notification will be delivered to all affected
Supabase projects. The notification contains instructions to manually apply
the migration. If you have separate staging and production Supabase projects,
apply it on the staging project first to verify everything is working as
expected.

![](https://user-
images.githubusercontent.com/1639722/193756841-9442ad32-a561-4262-962b-edc279571632.png)

If you only have one Supabase project, try to avoid hours of high application
traffic when applying the migration to minimise potential downtime. If you
notice elevated error rates or other unusual activities after migrating,
follow the rollback instructions to **revert** the change. Both apply now and
rollback actions are idempotent. If you encounter any problems during
migration or rollback, please contact [[email protected]](/cdn-cgi/l/email-
protection#99eaece9e9f6ebedd9eaece9f8fbf8eafcb7f0f6) for further assistance.

For paused projects, applying now will schedule the migration script to run
the next time your project is restored. We suggest that you restore your
project immediately to verify that everything works or rollback if necessary.
If you project is in any other states, please contact [[email
protected]](/cdn-cgi/l/email-
protection#6714121717081513271412170605061402490e08) to bring it to an active
healthy state before continuing with the migration.

After successfully applying the migration, all entities you have created from
the dashboard's SQL Editor will be owned by a temporary role. These entities
are currently owned by `supabase_admin` role by default. You can check the
current owner of all your schemas using the query below.

`  

_10

select *, nspowner::regrole::name from pg_namespace;

  
`

New entities created via the SQL Editor will also be owned by this temporary
role. Since the temporary role is not a superuser, there are some restrictions
with using the SQL Editor after migrating. If you are unsure whether those
restrictions affect your project, please contact [[email protected]](/cdn-
cgi/l/email-protection#bac9cfcacad5c8cefac9cfcadbd8dbc9df94d3d5) for
assistance.

### After 5 Nov#

After the opt-in period, you will receive another notification to drop the
temporary role and reassign all entities owned by the temporary role to
`postgres` role. The SQL Editor will also default to using `postgres` role.
New projects created after 5 Nov will also default to using the `postgres`
role. Since this change is irreversible, it is crucial that you run the
migration during the opt-in period to verify that your project continues to
work.

For any projects **not** migrated after 5 Nov deadline, we will run the
migration on your behalf to reassign all entities to `postgres` role. No
temporary role can be used for rollback. If you notice any breakages then,
please do not hesitate to contact [[email protected]](/cdn-cgi/l/email-
protection#91e2e4e1e1fee3e5d1e2e4e1f0f3f0e2f4bff8fe).

## Restricted Features#

After revoking superuser access, you will not be able to perform the following
actions through the dashboard SQL Editor.

### Managing Event Triggers#

You will no longer be able to create, alter, or drop [event
triggers](https://www.postgresql.org/docs/current/event-triggers.html)
directly through SQL statements.

Event triggers can only be created by superusers and you will not be able to
manage them after the migration. One exception is Postgres extensions. When
toggling extensions, they can still create or drop event triggers as needed.

If you are currently using custom event triggers, please contact [[email
protected]](/cdn-cgi/l/email-
protection#44373134342b36300437313425262537216a2d2b) to explain your use case.
We will try our best to figure out an alternative for your project. Note that
regular [triggers](https://www.postgresql.org/docs/current/sql-
createtrigger.html) are unaffected by the migration.

### Restricted use of Supabase schemas#

You will no longer be able to: create, alter, or drop tables, views,
functions, triggers, sequences, and other entities in Supabase managed
schemas, including `extensions`, `graphql`, `realtime`, and
`supabase_functions`.

Supabase managed schemas are used to support platform features for all
projects. Entities in these schemas are owned by `supabase_admin` role to
prevent users from accidentally overriding them and breaking platform
features. Unless explicitly granted, non-superuser roles cannot manage
entities in Supabase managed schemas after the migration.

If you think modifying these schemas is necessary for your project, please
contact [[email protected]](/cdn-cgi/l/email-
protection#f685838686998482b68583869794978593d89f99) to explain your use case.
We will try our best to accommodate your use case using alternative
suggestions.

Entities in `auth` and `storage` schemas have been explicitly granted all
permissions to `postgres` role. Therefore, you can still manage these schemas
directly through SQL statements. If you have existing triggers created on
these schemas, they will continue to work as well.

All user defined schemas and the `public` schema will be owned by `postgres`
role after the migration. Therefore, you should be able to manage entities in
those schemas directly through SQL statements. One exception is if you have
manually changed the owner of specific schemas before. In that case, you can
either reassign their owner to `postgres` role manually or leave them
untouched. Please reach out to [[email protected]](/cdn-cgi/l/email-
protection#097a7c7979667b7d497a7c79686b687a6c276066) if you are unsure what to
do.

### Managing RLS Policies on Supabase schemas#

You will no longer be able to create or drop [RLS
policies](https://www.postgresql.org/docs/current/ddl-rowsecurity.html) on
entities in Supabase managed schemas.

RLS policies can only be created or dropped by entity owners or superusers.
After the migration, you can’t manage RLS policies in Supabase managed schemas
through the SQL Editor. If you need to expose certain tables in `realtime`
schema to `anon` or `authenticated` users, one way is to create a view in the
`public` schema using the `postgres` role.

RLS policies in `auth`, `storage`, `public`, and all user defined schemas can
still be managed directly through SQL statements. Unless you have policies
that check for `supabase_admin` role, all existing RLS policies should be
unaffected by the migration.

### Restricted use of Role Attributes#

You will no longer be able to alter [role
attributes](https://www.postgresql.org/docs/current/role-attributes.html) of
replication, superuser, and reserved roles directly through the SQL Editor.

Only superuser roles can alter attributes of other superuser and replication
roles. Reserved roles include `anon`, `authenticated`, `postgres`,
`service_role`, etc. After the migration, you will not be able to change
attributes of these roles directly through SQL statements. You can still alter
attributes of other roles created by yourself, except to elevate those roles
to superuser or replication.

Some common attributes that can’t be changed include password, login, and
bypassrls. Here are some known workarounds:

  1. To change your `postgres` role password, you can do it via [dashboard settings](https://supabase.com/docs/guides/database/managing-passwords) page.
  2. If you need to run one-off scripts that bypass RLS, you can use the provided [service key](https://egghead.io/lessons/supabase-use-the-supabase-service-key-to-bypass-row-level-security).
  3. If you are [pushing schema migrations](https://supabase.com/docs/guides/cli/local-development#deploy-database-changes) from CLI, superuser privilege is no longer required as all entities are owned by `postgres` role after the migration.
  4. [Migrating between projects](https://supabase.com/docs/guides/platform/migrating-and-upgrading-projects#migrate-your-project) no longer requires superuser privilege.

### Update 26/10/22#

A number of users reported the following error accessing the dashboard
restoring a paused project.

`  

_10

Error: [500] failed to get pg.tables: password authentication failed for user
"postgres_temporary_object_holder"

  
`

It is due to a bug in the restore script that we have since fixed. If you are
still experiencing this issue, you may pause and restore the project again to
fix it manually. If that fails, please don't hesitate to contact [[email
protected]](/cdn-cgi/l/email-
protection#6d1e181d1d021f192d1e181d0c0f0c1e08430402).

### Update 03/11/22#

We will be adding additional privileges to the `postgres` role to do the
following actions, which otherwise can only be done by a superuser:

  * manage the `bypassrls` role attribute
  * set the `session_replication_role` runtime config

### Update 28/12/22#

  * TimescaleDB extension fails to toggle (we can enable manually via support)
  * Custom [security definer functions](https://supabase.com/docs/guides/auth/row-level-security#policies-with-security-definer-functions) will run as non-superuser (only affects extensions schemas owned by supabase_admin)

[ Previous](/changelog)

## Build in a weekend, scale to millions

[Start your project](https://supabase.com/dashboard)[Request a
demo](/contact/sales)

