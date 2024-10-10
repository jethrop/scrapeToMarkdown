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
  6.   7. [Custom access token hook](/docs/guides/auth/auth-hooks/custom-access-token-hook)
  8. 

# Custom Access Token Hook

## Customize the access token issued by Supabase Auth

* * *

The custom access token hook runs before a token is issued and allows you to
add additional claims based on the authentication method used.

Claims returned must conform to our specification. Supabase Auth will check
for these claims after the hook is run and return an error if they are not
present.

These are the fields currently available on an access token:

Required Claims: `aud`, `exp`, `iat`, `sub`, `email`, `phone`, `role`, `aal`,
`session_id` Optional Claims: `jti`, `iss`, `nbf`, `app_metadata`,
`user_metadata`, `amr`

**Inputs**

Field| Type| Description  
---|---|---  
`user_id`| `string`| Unique identifier for the user attempting to sign in.  
`claims`| `object`| Claims which are included in the access token.  
`authentication_method`| `string`| The authentication method used to request
the access token. Possible values include: `oauth`, `password`, `otp`, `totp`,
`recovery`, `invite`, `sso/saml`, `magiclink`, `email/signup`, `email_change`,
`token_refresh`, `anonymous`.  
  
JSONJSON Schema

`  

_19

{

_19

"user_id": "8ccaa7af-909f-44e7-84cb-67cdccb56be6",

_19

"claims": {

_19

"aud": "authenticated",

_19

"exp": 1715690221,

_19

"iat": 1715686621,

_19

"sub": "8ccaa7af-909f-44e7-84cb-67cdccb56be6",

_19

"email": "",

_19

"phone": "",

_19

"app_metadata": {},

_19

"user_metadata": {},

_19

"role": "authenticated",

_19

"aal": "aal1",

_19

"amr": [ { "method": "anonymous", "timestamp": 1715686621 } ],

_19

"session_id": "4b938a09-5372-4177-a314-cfa292099ea2",

_19

"is_anonymous": true

_19

},

_19

"authentication_method": "anonymous"

_19

}

  
`

**Outputs**

Return these only if your hook processed the input without errors.

Field| Type| Description  
---|---|---  
`claims`| `object`| The updated claims after the hook has been run.  
  
SQLHTTP

Add admin roleAdd claim via plv8Restrict access to SSO users

You can allow registered admin users to perform restricted actions by granting
an `admin` claim to their token.

Create a profiles table with an `is_admin` flag:

`  

_10

create table profiles (

_10

user_id uuid not null primary key references auth.users (id),

_10

is_admin boolean not null default false

_10

);

  
`

Create a hook:

`  

_40

create or replace function public.custom_access_token_hook(event jsonb)

_40

returns jsonb

_40

language plpgsql

_40

as $$

_40

declare

_40

claims jsonb;

_40

is_admin boolean;

_40

begin

_40

-- Check if the user is marked as admin in the profiles table

_40

select is_admin into is_admin from profiles where user_id =
(event->>'user_id')::uuid;

_40

_40

-- Proceed only if the user is an admin

_40

if is_admin then

_40

claims := event->'claims';

_40

_40

-- Check if 'app_metadata' exists in claims

_40

if jsonb_typeof(claims->'app_metadata') is null then

_40

-- If 'app_metadata' does not exist, create an empty object

_40

claims := jsonb_set(claims, '{app_metadata}', '{}');

_40

end if;

_40

_40

-- Set a claim of 'admin'

_40

claims := jsonb_set(claims, '{app_metadata, admin}', 'true');

_40

_40

-- Update the 'claims' object in the original event

_40

event := jsonb_set(event, '{claims}', claims);

_40

end if;

_40

_40

-- Return the modified or original event

_40

return event;

_40

end;

_40

$$;

_40

_40

grant all

_40

on table public.profiles

_40

to supabase_auth_admin;

_40

_40

revoke all

_40

on table public.profiles

_40

from authenticated, anon, public;

  
`

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/content/guides/auth/auth-
hooks/custom-access-token-hook.mdx)

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

