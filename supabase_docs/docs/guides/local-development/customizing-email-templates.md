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
  2.   3. Local development
  4.   5. [Customizing email templates](/docs/guides/local-development/customizing-email-templates)
  6. 

# Customizing email templates

## Customizing local email templates using config.toml.

* * *

You can customize the email templates for local development [using the
`config.toml` settings](/docs/guides/cli/config#auth-config).

## Configuring templates#

You should provide a relative URL to the `content_path` parameter, pointing to
an HTML file which contains the template. For example

supabase/config.toml

supabase/templates/invite.html

`  

_10

[auth.email.template.invite]

_10

subject = "You are invited to Acme Inc"

_10

content_path = "./supabase/templates/invite.html"

  
`

## Available email templates#

There are several Auth email templates which can be configured:

  * `auth.email.template.invite`
  * `auth.email.template.confirmation`
  * `auth.email.template.recovery`
  * `auth.email.template.magic_link`
  * `auth.email.template.email_change`

## Template variables#

The templating system provides the following variables for use:

### ConfirmationURL#

Contains the confirmation URL. For example, a signup confirmation URL would
look like:

`  

_10

https://project-ref.supabase.co/auth/v1/verify?token={{ .TokenHash
}}&type=signup&redirect_to=https://example.com/path

  
`

**Usage**

`  

_10

<p>Click here to confirm: {{ .ConfirmationURL }}</p>

  
`

### Token#

Contains a 6-digit One-Time-Password (OTP) that can be used instead of the
`ConfirmationURL`.

**Usage**

`  

_10

<p>Here is your one time password: {{ .Token }}</p>

  
`

### TokenHash#

Contains a hashed version of the `Token`. This is useful for constructing your
own email link in the email template.

**Usage**

`  

_10

<p>Follow this link to confirm your user:</p>

_10

<p>

_10

<a href="{{ .SiteURL }}/auth/confirm?token_hash={{ .TokenHash }}&type=email"

_10

>Confirm your email</a

_10

>

_10

</p>

  
`

### SiteURL#

Contains your application's Site URL. This can be configured in your project's
[authentication settings](/dashboard/project/_/auth/url-configuration).

**Usage**

`  

_10

<p>Visit <a href="{{ .SiteURL }}">here</a> to log in.</p>

  
`

### Email#

Contains the user's email address.

**Usage**

`  

_10

<p>A recovery request was sent to {{ .Email }}.</p>

  
`

### NewEmail#

Contains the new user's email address. This is only available in the
`email_change` email template.

**Usage**

`  

_10

<p>You are requesting to update your email address to {{ .NewEmail }}.</p>

  
`

## Deploying email templates#

These settings are for local development. To apply the changes locally, stop
and restart the Supabase containers:

`  

_10

supabase stop && supabase start

  
`

For hosted projects managed by Supabase, copy the templates into the [Email
Templates](/dashboard/project/_/auth/templates) section of the Dashboard.

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/content/guides/local-
development/customizing-email-templates.mdx)

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

