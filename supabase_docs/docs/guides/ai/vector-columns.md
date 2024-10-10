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

AI & Vectors

  1. [AI & Vectors](/docs/guides/ai)
  2.   3. Learn
  4.   5. [Vector columns](/docs/guides/ai/vector-columns)
  6. 

# Vector columns

* * *

Supabase offers a number of different ways to store and query vectors within
Postgres. The SQL included in this guide is applicable for clients in all
programming languages. If you are a Python user see your [Python client
options](/docs/guides/ai/python-clients) after reading the `Learn` section.

Vectors in Supabase are enabled via
[pgvector](https://github.com/pgvector/pgvector/), a PostgreSQL extension for
storing and querying vectors in Postgres. It can be used to store
[embeddings](/docs/guides/ai/concepts#what-are-embeddings).

## Usage#

### Enable the extension#

DashboardSQL

  1. Go to the [Database](https://supabase.com/dashboard/project/_/database/tables) page in the Dashboard.
  2. Click on **Extensions** in the sidebar.
  3. Search for "vector" and enable the extension.

### Create a table to store vectors#

After enabling the `vector` extension, you will get access to a new data type
called `vector`. The size of the vector (indicated in parenthesis) represents
the number of dimensions stored in that vector.

`  

_10

create table documents (

_10

id serial primary key,

_10

title text not null,

_10

body text not null,

_10

embedding vector(384)

_10

);

  
`

In the above SQL snippet, we create a `documents` table with a column called
`embedding` (note this is just a regular Postgres column - you can name it
whatever you like). We give the `embedding` column a `vector` data type with
384 dimensions. Change this to the number of dimensions produced by your
embedding model. For example, if you are [generating
embeddings](/docs/guides/ai/quickstarts/generate-text-embeddings) using the
open source [`gte-small`](https://huggingface.co/Supabase/gte-small) model,
you would set this number to 384 since that model produces 384 dimensions.

In general, embeddings with fewer dimensions perform best. See our [analysis
on fewer dimensions in pgvector](https://supabase.com/blog/fewer-dimensions-
are-better-pgvector).

### Storing a vector / embedding#

In this example we'll generate a vector using Transformers.js, then store it
in the database using the Supabase JavaScript client.

`  

_21

import { pipeline } from '@xenova/transformers'

_21

const generateEmbedding = await pipeline('feature-extraction', 'Supabase/gte-
small')

_21

_21

const title = 'First post!'

_21

const body = 'Hello world!'

_21

_21

// Generate a vector using Transformers.js

_21

const output = await generateEmbedding(body, {

_21

pooling: 'mean',

_21

normalize: true,

_21

})

_21

_21

// Extract the embedding output

_21

const embedding = Array.from(output.data)

_21

_21

// Store the vector in Postgres

_21

const { data, error } = await supabase.from('documents').insert({

_21

title,

_21

body,

_21

embedding,

_21

})

  
`

This example uses the JavaScript Supabase client, but you can modify it to
work with any [supported language library](/docs#client-libraries).

### Querying a vector / embedding#

Similarity search is the most common use case for vectors. `pgvector` support
3 new operators for computing distance:

Operator| Description  
---|---  
`<->`| Euclidean distance  
`<#>`| negative inner product  
`<=>`| cosine distance  
  
Choosing the right operator depends on your needs. Dot product tends to be the
fastest if your vectors are normalized. For more information on how embeddings
work and how they relate to each other, see [What are
Embeddings?](/docs/guides/ai/concepts#what-are-embeddings).

Supabase client libraries like `supabase-js` connect to your Postgres instance
via [PostgREST](/docs/guides/getting-started/architecture#postgrest-api).
PostgREST does not currently support `pgvector` similarity operators, so we'll
need to wrap our query in a Postgres function and call it via the `rpc()`
method:

`  

_23

create or replace function match_documents (

_23

query_embedding vector(384),

_23

match_threshold float,

_23

match_count int

_23

)

_23

returns table (

_23

id bigint,

_23

title text,

_23

body text,

_23

similarity float

_23

)

_23

language sql stable

_23

as $$

_23

select

_23

documents.id,

_23

documents.title,

_23

documents.body,

_23

1 - (documents.embedding <=> query_embedding) as similarity

_23

from documents

_23

where 1 - (documents.embedding <=> query_embedding) > match_threshold

_23

order by (documents.embedding <=> query_embedding) asc

_23

limit match_count;

_23

$$;

  
`

This function takes a `query_embedding` argument and compares it to all other
embeddings in the `documents` table. Each comparison returns a similarity
score. If the similarity is greater than the `match_threshold` argument, it is
returned. The number of rows returned is limited by the `match_count`
argument.

Feel free to modify this method to fit the needs of your application. The
`match_threshold` ensures that only documents that have a minimum similarity
to the `query_embedding` are returned. Without this, you may end up returning
documents that subjectively don't match. This value will vary for each
application - you will need to perform your own testing to determine the
threshold that makes sense for your app.

If you index your vector column, ensure that the `order by` sorts by the
distance function directly (rather than sorting by the calculated `similarity`
column, which may lead to the index being ignored and poor performance).

To execute the function from your client library, call `rpc()` with the name
of your Postgres function:

`  

_10

const { data: documents } = await supabaseClient.rpc('match_documents', {

_10

query_embedding: embedding, // Pass the embedding you want to compare

_10

match_threshold: 0.78, // Choose an appropriate threshold for your data

_10

match_count: 10, // Choose the number of matches

_10

})

  
`

In this example `embedding` would be another embedding you wish to compare
against your table of pre-generated embedding documents. For example if you
were building a search engine, every time the user submits their query you
would first generate an embedding on the search query itself, then pass it
into the above `rpc()` function to match.

Be sure to use embeddings produced from the same embedding model when
calculating distance. Comparing embeddings from two different models will
produce no meaningful result.

Vectors and embeddings can be used for much more than search. Learn more about
embeddings at [What are Embeddings?](/docs/guides/ai/concepts#what-are-
embeddings).

### Indexes#

Once your vector table starts to grow, you will likely want to add an index to
speed up queries. See [Vector indexes](/docs/guides/ai/vector-indexes) to
learn how vector indexes work and how to create them.

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/content/guides/ai/vector-
columns.mdx)

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

