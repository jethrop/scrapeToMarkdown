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

Local Development

  1. [Local Dev / CLI](/docs/guides/local-development)
  2.   3. CLI
  4.   5. [Configuration](/docs/guides/local-development/cli/config)
  6. 

# Supabase CLI config

* * *

A `supabase/config.toml` file is generated after running `supabase init`.

You can edit this file to change the settings for your locally running
project. After you make changes, you will need to restart using `supabase
stop` and then `supabase start` for the changes to take effect.

## General Config#

### `project_id`#

Name| Default| Required  
---|---|---  
project_id| None| true  
  
Description

A string used to distinguish different Supabase projects on the same host.
Defaults to the working directory name when running `supabase init`.

## Auth Config#

### `auth.enabled`#

Name| Default| Required  
---|---|---  
auth.enabled| true| false  
  
Description

Enable the local GoTrue service.

See also

  * [Auth Server configuration](https://supabase.com/docs/reference/auth)

### `auth.site_url`#

Name| Default| Required  
---|---|---  
auth.site_url| "http://localhost:3000"| false  
  
Description

The base URL of your website. Used as an allow-list for redirects and for
constructing URLs used in emails.

See also

  * [Auth Server configuration](https://supabase.com/docs/reference/auth)

### `auth.additional_redirect_urls`#

Name| Default| Required  
---|---|---  
auth.additional_redirect_urls| ["https://localhost:3000"]| false  
  
Description

A list of _exact_ URLs that auth providers are permitted to redirect to post
authentication.

See also

  * [Auth Server configuration](https://supabase.com/docs/reference/auth)

### `auth.jwt_expiry`#

Name| Default| Required  
---|---|---  
auth.jwt_expiry| 3600| false  
  
Description

How long tokens are valid for, in seconds. Defaults to 3600 (1 hour), maximum
604,800 seconds (one week).

See also

  * [Auth Server configuration](https://supabase.com/docs/reference/auth)

### `auth.enable_refresh_token_rotation`#

Name| Default| Required  
---|---|---  
auth.enable_refresh_token_rotation| true| false  
  
Description

If disabled, the refresh token will never expire.

See also

  * [Auth Server configuration](https://supabase.com/docs/reference/auth)

### `auth.refresh_token_reuse_interval`#

Name| Default| Required  
---|---|---  
auth.refresh_token_reuse_interval| 10| false  
  
Description

Allows refresh tokens to be reused after expiry, up to the specified interval
in seconds. Requires enable_refresh_token_rotation = true.

See also

  * [Auth Server configuration](https://supabase.com/docs/reference/auth)

### `auth.enable_signup`#

Name| Default| Required  
---|---|---  
auth.enable_signup| true| false  
  
Description

Allow/disallow new user signups to your project.

See also

  * [Auth Server configuration](https://supabase.com/docs/reference/auth)

### `auth.enable_anonymous_sign_ins`#

Name| Default| Required  
---|---|---  
auth.enable_anonymous_sign_ins| false| false  
  
Description

Allow/disallow anonymous sign-ins to your project.

See also

  * [Auth Server configuration](https://supabase.com/docs/reference/auth)

### `auth.email.enable_signup`#

Name| Default| Required  
---|---|---  
auth.email.enable_signup| true| false  
  
Description

Allow/disallow new user signups via email to your project.

See also

  * [Auth Server configuration](https://supabase.com/docs/reference/auth)

### `auth.email.double_confirm_changes`#

Name| Default| Required  
---|---|---  
auth.email.double_confirm_changes| true| false  
  
Description

If enabled, a user will be required to confirm any email change on both the
old, and new email addresses. If disabled, only the new email is required to
confirm.

See also

  * [Auth Server configuration](https://supabase.com/docs/reference/auth)

### `auth.email.enable_confirmations`#

Name| Default| Required  
---|---|---  
auth.email.enable_confirmations| false| false  
  
Description

If enabled, users need to confirm their email address before signing in.

See also

  * [Auth Server configuration](https://supabase.com/docs/reference/auth)

### `auth.email.smtp.host`#

Name| Default| Required  
---|---|---  
auth.email.smtp.host| inbucket| false  
  
Description

Hostname or IP address of the SMTP server.

### `auth.email.smtp.port`#

Name| Default| Required  
---|---|---  
auth.email.smtp.port| 2500| false  
  
Description

Port number of the SMTP server.

### `auth.email.smtp.user`#

Name| Default| Required  
---|---|---  
auth.email.smtp.user| None| false  
  
Description

Username for authenticating with the SMTP server.

### `auth.email.smtp.pass`#

Name| Default| Required  
---|---|---  
auth.email.smtp.pass| None| false  
  
Description

Password for authenticating with the SMTP server.

### `auth.email.smtp.admin_email`#

Name| Default| Required  
---|---|---  
auth.email.smtp.admin_email| [[email protected]](/cdn-cgi/l/email-protection)|
false  
  
Description

Email used as the sender for emails sent from the application.

### `auth.email.smtp.sender_name`#

Name| Default| Required  
---|---|---  
auth.email.smtp.sender_name| None| false  
  
Description

Display name used as the sender for emails sent from the application.

### `auth.email.template.<type>.subject`#

Name| Default| Required  
---|---|---  
auth.email.template.type.subject| None| false  
  
Description

The full list of email template types are:

  * `invite`
  * `confirmation`
  * `recovery`
  * `magic_link`
  * `email_change`

See also

  * [Auth Server configuration](https://supabase.com/docs/reference/auth)

### `auth.email.template.<type>.content_path`#

Name| Default| Required  
---|---|---  
auth.email.template.type.content_path| None| false  
  
Description

The full list of email template types are:

  * `invite`
  * `confirmation`
  * `recovery`
  * `magic_link`
  * `email_change`

See also

  * [Auth Server configuration](https://supabase.com/docs/reference/auth)

### `auth.sms.enable_signup`#

Name| Default| Required  
---|---|---  
auth.sms.enable_signup| true| false  
  
Description

Allow/disallow new user signups via SMS to your project.

See also

  * [Auth Server configuration](https://supabase.com/docs/reference/auth)

### `auth.sms.enable_confirmations`#

Name| Default| Required  
---|---|---  
auth.sms.enable_confirmations| false| false  
  
Description

If enabled, users need to confirm their phone number before signing in.

See also

  * [Auth Server configuration](https://supabase.com/docs/reference/auth)

### `auth.sms.test_otp`#

Name| Default| Required  
---|---|---  
auth.sms.test_otp| None| false  
  
Description

Use pre-defined map of phone number to OTP for testing.

Usage

    
    
    1[auth.sms.test_otp]
    24152127777 = "123456"

See also

  * [Auth Server configuration](https://supabase.com/docs/reference/auth)

### `auth.sms.<provider>.enabled`#

Name| Default| Required  
---|---|---  
auth.sms.provider.enabled| false| false  
  
Description

Use an external SMS provider. The full list of providers are:

  * `twilio`
  * `twilio_verify`
  * `messagebird`
  * `textlocal`
  * `vonage`

See also

  * [Auth Server configuration](https://supabase.com/docs/reference/auth)

### `auth.sms.<twilio|twilio_verify>.account_sid`#

Name| Default| Required  
---|---|---  
auth.sms.twilio.account_sid| None| true  
  
Description

Twilio Account SID

See also

  * [Auth Server configuration](https://supabase.com/docs/reference/auth)

### `auth.sms.<twilio|twilio_verify>.message_service_sid`#

Name| Default| Required  
---|---|---  
auth.sms.twilio.message_service_sid| None| true  
  
Description

Twilio Message Service SID

See also

  * [Auth Server configuration](https://supabase.com/docs/reference/auth)

### `auth.sms.<twilio|twilio_verify>.auth_token`#

Name| Default| Required  
---|---|---  
auth.sms.twilio.auth_token| env(SUPABASE_AUTH_SMS_TWILIO_AUTH_TOKEN)| true  
  
Description

Twilio Auth Token

DO NOT commit your Twilio auth token to git. Use environment variable
substitution instead.

See also

  * [Auth Server configuration](https://supabase.com/docs/reference/auth)

### `auth.sms.messagebird.originator`#

Name| Default| Required  
---|---|---  
auth.sms.messagebird.originator| None| true  
  
Description

MessageBird Originator

See also

  * [Auth Server configuration](https://supabase.com/docs/reference/auth)

### `auth.sms.messagebird.access_key`#

Name| Default| Required  
---|---|---  
auth.sms.messagebird.access_key|
env(SUPABASE_AUTH_SMS_MESSAGEBIRD_ACCESS_KEY)| true  
  
Description

MessageBird Access Key

DO NOT commit your MessageBird access key to git. Use environment variable
substitution instead.

See also

  * [Auth Server configuration](https://supabase.com/docs/reference/auth)

### `auth.sms.textlocal.sender`#

Name| Default| Required  
---|---|---  
auth.sms.textlocal.sender| None| true  
  
Description

TextLocal Sender

See also

  * [Auth Server configuration](https://supabase.com/docs/reference/auth)

### `auth.sms.textlocal.api_key`#

Name| Default| Required  
---|---|---  
auth.sms.textlocal.api_key| env(SUPABASE_AUTH_SMS_TEXTLOCAL_API_KEY)| true  
  
Description

TextLocal API Key

DO NOT commit your TextLocal API key to git. Use environment variable
substitution instead.

See also

  * [Auth Server configuration](https://supabase.com/docs/reference/auth)

### `auth.sms.vonage.from`#

Name| Default| Required  
---|---|---  
auth.sms.vonage.from| None| true  
  
Description

Vonage From

See also

  * [Auth Server configuration](https://supabase.com/docs/reference/auth)

### `auth.sms.vonage.api_key`#

Name| Default| Required  
---|---|---  
auth.sms.vonage.api_key| None| true  
  
Description

Vonage API Key

See also

  * [Auth Server configuration](https://supabase.com/docs/reference/auth)

### `auth.sms.vonage.api_secret`#

Name| Default| Required  
---|---|---  
auth.sms.vonage.api_secret| env(SUPABASE_AUTH_SMS_VONAGE_API_SECRET)| true  
  
Description

Vonage API Secret

DO NOT commit your Vonage API secret to git. Use environment variable
substitution instead.

See also

  * [Auth Server configuration](https://supabase.com/docs/reference/auth)

### `auth.external.<provider>.enabled`#

Name| Default| Required  
---|---|---  
auth.external.provider.enabled| false| false  
  
Description

Use an external OAuth provider. The full list of providers are:

  * `apple`
  * `azure`
  * `bitbucket`
  * `discord`
  * `facebook`
  * `github`
  * `gitlab`
  * `google`
  * `kakao`
  * `keycloak`
  * `linkedin`
  * `notion`
  * `twitch`
  * `twitter`
  * `slack`
  * `spotify`
  * `workos`
  * `zoom`

See also

  * [Auth Server configuration](https://supabase.com/docs/reference/auth)

### `auth.external.<provider>.client_id`#

Name| Default| Required  
---|---|---  
auth.external.provider.client_id| None| true  
  
Description

Client ID for the external OAuth provider.

See also

  * [Auth Server configuration](https://supabase.com/docs/reference/auth)

### `auth.external.<provider>.secret`#

Name| Default| Required  
---|---|---  
auth.external.provider.secret| env(SUPABASE_AUTH_EXTERNAL_<PROVIDER>_SECRET)|
true  
  
Description

Client secret for the external OAuth provider.

DO NOT commit your OAuth provider secret to git. Use environment variable
substitution instead.

See also

  * [Auth Server configuration](https://supabase.com/docs/reference/auth)

### `auth.external.<provider>.url`#

Name| Default| Required  
---|---|---  
auth.external.provider.url| None| false  
  
Description

The base URL used for constructing the URLs to request authorization and
access tokens. Used by gitlab and keycloak. For gitlab it defaults to
https://gitlab.com. For keycloak you need to set this to your instance, for
example: https://keycloak.example.com/realms/myrealm .

See also

  * [Auth Server configuration](https://supabase.com/docs/reference/auth)

### `auth.external.<provider>.redirect_uri`#

Name| Default| Required  
---|---|---  
auth.external.provider.redirect_uri| None| false  
  
Description

The URI a OAuth2 provider will redirect to with the code and state values.

See also

  * [Auth Server configuration](https://supabase.com/docs/reference/auth)

## API Config#

### `api.enabled`#

Name| Default| Required  
---|---|---  
api.enabled| true| false  
  
Description

Enable the local PostgREST service.

See also

  * [PostgREST configuration](https://postgrest.org/en/stable/configuration.html)

### `api.port`#

Name| Default| Required  
---|---|---  
api.port| 54321| false  
  
Description

Port to use for the API URL.

Usage

    
    
    1[api]
    2port = 54321

See also

  * [PostgREST configuration](https://postgrest.org/en/stable/configuration.html)

### `api.schemas`#

Name| Default| Required  
---|---|---  
api.schemas| ["public", "storage", "graphql_public"]| false  
  
Description

Schemas to expose in your API. Tables, views and functions in this schema will
get API endpoints. `public` and `storage` are always included.

See also

  * [PostgREST configuration](https://postgrest.org/en/stable/configuration.html)

### `api.extra_search_path`#

Name| Default| Required  
---|---|---  
api.extra_search_path| ["public", "extensions"]| false  
  
Description

Extra schemas to add to the search_path of every request. public is always
included.

See also

  * [PostgREST configuration](https://postgrest.org/en/stable/configuration.html)

### `api.max_rows`#

Name| Default| Required  
---|---|---  
api.max_rows| 1000| false  
  
Description

The maximum number of rows returned from a view, table, or stored procedure.
Limits payload size for accidental or malicious requests.

See also

  * [PostgREST configuration](https://postgrest.org/en/stable/configuration.html)

## Database Config#

### `db.port`#

Name| Default| Required  
---|---|---  
db.port| 54322| false  
  
Description

Port to use for the local database URL.

See also

  * [PostgreSQL configuration](https://postgrest.org/en/stable/configuration.html)

### `db.shadow_port`#

Name| Default| Required  
---|---|---  
db.shadow_port| 54320| false  
  
Description

Port to use for the local shadow database.

See also

### `db.major_version`#

Name| Default| Required  
---|---|---  
db.major_version| 15| false  
  
Description

The database major version to use. This has to be the same as your remote
database's. Run `SHOW server_version;` on the remote database to check.

See also

  * [PostgreSQL configuration](https://postgrest.org/en/stable/configuration.html)

### `db.pooler.enabled`#

Name| Default| Required  
---|---|---  
db.pooler.enabled| false| false  
  
Description

Enable the local PgBouncer service.

See also

  * [PgBouncer Configuration](https://www.pgbouncer.org/config.html)

### `db.pooler.port`#

Name| Default| Required  
---|---|---  
db.pooler.port| 54329| false  
  
Description

Port to use for the local connection pooler.

See also

  * [PgBouncer Configuration](https://www.pgbouncer.org/config.html#listen_port)

### `db.pooler.pool_mode`#

Name| Default| Required  
---|---|---  
db.pooler.pool_mode| "transaction"| false  
  
Description

Specifies when a server connection can be reused by other clients. Configure
one of the supported pooler modes: `transaction`, `session`.

See also

  * [PgBouncer Configuration](https://www.pgbouncer.org/config.html#pool_mode)

### `db.pooler.default_pool_size`#

Name| Default| Required  
---|---|---  
db.pooler.default_pool_size| 20| false  
  
Description

How many server connections to allow per user/database pair.

See also

  * [PgBouncer Configuration](https://www.pgbouncer.org/config.html#default_pool_size)

### `db.pooler.max_client_conn`#

Name| Default| Required  
---|---|---  
db.pooler.max_client_conn| 100| false  
  
Description

Maximum number of client connections allowed.

See also

  * [PgBouncer Configuration](https://www.pgbouncer.org/config.html#max_client_conn)

### `db.seed.enabled`#

Name| Default| Required  
---|---|---  
db.seed.enabled| true| false  
  
Description

Enables running seeds when starting or resetting the database.

See also

### `db.seed.sql_paths`#

Name| Default| Required  
---|---|---  
db.seed.sql_paths| ["./seed.sql"]| false  
  
Description

An array of files or glob patterns to find seeds in.

See also

  * [Seeding your database](https://supabase.com/docs/guides/cli/seeding-your-database)

## Dashboard Config#

### `studio.enabled`#

Name| Default| Required  
---|---|---  
studio.enabled| true| false  
  
Description

Enable the local Supabase Studio dashboard.

See also

### `studio.port`#

Name| Default| Required  
---|---|---  
studio.port| 54323| false  
  
Description

Port to use for Supabase Studio.

See also

### `studio.api_url`#

Name| Default| Required  
---|---|---  
studio.api_url| "http://localhost"| false  
  
Description

External URL of the API server that frontend connects to.

See also

## Realtime Config#

### `realtime.enabled`#

Name| Default| Required  
---|---|---  
realtime.enabled| true| false  
  
Description

Enable the local Realtime service.

See also

### `realtime.ip_version`#

Name| Default| Required  
---|---|---  
realtime.ip_version| "IPv6"| false  
  
Description

Bind realtime via either IPv4 or IPv6. (default: IPv6)

See also

## Storage Config#

### `storage.enabled`#

Name| Default| Required  
---|---|---  
storage.enabled| true| false  
  
Description

Enable the local Storage service.

See also

  * [Storage server configuration](https://supabase.com/docs/guides/self-hosting/storage/config)

### `storage.file_size_limit`#

Name| Default| Required  
---|---|---  
storage.file_size_limit| "50MiB"| false  
  
Description

The maximum file size allowed (e.g. "5MB", "500KB").

See also

  * [Storage server configuration](https://supabase.com/docs/guides/self-hosting/storage/config)

## Edge-Functions Config#

### `functions.<function_name>.enabled`#

Name| Default| Required  
---|---|---  
functions.function_name.enabled| true| false  
  
Description

Controls whether a function is deployed or served. When set to false, the
function will be skipped during deployment and won't be served locally. This
is useful for disabling demo functions or temporarily disabling a function
without removing its code.

See also

  * [`supabase functions` CLI subcommands](https://supabase.com/docs/reference/cli/supabase-functions)

### `functions.<function_name>.verify_jwt`#

Name| Default| Required  
---|---|---  
functions.function_name.verify_jwt| true| false  
  
Description

By default, when you deploy your Edge Functions or serve them locally, it will
reject requests without a valid JWT in the Authorization header. Setting this
configuration changes the default behavior.

Note that the `--no-verify-jwt` flag overrides this configuration.

See also

  * [`supabase functions` CLI subcommands](https://supabase.com/docs/reference/cli/supabase-functions)

### `functions.<function_name>.import_map`#

Name| Default| Required  
---|---|---  
functions.function_name.import_map| None| false  
  
Description

Specify the Deno import map file to use for the Function.

Note that the `--import-map` flag overrides this configuration.

See also

  * [`supabase functions` CLI subcommands](https://supabase.com/docs/reference/cli/supabase-functions)

## Analytics Config#

### `analytics.enabled`#

Name| Default| Required  
---|---|---  
analytics.enabled| false| false  
  
Description

Enable the local Logflare service.

See also

  * [Self-hosted Logflare Configuration](https://supabase.com/docs/reference/self-hosting-analytics/list-endpoints#getting-started)

### `analytics.port`#

Name| Default| Required  
---|---|---  
analytics.port| 54327| false  
  
Description

Port to the local Logflare service.

See also

### `analytics.vector_port`#

Name| Default| Required  
---|---|---  
analytics.vector_port| 54328| false  
  
Description

Port to the local syslog ingest service.

See also

### `analytics.backend`#

Name| Default| Required  
---|---|---  
analytics.backend| "postgres"| false  
  
Description

Configure one of the supported backends:

  * `postgres`
  * `bigquery`

See also

  * [Self-hosted Logflare Configuration](https://supabase.com/docs/reference/self-hosting-analytics/list-endpoints#getting-started)

## Local Development Config#

### `inbucket.enabled`#

Name| Default| Required  
---|---|---  
inbucket.enabled| true| false  
  
Description

Enable the local InBucket service.

See also

  * [Inbucket documentation](https://www.inbucket.org)

### `inbucket.port`#

Name| Default| Required  
---|---|---  
inbucket.port| 54324| false  
  
Description

Port to use for the email testing server web interface.

Emails sent with the local dev setup are not actually sent - rather, they are
monitored, and you can view the emails that would have been sent from the web
interface.

See also

  * [Inbucket documentation](https://www.inbucket.org)

### `inbucket.smtp_port`#

Name| Default| Required  
---|---|---  
inbucket.smtp_port| 54325| false  
  
Description

Port to use for the email testing server SMTP port.

Emails sent with the local dev setup are not actually sent - rather, they are
monitored, and you can view the emails that would have been sent from the web
interface.

If set, you can access the SMTP server from this port.

See also

  * [Inbucket documentation](https://www.inbucket.org)

### `inbucket.pop3_port`#

Name| Default| Required  
---|---|---  
inbucket.pop3_port| 54326| false  
  
Description

Port to use for the email testing server POP3 port.

Emails sent with the local dev setup are not actually sent - rather, they are
monitored, and you can view the emails that would have been sent from the web
interface.

If set, you can access the POP3 server from this port.

See also

  * [Inbucket documentation](https://www.inbucket.org)

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/spec/cli_v1_config.yaml)

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

