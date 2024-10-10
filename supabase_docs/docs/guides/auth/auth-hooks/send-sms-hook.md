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

Auth

  1. Auth
  2.   3. More
  4.   5. [Auth Hooks](/docs/guides/auth/auth-hooks)
  6.   7. [Send SMS hook](/docs/guides/auth/auth-hooks/send-sms-hook)
  8. 

# Send SMS Hook

## Use a custom SMS provider to send authentication messages

* * *

Runs before a message is sent. Use the hook to:

  * Use a regional SMS Provider
  * Use alternate messaging channels such as WhatsApp
  * Adjust the message body to include platform specific fields such as the [AppHash](https://developers.google.com/identity/sms-retriever/overview)

**Inputs**

Field| Type| Description  
---|---|---  
`user`| [`User`](/docs/guides/auth/users#the-user-object)| The user attempting
to sign in.  
`sms`| `object`| Metadata specific to the SMS sending process. Includes the
OTP.  
  
JSONJSON Schema

`  

_42

{

_42

"user": {

_42

"id": "6481a5c1-3d37-4a56-9f6a-bee08c554965",

_42

"aud": "authenticated",

_42

"role": "authenticated",

_42

"email": "",

_42

"phone": "+1333363128",

_42

"phone_confirmed_at": "2024-05-13T11:52:48.157306Z",

_42

"confirmation_sent_at": "2024-05-14T12:31:52.824573Z",

_42

"confirmed_at": "2024-05-13T11:52:48.157306Z",

_42

"phone_change_sent_at": "2024-05-13T11:47:02.183064Z",

_42

"last_sign_in_at": "2024-05-13T11:52:48.162518Z",

_42

"app_metadata": {

_42

"provider": "phone",

_42

"providers": ["phone"]

_42

},

_42

"user_metadata": {},

_42

"identities": [

_42

{

_42

"identity_id": "3be5e552-65aa-41d9-9db9-2a502f845459",

_42

"id": "6481a5c1-3d37-4a56-9f6a-bee08c554965",

_42

"user_id": "6481a5c1-3d37-4a56-9f6a-bee08c554965",

_42

"identity_data": {

_42

"email_verified": false,

_42

"phone": "+1612341244428",

_42

"phone_verified": true,

_42

"sub": "6481a5c1-3d37-4a56-9f6a-bee08c554965"

_42

},

_42

"provider": "phone",

_42

"last_sign_in_at": "2024-05-13T11:52:48.155562Z",

_42

"created_at": "2024-05-13T11:52:48.155599Z",

_42

"updated_at": "2024-05-13T11:52:48.159391Z"

_42

}

_42

],

_42

"created_at": "2024-05-13T11:45:33.7738Z",

_42

"updated_at": "2024-05-14T12:31:52.82475Z",

_42

"is_anonymous": false

_42

},

_42

"sms": {

_42

"otp": "561166"

_42

}

_42

}

  
`

**Outputs**

  * No outputs are required. An empty response with a status code of 200 is taken as a successful response.

SQLHTTP

Queue SMS Messages

Your company uses a worker to manage all messaging related jobs. For
performance reasons, the messaging system sends messages in intervals via a
job queue. Instead of sending a message immediately, messages are queued and
sent in periodic intervals via `pg_cron`.

Create a table to store jobs

`  

_10

create table job_queue (

_10

job_id uuid primary key default gen_random_uuid(),

_10

job_data jsonb not null,

_10

created_at timestamp default now(),

_10

status text default 'pending',

_10

priority int default 0,

_10

retry_count int default 0,

_10

max_retries int default 2,

_10

scheduled_at timestamp default now()

_10

);

  
`

Create the hook:

`  

_31

create or replace function send_sms(event jsonb) returns void as $$

_31

declare

_31

job_data jsonb;

_31

scheduled_time timestamp;

_31

priority int;

_31

begin

_31

-- extract phone and otp from the event json

_31

job_data := jsonb_build_object(

_31

'phone', event->'user'->>'phone',

_31

'otp', event->'sms'->>'otp'

_31

);

_31

_31

-- calculate the nearest 5-minute window for scheduled_time

_31

scheduled_time := date_trunc('minute', now()) + interval '5 minute' *
floor(extract('epoch' from (now() - date_trunc('minute', now())) / 60) / 5);

_31

_31

-- assign priority dynamically (example logic: higher priority for earlier
scheduled time)

_31

priority := extract('epoch' from (scheduled_time - now()))::int;

_31

_31

-- insert the job into the job_queue table

_31

insert into job_queue (job_data, priority, scheduled_at, max_retries)

_31

values (job_data, priority, scheduled_time, 2);

_31

end;

_31

$$ language plpgsql;

_31

_31

grant all

_31

on table public.job_queue

_31

to supabase_auth_admin;

_31

_31

revoke all

_31

on table public.job_queue

_31

from authenticated, anon;

  
`

Create a function to periodically run and dequeue all jobs

`  

_42

create or replace function dequeue_and_run_jobs() returns void as $$

_42

declare

_42

job record;

_42

begin

_42

for job in

_42

select * from job_queue

_42

where status = 'pending'

_42

and scheduled_at <= now()

_42

order by priority desc, created_at

_42

for update skip locked

_42

loop

_42

begin

_42

-- add job processing logic here.

_42

-- for demonstration, we'll just update the job status to 'completed'.

_42

update job_queue

_42

set status = 'completed'

_42

where job_id = job.job_id;

_42

_42

exception when others then

_42

-- handle job failure and retry logic

_42

if job.retry_count < job.max_retries then

_42

update job_queue

_42

set retry_count = retry_count + 1,

_42

scheduled_at = now() + interval '1 minute' -- delay retry by 1 minute

_42

where job_id = job.job_id;

_42

else

_42

update job_queue

_42

set status = 'failed'

_42

where job_id = job.job_id;

_42

end if;

_42

end;

_42

end loop;

_42

end;

_42

$$ language plpgsql;

_42

_42

grant execute

_42

on function public.dequeue_and_run_jobs

_42

to supabase_auth_admin;

_42

_42

revoke execute

_42

on function public.dequeue_and_run_jobs

_42

from authenticated, anon;

  
`

Configure `pg_cron` to run the job on an interval. You can use a tool like
[crontab.guru](https://crontab.guru/) to check that your job is running on an
appropriate schedule. Ensure that `pg_cron` is enabled under `Database >
Extensions`

`  

_10

select

_10

cron.schedule(

_10

'* * * * *', -- this cron expression means every minute.

_10

'select dequeue_and_run_jobs();'

_10

);

  
`

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/content/guides/auth/auth-
hooks/send-sms-hook.mdx)

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

