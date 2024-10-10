[Back](/blog)

[Blog](/blog)

# AI Inference now available in Supabase Edge Functions

16 Apr 2024

•

7 minute read

[![Lakshan Perera
avatar](/_next/image?url=https%3A%2F%2Fgithub.com%2Flaktek.png&w=96&q=75)Lakshan
PereraEngineering](https://github.com/laktek)

![AI Inference now available in Supabase Edge
Functions](/_next/image?url=%2Fimages%2Fblog%2Fga-week%2Fai-inference-now-
available-in-supabase-edge-functions%2Fthumb.jpg&w=3840&q=100)

We're making it super easy to run AI models within Supabase Edge Functions. A
new built-in API is available within the Edge Runtime to run inference
workloads in just a few lines of code:

`  

_10

// Instantiate a new inference session

_10

const session = new Supabase.ai.Session('gte-small')

_10

_10

// then use the session to run inference on a prompt

_10

const output = await session.run('Luke, I am your father')

_10

_10

console.log(output)

_10

// [ -0.047715719789266586, -0.006132732145488262, ...]

  
`

With this new API you can:

  * Generate embeddings using models like `gte-small` to store and retrieve with pgvector. This is available today.
  * Use Large Language Models like `llama2` and `mistral` for GenAI workloads. This will be progressively rolled out as we get our hands on more GPUs.

In our previous Launch Week we [announced](/blog/hugging-face-supabase)
support for AI inference via Transformers.js. This was a good start but had
some shortcomings: it takes time to “boot” because it needs to instantiate a
WASM runtime and build the inference pipeline. We increased CPU limits to
mitigate this, but we knew we wanted a better Developer Experience.

In this post we'll cover some of the improvements to remove cold starts using
[Ort](https://github.com/pykeio/ort) and how we're adding LLM support using
[Ollama](https://ollama.com/).

## Generating Text Embeddings in Edge Functions#

Embeddings capture the "relatedness" of text, images, video, or other types of
information. Embeddings are stored in the database as an array of floating
point numbers, known as vectors. Since we [released](/openai-embeddings-
postgres-vector) pgvector on the platform, Postgres has become a popular
vector database.

Today's release solves a few technical challenges for developers who want to
generate embeddings from the content in their database, giving them the
ability to offload this compute-intensive task to background workers.

### Integrated pgvector experience#

You can now utilize [database webhooks](/docs/guides/database/webhooks) to
automatically generate embeddings whenever a new row is inserted into a
database table.

Because embedding creation is a compute-intensive task, it makes sense to
offload the work from your database. Edge Functions are the perfect
“background worker”. We've created a simple example to show how you can
generate embeddings in Edge Functions: [Semantic Search with pgvector and
Supabase Edge Functions](/docs/guides/functions/examples/semantic-search).

### Technical architecture#

Embedding generation uses the [ONNX runtime](https://onnxruntime.ai/) under
the hood. This is a cross-platform inferencing library that supports multiple
execution providers from CPU to specialized GPUs.

Libraries like `transformers.js` also use ONNX runtime which, in the context
of Edge Functions, runs as a WASM module, which can be slow during the
instantiation process.

To solve this, we built a native extension in Edge Runtime that enables using
ONNX runtime via the Rust interface. This was made possible thanks to an
excellent Rust wrapper called [Ort](https://github.com/pykeio/ort):

Embedding generation is fairly lightweight compared to LLM workloads, so it
can run on a CPU without hardware acceleration.

### Availability: open source embeddings#

Embeddings models are available on Edge Functions today. We currently support
[`gte-small`](https://huggingface.co/Supabase/gte-small) and we'll add more
embeddings models based on user feedback.

Embedding generation via `Supabase.ai` API is available today for all Edge
Functions users in both local, hosted, and self-hosted platforms.

### Lower costs#

Generating embeddings in an Edge Function doesn't cost anything extra: we
still charge on CPU usage. A typical embedding generation request should run
in less than a 1s, even from a cold start. Typically it won't use more than
100-200ms of CPU time.

Proprietary LLMs like OpenAI and Claude provide
[APIs](https://platform.openai.com/docs/guides/embeddings) to generate text
embeddings, charging per token. For example, OpenAI's `text-embedding-3-small`
cost $0.02/1M tokens at the time of writing this post.

Open source text embedding models provide similar performance to OpenAI's paid
models. For example, the `gte-small` model, which operates on 384 dimensions,
has an average of 61.36 compared to OpenAI's `text-embedding-3-small`, which
is at 62.26 on the [MTEB
leaderboard](https://huggingface.co/spaces/mteb/leaderboard), and they perform
search faster with [fewer dimensions](https://supabase.com/blog/fewer-
dimensions-are-better-pgvector).

With Supabase Edge Functions, you can generate text embeddings 10x cheaper
than OpenAI embeddings APIs.

## Large Language Models in Supabase Edge Functions#

Embedding generation only a part of the solution. Typically you need an LLM
(like OpenAI's GPT-3.5) to generate human-like interactions. We're working
with Ollama to make this possible with Supabase: local development, self-
hosted, and on the platform.

### Open source inference models#

We are excited to announce experimental support for Llama & Mistral with
`Supabase.ai` API.

The API is simple to use, with support for streaming responses:

`  

_28

const session = new Supabase.ai.Session('mistral')

_28

_28

Deno.serve(async (req: Request) => {

_28

// Get the prompt from the query string

_28

const params = new URL(req.url).searchParams

_28

const prompt = params.get('prompt') ?? ''

_28

_28

// Get the output as a stream

_28

const output = await session.run(prompt, { stream: true })

_28

_28

// Create a stream

_28

const stream = new ReadableStream({

_28

async start(controller) {

_28

const encoder = new TextEncoder()

_28

for await (const chunk of output) {

_28

controller.enqueue(encoder.encode(chunk.response ?? ''))

_28

}

_28

},

_28

})

_28

_28

// Return the stream to the user

_28

return new Response(stream, {

_28

headers: new Headers({

_28

'Content-Type': 'text/event-stream',

_28

Connection: 'keep-alive',

_28

}),

_28

})

_28

})

  
`

Check out the full guide [here](https://supabase.com/docs/guides/functions/ai-
models#using-large-language-models).

### Technical architecture#

LLM models are challenging to run directly via ONNX runtime on CPU. For these,
we are using a GPU-accelerated [Ollama](https://ollama.com/) server under the
hood:

We think this is a great match: the Ollama team have worked hard to ensure
that the local development experience is great, and we love development
environments that can be run without internet access (for those who enjoy
programming on planes).

As a Supabase developer, you don't have to worry about deploying models and
managing GPU instances - simply use a serverless API to get your job done.

### Availability: open source embeddings#

Access to open-source LLMs is currently invite-only while we manage demand for
the GPU instances. Please [get in
touch](https://forms.supabase.com/supabase.ai-llm-early-access) if you need
early access.

## Extending model support#

We plan to extend support for more models. [Let us
know](https://forms.supabase.com/supabase.ai-llm-early-access) which models
you want next. We're looking to support fine-tuned models too!

## Getting started#

Check out the Supabase docs today to get started with the AI models:

  * Edge Functions: [supabase.com/docs/guides/functions](https://supabase.com/docs/guides/functions)
  * Vectors: [supabase.com/docs/guides/ai](https://supabase.com/docs/guides/ai)
  * [Semantic search demo](https://github.com/supabase/supabase/tree/master/examples/ai/edge-functions)
  * [Store and query embeddings](/docs/guides/ai/vector-columns#querying-a-vector--embedding) in Postgres and use them for Retrieval Augmented Generation (RAG) and Semantic Search

[![GA logo](/_next/image?url=%2Fimages%2Flaunchweek%2Fga%2Fga-
black.svg&w=64&q=75)![GA
logo](/_next/image?url=%2Fimages%2Flaunchweek%2Fga%2Fga-
white.svg&w=64&q=75)Week](/ga-week)

15-19 April

[Day 1 -Supabase is officially launching into General Availability](/ga)[Day 2
-Supabase Functions now supports AI models](/blog/ai-inference-now-available-
in-supabase-edge-functions)[Day 3 -Supabase Auth now supports Anonymous sign-
ins](/blog/anonymous-sign-ins)[Day 4 -Supabase Storage: now supports the S3
protocol](/blog/s3-compatible-storage)[Day 5 -Supabase Security Advisor &
Performance Advisor](/blog/security-performance-advisor)

Build Stage

[01 -PostgreSQL Index Advisor](https://github.com/supabase/index_advisor)[02
-Branching now Publicly Available](/blog/branching-publicly-available)[03
-Oriole joins Supabase](/blog/supabase-acquires-oriole)[04 -Supabase on AWS
Marketplace](/blog/supabase-aws-marketplace)[05 -Supabase
Bootstrap](/blog/supabase-bootstrap)[06 -Supabase Swift](/blog/supabase-
swift)[07 -Top 10 Launches from Supabase GA Week](/blog/ga-week-summary)[Open
Source Hackathon 2024](/blog/supabase-oss-hackathon)[Community Meetups](/ga-
week#meetups)

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fai-
inference-now-available-in-supabase-edge-
functions&text=AI%20Inference%20now%20available%20in%20Supabase%20Edge%20Functions)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fai-
inference-now-available-in-supabase-edge-
functions&text=AI%20Inference%20now%20available%20in%20Supabase%20Edge%20Functions)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fai-
inference-now-available-in-supabase-edge-
functions&t=AI%20Inference%20now%20available%20in%20Supabase%20Edge%20Functions)

[Last postSupabase Auth now supports Anonymous Sign-ins17 April
2024](/blog/anonymous-sign-ins)

[Next postBranching now Publicly Available15 April 2024](/blog/branching-
publicly-available)

[launch-week](/blog/tags/launch-week)[database](/blog/tags/database)

On this page

  * Generating Text Embeddings in Edge Functions
    * Integrated pgvector experience
    * Technical architecture
    * Availability: open source embeddings
    * Lower costs
  * Large Language Models in Supabase Edge Functions
    * Open source inference models
    * Technical architecture
    * Availability: open source embeddings
  * Extending model support
  * Getting started

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fai-
inference-now-available-in-supabase-edge-
functions&text=AI%20Inference%20now%20available%20in%20Supabase%20Edge%20Functions)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fai-
inference-now-available-in-supabase-edge-
functions&text=AI%20Inference%20now%20available%20in%20Supabase%20Edge%20Functions)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fai-
inference-now-available-in-supabase-edge-
functions&t=AI%20Inference%20now%20available%20in%20Supabase%20Edge%20Functions)

## Build in a weekend, scale to millions

[Start your project](https://supabase.com/dashboard)[Request a
demo](/contact/sales)

