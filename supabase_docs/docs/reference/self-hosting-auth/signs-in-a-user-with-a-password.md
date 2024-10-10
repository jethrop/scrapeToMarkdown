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

Auth Server Reference

# Self-Hosting Auth

The Supabase Auth Server (GoTrue) is a JSON Web Token (JWT)-based API for
managing users and issuing access tokens.

GoTrue is an open-source API written in Golang, that acts as a self-standing
API service for handling user registration and authentication for JAM
projects. It's based on OAuth2 and JWT and handles user signup,
authentication, and custom user data.

### Client libraries#

  * [JavaScript](https://github.com/supabase/gotrue-js)
  * [Dart](https://github.com/supabase/gotrue-dart)

### Additional links#

  * [Source code](https://github.com/supabase/gotrue)
  * [Known bugs and issues](https://github.com/supabase/gotrue/issues)
  * [Auth guides](/docs/guides/auth)

* * *

## Generates an email action link.

post`/admin/generate_link`

### Body

  * dataOptionalobject

Object schema

  * emailOptionalstring

  * new_emailOptionalstring

  * passwordOptionalstring

  * redirect_toOptionalstring

  * typeOptionalstring

### Response codes

  * 200
  * 401

### Response (200)

exampleschema

    
    
    {
      "action_link": "lorem",
      "app_metadata": {
        "property1": null,
        "property2": null
      },
      "aud": "lorem",
      "banned_until": "2021-12-31T23:34:00Z",
      "confirmation_sent_at": "2021-12-31T23:34:00Z",
      "confirmed_at": "2021-12-31T23:34:00Z",
      "created_at": "2021-12-31T23:34:00Z",
      "email": "lorem",
      "email_change_sent_at": "2021-12-31T23:34:00Z",
      "email_confirmed_at": "2021-12-31T23:34:00Z",
      "email_otp": "lorem",
      "hashed_token": "lorem",
      "id": "fbdf5a53-161e-4460-98ad-0e39408d8689",
      "identities": [
        {
          "created_at": "2021-12-31T23:34:00Z",
          "id": "lorem",
          "identity_data": {
            "property1": null,
            "property2": null
          },
          "last_sign_in_at": "2021-12-31T23:34:00Z",
          "provider": "lorem",
          "updated_at": "2021-12-31T23:34:00Z",
          "user_id": "fbdf5a53-161e-4460-98ad-0e39408d8689"
        }
      ],
      "invited_at": "2021-12-31T23:34:00Z",
      "last_sign_in_at": "2021-12-31T23:34:00Z",
      "new_email": "lorem",
      "new_phone": "lorem",
      "phone": "lorem",
      "phone_change_sent_at": "2021-12-31T23:34:00Z",
      "phone_confirmed_at": "2021-12-31T23:34:00Z",
      "reauthentication_sent_at": "2021-12-31T23:34:00Z",
      "recovery_sent_at": "2021-12-31T23:34:00Z",
      "redirect_to": "lorem",
      "role": "lorem",
      "updated_at": "2021-12-31T23:34:00Z",
      "user_metadata": {
        "property1": null,
        "property2": null
      },
      "verification_type": "lorem"
    }

* * *

## Get a user.

get`/admin/user/{user_id}`

### Path parameters

  * user_idRequired

The user's id

### Response codes

  * 200
  * 401

### Response (200)

exampleschema

    
    
    {
      "app_metadata": {
        "property1": null,
        "property2": null
      },
      "aud": "lorem",
      "banned_until": "2021-12-31T23:34:00Z",
      "confirmation_sent_at": "2021-12-31T23:34:00Z",
      "confirmed_at": "2021-12-31T23:34:00Z",
      "created_at": "2021-12-31T23:34:00Z",
      "email": "lorem",
      "email_change_sent_at": "2021-12-31T23:34:00Z",
      "email_confirmed_at": "2021-12-31T23:34:00Z",
      "id": "fbdf5a53-161e-4460-98ad-0e39408d8689",
      "identities": [
        {
          "created_at": "2021-12-31T23:34:00Z",
          "id": "lorem",
          "identity_data": {
            "property1": null,
            "property2": null
          },
          "last_sign_in_at": "2021-12-31T23:34:00Z",
          "provider": "lorem",
          "updated_at": "2021-12-31T23:34:00Z",
          "user_id": "fbdf5a53-161e-4460-98ad-0e39408d8689"
        }
      ],
      "invited_at": "2021-12-31T23:34:00Z",
      "last_sign_in_at": "2021-12-31T23:34:00Z",
      "new_email": "lorem",
      "new_phone": "lorem",
      "phone": "lorem",
      "phone_change_sent_at": "2021-12-31T23:34:00Z",
      "phone_confirmed_at": "2021-12-31T23:34:00Z",
      "reauthentication_sent_at": "2021-12-31T23:34:00Z",
      "recovery_sent_at": "2021-12-31T23:34:00Z",
      "role": "lorem",
      "updated_at": "2021-12-31T23:34:00Z",
      "user_metadata": {
        "property1": null,
        "property2": null
      }
    }

* * *

## Update a user.

put`/admin/user/{user_id}`

### Path parameters

  * user_idRequired

The user's id

### Response codes

  * 200
  * 401

### Response (200)

exampleschema

    
    
    {
      "app_metadata": {
        "property1": null,
        "property2": null
      },
      "aud": "lorem",
      "banned_until": "2021-12-31T23:34:00Z",
      "confirmation_sent_at": "2021-12-31T23:34:00Z",
      "confirmed_at": "2021-12-31T23:34:00Z",
      "created_at": "2021-12-31T23:34:00Z",
      "email": "lorem",
      "email_change_sent_at": "2021-12-31T23:34:00Z",
      "email_confirmed_at": "2021-12-31T23:34:00Z",
      "id": "fbdf5a53-161e-4460-98ad-0e39408d8689",
      "identities": [
        {
          "created_at": "2021-12-31T23:34:00Z",
          "id": "lorem",
          "identity_data": {
            "property1": null,
            "property2": null
          },
          "last_sign_in_at": "2021-12-31T23:34:00Z",
          "provider": "lorem",
          "updated_at": "2021-12-31T23:34:00Z",
          "user_id": "fbdf5a53-161e-4460-98ad-0e39408d8689"
        }
      ],
      "invited_at": "2021-12-31T23:34:00Z",
      "last_sign_in_at": "2021-12-31T23:34:00Z",
      "new_email": "lorem",
      "new_phone": "lorem",
      "phone": "lorem",
      "phone_change_sent_at": "2021-12-31T23:34:00Z",
      "phone_confirmed_at": "2021-12-31T23:34:00Z",
      "reauthentication_sent_at": "2021-12-31T23:34:00Z",
      "recovery_sent_at": "2021-12-31T23:34:00Z",
      "role": "lorem",
      "updated_at": "2021-12-31T23:34:00Z",
      "user_metadata": {
        "property1": null,
        "property2": null
      }
    }

* * *

## Deletes a user.

delete`/admin/user/{user_id}`

### Path parameters

  * user_idRequired

The user's id

### Response codes

  * 200
  * 401

### Response (200)

schema

    
    
    {}

* * *

## List all users.

get`/admin/users`

### Response codes

  * 200
  * 401

### Response (200)

exampleschema

    
    
    {
      "aud": "lorem",
      "users": [
        {
          "app_metadata": {
            "property1": null,
            "property2": null
          },
          "aud": "lorem",
          "banned_until": "2021-12-31T23:34:00Z",
          "confirmation_sent_at": "2021-12-31T23:34:00Z",
          "confirmed_at": "2021-12-31T23:34:00Z",
          "created_at": "2021-12-31T23:34:00Z",
          "email": "lorem",
          "email_change_sent_at": "2021-12-31T23:34:00Z",
          "email_confirmed_at": "2021-12-31T23:34:00Z",
          "id": "fbdf5a53-161e-4460-98ad-0e39408d8689",
          "identities": [
            {
              "created_at": "2021-12-31T23:34:00Z",
              "id": "lorem",
              "identity_data": {
                "property1": null,
                "property2": null
              },
              "last_sign_in_at": "2021-12-31T23:34:00Z",
              "provider": "lorem",
              "updated_at": "2021-12-31T23:34:00Z",
              "user_id": "fbdf5a53-161e-4460-98ad-0e39408d8689"
            }
          ],
          "invited_at": "2021-12-31T23:34:00Z",
          "last_sign_in_at": "2021-12-31T23:34:00Z",
          "new_email": "lorem",
          "new_phone": "lorem",
          "phone": "lorem",
          "phone_change_sent_at": "2021-12-31T23:34:00Z",
          "phone_confirmed_at": "2021-12-31T23:34:00Z",
          "reauthentication_sent_at": "2021-12-31T23:34:00Z",
          "recovery_sent_at": "2021-12-31T23:34:00Z",
          "role": "lorem",
          "updated_at": "2021-12-31T23:34:00Z",
          "user_metadata": {
            "property1": null,
            "property2": null
          }
        }
      ]
    }

* * *

## Returns the created user.

post`/admin/users`

### Body

  * app_metadataOptionalobject

Object schema

  * audOptionalstring

  * ban_durationOptionalstring

  * emailOptionalstring

  * email_confirmOptionalboolean

  * passwordOptionalstring

  * phoneOptionalstring

  * phone_confirmOptionalboolean

  * roleOptionalstring

  * user_metadataOptionalobject

Object schema

### Response codes

  * 200
  * 401

### Response (200)

exampleschema

    
    
    {
      "app_metadata": {
        "property1": null,
        "property2": null
      },
      "aud": "lorem",
      "banned_until": "2021-12-31T23:34:00Z",
      "confirmation_sent_at": "2021-12-31T23:34:00Z",
      "confirmed_at": "2021-12-31T23:34:00Z",
      "created_at": "2021-12-31T23:34:00Z",
      "email": "lorem",
      "email_change_sent_at": "2021-12-31T23:34:00Z",
      "email_confirmed_at": "2021-12-31T23:34:00Z",
      "id": "fbdf5a53-161e-4460-98ad-0e39408d8689",
      "identities": [
        {
          "created_at": "2021-12-31T23:34:00Z",
          "id": "lorem",
          "identity_data": {
            "property1": null,
            "property2": null
          },
          "last_sign_in_at": "2021-12-31T23:34:00Z",
          "provider": "lorem",
          "updated_at": "2021-12-31T23:34:00Z",
          "user_id": "fbdf5a53-161e-4460-98ad-0e39408d8689"
        }
      ],
      "invited_at": "2021-12-31T23:34:00Z",
      "last_sign_in_at": "2021-12-31T23:34:00Z",
      "new_email": "lorem",
      "new_phone": "lorem",
      "phone": "lorem",
      "phone_change_sent_at": "2021-12-31T23:34:00Z",
      "phone_confirmed_at": "2021-12-31T23:34:00Z",
      "reauthentication_sent_at": "2021-12-31T23:34:00Z",
      "recovery_sent_at": "2021-12-31T23:34:00Z",
      "role": "lorem",
      "updated_at": "2021-12-31T23:34:00Z",
      "user_metadata": {
        "property1": null,
        "property2": null
      }
    }

* * *

## Receives the redirect from an external provider during the OAuth
authentication process. Starts the process of creating an access and refresh
token.

get`/callback`

### Response codes

  * 302

* * *

## The healthcheck endpoint for gotrue. Returns the current gotrue version.

get`/health`

### Response codes

  * 200

### Response (200)

exampleschema

    
    
    {
      "description": "lorem",
      "name": "lorem",
      "version": "lorem"
    }

* * *

## Sends an invite link to the user.

post`/invite`

### Body

  * dataOptionalobject

Object schema

  * emailOptionalstring

### Response codes

  * 200

### Response (200)

schema

    
    
    {}

* * *

## Logs out the user.

post`/logout`

### Response codes

  * 204

### Response (204)

schema

    
    
    {}

* * *

## Passwordless sign-in method for email or phone.

post`/otp`

### Body

  * create_userOptionalboolean

  * dataOptionalobject

Object schema

  * emailOptionalstring

  * phoneOptionalstring

### Response codes

  * 200

### Response (200)

schema

    
    
    {}

* * *

## Sends a password recovery email link to the user's email.

post`/recover`

### Body

  * emailOptionalstring

### Response codes

  * 200

### Response (200)

schema

    
    
    {}

* * *

## Returns the configuration settings for the gotrue server.

get`/settings`

### Response codes

  * 200

### Response (200)

exampleschema

    
    
    {
      "disable_signup": true,
      "external": {
        "apple": true,
        "azure": true,
        "bitbucket": true,
        "discord": true,
        "email": true,
        "facebook": true,
        "github": true,
        "gitlab": true,
        "google": true,
        "keycloak": true,
        "linkedin": true,
        "notion": true,
        "phone": true,
        "saml": true,
        "slack": true,
        "spotify": true,
        "twitch": true,
        "twitter": true,
        "workos": true,
        "zoom": true
      },
      "mailer_autoconfirm": true,
      "phone_autoconfirm": true,
      "sms_provider": "lorem"
    }

* * *

## Password-based signup with either email or phone.

post`/signup`

### Body

  * dataOptionalobject

Object schema

  * emailOptionalstring

  * passwordOptionalstring

  * phoneOptionalstring

### Response codes

  * 200

### Response (200)

exampleschema

    
    
    {
      "app_metadata": {
        "property1": null,
        "property2": null
      },
      "aud": "lorem",
      "banned_until": "2021-12-31T23:34:00Z",
      "confirmation_sent_at": "2021-12-31T23:34:00Z",
      "confirmed_at": "2021-12-31T23:34:00Z",
      "created_at": "2021-12-31T23:34:00Z",
      "email": "lorem",
      "email_change_sent_at": "2021-12-31T23:34:00Z",
      "email_confirmed_at": "2021-12-31T23:34:00Z",
      "id": "fbdf5a53-161e-4460-98ad-0e39408d8689",
      "identities": [
        {
          "created_at": "2021-12-31T23:34:00Z",
          "id": "lorem",
          "identity_data": {
            "property1": null,
            "property2": null
          },
          "last_sign_in_at": "2021-12-31T23:34:00Z",
          "provider": "lorem",
          "updated_at": "2021-12-31T23:34:00Z",
          "user_id": "fbdf5a53-161e-4460-98ad-0e39408d8689"
        }
      ],
      "invited_at": "2021-12-31T23:34:00Z",
      "last_sign_in_at": "2021-12-31T23:34:00Z",
      "new_email": "lorem",
      "new_phone": "lorem",
      "phone": "lorem",
      "phone_change_sent_at": "2021-12-31T23:34:00Z",
      "phone_confirmed_at": "2021-12-31T23:34:00Z",
      "reauthentication_sent_at": "2021-12-31T23:34:00Z",
      "recovery_sent_at": "2021-12-31T23:34:00Z",
      "role": "lorem",
      "updated_at": "2021-12-31T23:34:00Z",
      "user_metadata": {
        "property1": null,
        "property2": null
      }
    }

* * *

## Signs in a user with a password.

post`/token?grant_type=password`

### Body

  * emailOptionalstring

  * passwordOptionalstring

  * phoneOptionalstring

### Response codes

  * 200

### Response (200)

exampleschema

    
    
    {
      "access_token": "lorem",
      "expires_in": 42,
      "refresh_token": "lorem",
      "token_type": "lorem",
      "user": {
        "app_metadata": {
          "property1": null,
          "property2": null
        },
        "aud": "lorem",
        "banned_until": "2021-12-31T23:34:00Z",
        "confirmation_sent_at": "2021-12-31T23:34:00Z",
        "confirmed_at": "2021-12-31T23:34:00Z",
        "created_at": "2021-12-31T23:34:00Z",
        "email": "lorem",
        "email_change_sent_at": "2021-12-31T23:34:00Z",
        "email_confirmed_at": "2021-12-31T23:34:00Z",
        "id": "fbdf5a53-161e-4460-98ad-0e39408d8689",
        "identities": [
          {
            "created_at": "2021-12-31T23:34:00Z",
            "id": "lorem",
            "identity_data": {
              "property1": null,
              "property2": null
            },
            "last_sign_in_at": "2021-12-31T23:34:00Z",
            "provider": "lorem",
            "updated_at": "2021-12-31T23:34:00Z",
            "user_id": "fbdf5a53-161e-4460-98ad-0e39408d8689"
          }
        ],
        "invited_at": "2021-12-31T23:34:00Z",
        "last_sign_in_at": "2021-12-31T23:34:00Z",
        "new_email": "lorem",
        "new_phone": "lorem",
        "phone": "lorem",
        "phone_change_sent_at": "2021-12-31T23:34:00Z",
        "phone_confirmed_at": "2021-12-31T23:34:00Z",
        "reauthentication_sent_at": "2021-12-31T23:34:00Z",
        "recovery_sent_at": "2021-12-31T23:34:00Z",
        "role": "lorem",
        "updated_at": "2021-12-31T23:34:00Z",
        "user_metadata": {
          "property1": null,
          "property2": null
        }
      }
    }

* * *

## Refreshes a user's refresh token.

post`/token?grant_type=refresh_token`

### Body

  * refresh_tokenOptionalstring

### Response codes

  * 200

### Response (200)

exampleschema

    
    
    {
      "access_token": "lorem",
      "expires_in": 42,
      "refresh_token": "lorem",
      "token_type": "lorem",
      "user": {
        "app_metadata": {
          "property1": null,
          "property2": null
        },
        "aud": "lorem",
        "banned_until": "2021-12-31T23:34:00Z",
        "confirmation_sent_at": "2021-12-31T23:34:00Z",
        "confirmed_at": "2021-12-31T23:34:00Z",
        "created_at": "2021-12-31T23:34:00Z",
        "email": "lorem",
        "email_change_sent_at": "2021-12-31T23:34:00Z",
        "email_confirmed_at": "2021-12-31T23:34:00Z",
        "id": "fbdf5a53-161e-4460-98ad-0e39408d8689",
        "identities": [
          {
            "created_at": "2021-12-31T23:34:00Z",
            "id": "lorem",
            "identity_data": {
              "property1": null,
              "property2": null
            },
            "last_sign_in_at": "2021-12-31T23:34:00Z",
            "provider": "lorem",
            "updated_at": "2021-12-31T23:34:00Z",
            "user_id": "fbdf5a53-161e-4460-98ad-0e39408d8689"
          }
        ],
        "invited_at": "2021-12-31T23:34:00Z",
        "last_sign_in_at": "2021-12-31T23:34:00Z",
        "new_email": "lorem",
        "new_phone": "lorem",
        "phone": "lorem",
        "phone_change_sent_at": "2021-12-31T23:34:00Z",
        "phone_confirmed_at": "2021-12-31T23:34:00Z",
        "reauthentication_sent_at": "2021-12-31T23:34:00Z",
        "recovery_sent_at": "2021-12-31T23:34:00Z",
        "role": "lorem",
        "updated_at": "2021-12-31T23:34:00Z",
        "user_metadata": {
          "property1": null,
          "property2": null
        }
      }
    }

* * *

## Get information for the logged-in user.

get`/user`

### Response codes

  * 200
  * 401

### Response (200)

exampleschema

    
    
    {
      "app_metadata": {
        "property1": null,
        "property2": null
      },
      "aud": "lorem",
      "banned_until": "2021-12-31T23:34:00Z",
      "confirmation_sent_at": "2021-12-31T23:34:00Z",
      "confirmed_at": "2021-12-31T23:34:00Z",
      "created_at": "2021-12-31T23:34:00Z",
      "email": "lorem",
      "email_change_sent_at": "2021-12-31T23:34:00Z",
      "email_confirmed_at": "2021-12-31T23:34:00Z",
      "id": "fbdf5a53-161e-4460-98ad-0e39408d8689",
      "identities": [
        {
          "created_at": "2021-12-31T23:34:00Z",
          "id": "lorem",
          "identity_data": {
            "property1": null,
            "property2": null
          },
          "last_sign_in_at": "2021-12-31T23:34:00Z",
          "provider": "lorem",
          "updated_at": "2021-12-31T23:34:00Z",
          "user_id": "fbdf5a53-161e-4460-98ad-0e39408d8689"
        }
      ],
      "invited_at": "2021-12-31T23:34:00Z",
      "last_sign_in_at": "2021-12-31T23:34:00Z",
      "new_email": "lorem",
      "new_phone": "lorem",
      "phone": "lorem",
      "phone_change_sent_at": "2021-12-31T23:34:00Z",
      "phone_confirmed_at": "2021-12-31T23:34:00Z",
      "reauthentication_sent_at": "2021-12-31T23:34:00Z",
      "recovery_sent_at": "2021-12-31T23:34:00Z",
      "role": "lorem",
      "updated_at": "2021-12-31T23:34:00Z",
      "user_metadata": {
        "property1": null,
        "property2": null
      }
    }

* * *

## Returns the updated user.

put`/user`

### Body

  * app_metadataOptionalobject

Object schema

  * dataOptionalobject

Object schema

  * emailOptionalstring

  * nonceOptionalstring

  * passwordOptionalstring

  * phoneOptionalstring

### Response codes

  * 200
  * 401

### Response (200)

exampleschema

    
    
    {
      "app_metadata": {
        "property1": null,
        "property2": null
      },
      "aud": "lorem",
      "banned_until": "2021-12-31T23:34:00Z",
      "confirmation_sent_at": "2021-12-31T23:34:00Z",
      "confirmed_at": "2021-12-31T23:34:00Z",
      "created_at": "2021-12-31T23:34:00Z",
      "email": "lorem",
      "email_change_sent_at": "2021-12-31T23:34:00Z",
      "email_confirmed_at": "2021-12-31T23:34:00Z",
      "id": "fbdf5a53-161e-4460-98ad-0e39408d8689",
      "identities": [
        {
          "created_at": "2021-12-31T23:34:00Z",
          "id": "lorem",
          "identity_data": {
            "property1": null,
            "property2": null
          },
          "last_sign_in_at": "2021-12-31T23:34:00Z",
          "provider": "lorem",
          "updated_at": "2021-12-31T23:34:00Z",
          "user_id": "fbdf5a53-161e-4460-98ad-0e39408d8689"
        }
      ],
      "invited_at": "2021-12-31T23:34:00Z",
      "last_sign_in_at": "2021-12-31T23:34:00Z",
      "new_email": "lorem",
      "new_phone": "lorem",
      "phone": "lorem",
      "phone_change_sent_at": "2021-12-31T23:34:00Z",
      "phone_confirmed_at": "2021-12-31T23:34:00Z",
      "reauthentication_sent_at": "2021-12-31T23:34:00Z",
      "recovery_sent_at": "2021-12-31T23:34:00Z",
      "role": "lorem",
      "updated_at": "2021-12-31T23:34:00Z",
      "user_metadata": {
        "property1": null,
        "property2": null
      }
    }

* * *

## Verifies a sign up.

post`/verify`

### Body

  * emailOptionalstring

  * phoneOptionalstring

  * redirect_toOptionalstring

  * tokenOptionalstring

  * typeOptionalstring

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

