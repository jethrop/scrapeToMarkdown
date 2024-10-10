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
  6.   7. [MFA verification hook](/docs/guides/auth/auth-hooks/mfa-verification-hook)
  8. 

# MFA Verification Hook

* * *

You can add additional checks to the [Supabase MFA
implementation](/docs/guides/auth/auth-mfa) with hooks. For example, you can:

  * Limit the number of verification attempts performed over a period of time.
  * Sign out users who have too many invalid verification attempts.
  * Count, rate limit, or ban sign-ins.

**Inputs**

Supabase Auth will send a payload containing these fields to your hook:

Field| Type| Description  
---|---|---  
`factor_id`| `string`| Unique identifier for the MFA factor being verified  
`factor_type`| `string`| `totp` or `phone`  
`user_id`| `string`| Unique identifier for the user  
`valid`| `boolean`| Whether the verification attempt was valid. For TOTP, this
means that the six digit code was correct (true) or incorrect (false).  
  
JSONJSON Schema

`  

_10

{

_10

"factor_id": "6eab6a69-7766-48bf-95d8-bd8f606894db",

_10

"user_id": "3919cb6e-4215-4478-a960-6d3454326cec",

_10

"valid": true

_10

}

  
`

**Outputs**

Return this if your hook processed the input without errors.

Field| Type| Description  
---|---|---  
`decision`| `string`| The decision on whether to allow authentication to move
forward. Use `reject` to deny the verification attempt and log the user out of
all active sessions. Use `continue` to use the default Supabase Auth behavior.  
`message`| `string`| The message to show the user if the decision was
`reject`.  
  
`  

_10

{

_10

"decision": "reject",

_10

"message": "You have exceeded maximum number of MFA attempts."

_10

}

  
`

SQL

Limit failed MFA verification attempts

Your company requires that a user can input an incorrect MFA Verification code
no more than once every 2 seconds.

Create a table to record the last time a user had an incorrect MFA
verification attempt for a factor.

`  

_10

create table public.mfa_failed_verification_attempts (

_10

user_id uuid not null,

_10

factor_id uuid not null,

_10

last_failed_at timestamp not null default now(),

_10

primary key (user_id, factor_id)

_10

);

  
`

Create a hook to read and write information to this table. For example:

`  

_58

create function public.hook_mfa_verification_attempt(event jsonb)

_58

returns jsonb

_58

language plpgsql

_58

as $$

_58

declare

_58

last_failed_at timestamp;

_58

begin

_58

if event->'valid' is true then

_58

-- code is valid, accept it

_58

return jsonb_build_object('decision', 'continue');

_58

end if;

_58

_58

select last_failed_at into last_failed_at

_58

from public.mfa_failed_verification_attempts

_58

where

_58

user_id = event->'user_id'

_58

and

_58

factor_id = event->'factor_id';

_58

_58

if last_failed_at is not null and now() - last_failed_at < interval '2
seconds' then

_58

-- last attempt was done too quickly

_58

return jsonb_build_object(

_58

'error', jsonb_build_object(

_58

'http_code', 429,

_58

'message', 'Please wait a moment before trying again.'

_58

)

_58

);

_58

end if;

_58

_58

-- record this failed attempt

_58

insert into public.mfa_failed_verification_attempts

_58

(

_58

user_id,

_58

factor_id,

_58

last_refreshed_at

_58

)

_58

values

_58

(

_58

event->'user_id',

_58

event->'factor_id',

_58

now()

_58

)

_58

on conflict do update

_58

set last_refreshed_at = now();

_58

_58

-- finally let Supabase Auth do the default behavior for a failed attempt

_58

return jsonb_build_object('decision', 'continue');

_58

end;

_58

$$;

_58

_58

-- Assign appropriate permissions and revoke access

_58

grant all

_58

on table public.mfa_failed_verification_attempts

_58

to supabase_auth_admin;

_58

_58

revoke all

_58

on table public.mfa_failed_verification_attempts

_58

from authenticated, anon, public;

  
`

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/content/guides/auth/auth-
hooks/mfa-verification-hook.mdx)

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

