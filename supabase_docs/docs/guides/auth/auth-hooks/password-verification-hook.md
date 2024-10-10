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
  6.   7. [Password verification hook](/docs/guides/auth/auth-hooks/password-verification-hook)
  8. 

# Password Verification Hook

* * *

Your company wishes to increase security beyond the requirements of the
default password implementation in order to fulfill security or compliance
requirements. You plan to track the status of a password sign-in attempt and
take action via an email or a restriction on logins where necessary.

As this hook runs on unauthenticated requests, malicious users can abuse the
hook by calling it multiple times. Pay extra care when using the hook as you
can unintentionally block legitimate users from accessing your application.

Check if a password is valid prior to taking any additional action to ensure
the user is legitimate. Where possible, send an email or notification instead
of blocking the user.

**Inputs**

Field| Type| Description  
---|---|---  
`user_id`| `string`| Unique identifier for the user attempting to sign in.
Correlate this to the `auth.users` table.  
`valid`| `boolean`| Whether the password verification attempt was valid.  
  
JSONJSON Schema

`  

_10

{

_10

"user_id": "3919cb6e-4215-4478-a960-6d3454326cec",

_10

"valid": true

_10

}

  
`

**Outputs**

Return these only if your hook processed the input without errors.

Field| Type| Description  
---|---|---  
`decision`| `string`| The decision on whether to allow authentication to move
forward. Use `reject` to deny the verification attempt and log the user out of
all active sessions. Use `continue` to use the default Supabase Auth behavior.  
`message`| `string`| The message to show the user if the decision was
`reject`.  
`should_logout_user`| `boolean`| Whether to log out the user if a `reject`
decision is issued. Has no effect when a `continue` decision is issued.  
  
`  

_10

{

_10

"decision": "reject",

_10

"message": "You have exceeded maximum number of password sign-in attempts.",

_10

"should_logout_user": "false"

_10

}

  
`

SQL

Limit failed password verification attemptsSend email notification on failed
password attempts

As part of new security measures within the company, users can only input an
incorrect password every 10 seconds and not more than that. You want to write
a hook to enforce this.

Create a table to record each user's last incorrect password verification
attempt.

`  

_10

create table public.password_failed_verification_attempts (

_10

user_id uuid not null,

_10

last_failed_at timestamp not null default now(),

_10

primary key (user_id)

_10

);

  
`

Create a hook to read and write information to this table. For example:

`  

_54

create function public.hook_password_verification_attempt(event jsonb)

_54

returns jsonb

_54

language plpgsql

_54

as $$

_54

declare

_54

last_failed_at timestamp;

_54

begin

_54

if event->'valid' is true then

_54

-- password is valid, accept it

_54

return jsonb_build_object('decision', 'continue');

_54

end if;

_54

_54

select last_failed_at into last_failed_at

_54

from public.password_failed_verification_attempts

_54

where

_54

user_id = event->'user_id';

_54

_54

if last_failed_at is not null and now() - last_failed_at < interval '10
seconds' then

_54

-- last attempt was done too quickly

_54

return jsonb_build_object(

_54

'error', jsonb_build_object(

_54

'http_code', 429,

_54

'message', 'Please wait a moment before trying again.'

_54

)

_54

);

_54

end if;

_54

_54

-- record this failed attempt

_54

insert into public.password_failed_verification_attempts

_54

(

_54

user_id,

_54

last_failed_at

_54

)

_54

values

_54

(

_54

event->'user_id',

_54

now()

_54

)

_54

on conflict do update

_54

set last_failed_at = now();

_54

_54

-- finally let Supabase Auth do the default behavior for a failed attempt

_54

return jsonb_build_object('decision', 'continue');

_54

end;

_54

$$;

_54

_54

-- Assign appropriate permissions

_54

grant all

_54

on table public.password_failed_verification_attempts

_54

to supabase_auth_admin;

_54

_54

revoke all

_54

on table public.password_failed_verification_attempts

_54

from authenticated, anon, public;

  
`

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/content/guides/auth/auth-
hooks/password-verification-hook.mdx)

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

